import socket
import traceback
import csv
import pandas as pd
import time
import os
import math

activity = 1
waitTime = 5

host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
data = []


def createTrainLog(activity):
    f = open('0' + str(activity) + '_trainLog.csv', 'w')
    f.write('time,sensor,x,y,z,sensor,x,y,z,sensor,x,y,z,activity\n')
    return f


def receiveData(activity, f):
    try:
        message, address = s.recvfrom(8192)
        print "Receiving Data"
        f.write(message + ', ' + str(activity) + ' \n ')
    except (KeyboardInterrupt, SystemExit):
        print data
        f.close()
        raise
    except:
        traceback.print_exc()


# Activities: Stand = 1, Sit = 2, Bend = 3, Crouch = 4, Walk = 5



def beep(a, b, c="sine"):
    # a = Duration
    # b = Frequency
    # c = Waveform
    os.system('play --no-show-progress --null --channels 1 synth %s %s %f' % (a, c, b))


def countdown(seconds):
    while seconds > 0:
        print seconds
        beep(0.5, 440)
        seconds -= 1
        time.sleep(1)


def activityTimer(activity, timeLimit=10):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "Prepare to execute Activty " + str(activity) + " in..."
    countdown(waitTime)
    print "Execute Activity " + str(activity)
    beep(1, 660)
    now = time.time()
    secs = timeLimit
    f = createTrainLog(activity)

    while (time.time() - now) <= timeLimit:

        receiveData(activity, f)
        if ((time.time() - now) == math.floor(time.time() - now)):
            print "Stop in " + str(secs)
            secs -= 1

    beep(1, 100, "saw")
    print "Stop"
    time.sleep(waitTime)


for i in range(1, 6):
    activityTimer(activity)
    activity += 1

print "Finished Capturing Data"
