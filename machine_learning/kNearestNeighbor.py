from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import metrics
import numpy as np


class KNearestNeighbor:
    """
    K Nearest Neighbor.
    This class supports multi-class classification.
    Note : see https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm

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
                number of neighbor.
        accuracy_rate : float
                        accuracy rate of the selected training model.
        """
        # Range of number of neighbor in knn.
        k_range = range(1, 31)
        k_scores = []
        # For every number of neighbor evaluate with k-fold cross validation.
        # where number of fold(cv = 10)
        for k in k_range:
            knn = KNeighborsClassifier(n_neighbors=k)
            scores = (cross_val_score(knn, self.training_data, self.target_data,
                                      cv=10, scoring='accuracy'))
            k_scores.append(scores.mean())

        # %matplotlib inline
        # plt.plot(k_range, k_scores)
        # plt.xlabel('Value of K for KNN')
        # plt.ylabel('Cross-Validated Accuracy')
        # plt.show()
        model = 0
        accuracy_rate = 0.0
        for i in range(0, len(k_scores)):
            if k_scores[i] >= accuracy_rate:
                accuracy_rate = k_scores[i]
                model = i
        return model + 1, accuracy_rate

    def train_model(self):
        """
        After evaluating the training model, train the model and save the model as
        .pkl file(compressed).
        :return:
        """

        model, accuracy_rate = self.select_model()
        # initialize knn
        knn = KNeighborsClassifier(n_neighbors=model)
        # train model.
        knn.fit(self.training_data, self.target_data)
        # save model as .pkl file.
        joblib.dump(value=knn, filename=self.intention_id+'.pkl', compress=1)

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
        knn = joblib.load(filename=self.intention_id+'.pkl')
        # Predict new value and return.
        return knn.predict(predict_value)
