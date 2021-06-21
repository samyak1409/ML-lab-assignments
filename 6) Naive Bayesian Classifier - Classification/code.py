# Assignment 6: Assuming a set of documents that need to be classified, use the naive Bayesian Classifier model to
# perform this task. Built-in Java classes/API can be used to write the program. Calculate the accuracy, precision, and
# recall for your data set.


from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import classification_report

categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train',categories=categories,shuffle=True)
twenty_test = fetch_20newsgroups(subset='test',categories=categories,shuffle=True)
print()
print(len(twenty_train.data))
print(len(twenty_test.data))
print(twenty_train.target_names)
print("\n".join(twenty_train.data[0].split("\n")))
print(twenty_train.target[0])

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
X_train_tf = count_vect.fit_transform(twenty_train.data)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_tf)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn import metrics

mod = MultinomialNB()
mod.fit(X_train_tfidf, twenty_train.target)
X_test_tf = count_vect.transform(twenty_test.data)
X_test_tfidf = tfidf_transformer.transform(X_test_tf)
predicted = mod.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(twenty_test.target, predicted))
print(classification_report(twenty_test.target,predicted,target_names=twenty_test.target_names))

print("confusion matrix is \n",metrics.confusion_matrix(twenty_test.target, predicted))

# NOTE: this code is taken from https://github.com/rajathv/Machine-Learning-Lab/blob/master/labprogram6/labprog6.py
