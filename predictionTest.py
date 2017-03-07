from sklearn import tree, metrics
import tensorflow.contrib.learn as tf


# Read data sets
with open("HAPT/Train/X_train.txt") as x_train:
    x = list(x_train)
with open("HAPT/Train/y_train.txt") as y_train:
    y = list(y_train)
with open("HAPT/Test/X_test.txt") as x_test:
    x_test = list(x_test)
with open("HAPT/Test/y_test.txt") as y_test:
    y_test = list(y_test)


# Convert the strings inside the lists into floats
x = [map(float, group.split()) for group in x]
x_test = [map(float, group.split()) for group in x_test]

# Convert the strings inside the lists into integers
y = map(int, y)
y_test = map(int, y_test)


# Create classifier and fit
# Sklearn Tree
tree_clf = tree.DecisionTreeClassifier()
tree_clf.fit(x, y)

# TensorFlow Linear Classifier
feature_colums = tf.infer_real_valued_columns_from_input(x)
tf_clf = tf.LinearClassifier(n_classes=12, feature_columns=feature_colums)
tf_clf.fit(x, y)
prediction = list(tf_clf.predict(x, as_iterable=True))

# Evaluate accuracy
tree_score = metrics.accuracy_score(y_test, tree_clf.predict(x_test))
tf_score = metrics.accuracy_score(y_test, prediction)
print("Tree Accuracy: %f" % tree_score)
print("TensorFlow Accuracy: %f" % tf_score)

