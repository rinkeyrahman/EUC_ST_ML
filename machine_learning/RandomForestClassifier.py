from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import metrics
import numpy as np


class RandomForestclassifier:
    """
    random Forest Classifier.
    This class supports multi-class classification.
    Note : see https://en.wikipedia.org/wiki/Random_forest

    :parameter
    dataset : list
              Training dataset.
    intention_id : string
                   user intention id.
    """
    def __init__(self, dataset, intention_id):
        self.dataset = dataset
        self.intention_id = intention_id
        column = len(self.dataset[0])
        temp = range(0, column-1)
        self.training_data = np.array(self.dataset[:, temp])
        self.target_data = np.array(self.dataset[:, column-1])

    def select_model(self):
        """
        Evaluate and select training model using k-fold cross validation methods.
        Note : https://en.wikipedia.org/wiki/Cross-validation_(statistics)

        :return:
        model : integer
                Number of trees in forest.
        accuracy_rate : float
                        accuracy rate of the selected training model.
        """
        # Initialize a range of trees.
        n_range = range(1, 31)
        n_scores = []
        # For every number of trees evaluate with k-fold cross validation.
        # where number of fold(cv = 10)
        for n in n_range:
            # Initialize random forest.
            clf = (RandomForestClassifier(n_estimators=n, max_depth=None,
                                          min_samples_split=2, random_state=0,
                                          bootstrap=True))
            # Cross validation
            scores = (cross_val_score(estimator=clf, X=self.training_data,
                                      y=self.target_data, scoring='accuracy', cv=10))
            # Average the accuracy rate of 10 folds.
            n_scores.append(scores.mean())

        # plt.plot(n_range, n_scores)
        # plt.xlabel("Value of number of Tree in Random Forest")
        # plt.ylabel("'Cross-Validated Accuracy'")
        # plt.show()
        model = 0
        accuracyrate = 0.0
        for i in range(0, len(n_scores)):
            if n_scores[i] >= accuracyrate:
                accuracyrate = n_scores[i]
                model = i
        return model + 1, accuracyrate

    def train_model(self):
        """
        After evaluating the training model, train the model and save the model as
        .pkl file(compressed).
        :return:
        """
        model, accuracyrate = self.select_model()
        # Initialize random forest with model(number of trees).
        clf = (RandomForestClassifier(n_estimators=model, max_depth=None,
                                      min_samples_split=2, random_state=0, bootstrap=True))
        # Train the model.
        clf.fit(self.training_data, self.target_data)
        # Save the trained model as .pkl file.
        joblib.dump(value=clf, filename=self.intention_id+'.pkl', compress=1)

    def accuracy(self):
        """
        After completing the training, compute predictive accuracy.

        :return:
        predictive accuarcy
        """
        # Load tarined model using intent id.
        clf = joblib.load(filename=self.intention_id+'.pkl')
        # Compute accuracy for hole training data and return.
        return clf.score(X=self.training_data, y=self.target_data)

    def predict_new_value(self, predict_value):
        """
        Predict new value.
        :param
        predict_value: list
                        List of feature value for new data.
        :return:
        predicted result.
        """
        # Load the trained model.
        clf = joblib.load(filename=self.intention_id+'.pkl')
        # predict new value and return.
        return clf.predict(predict_value)
