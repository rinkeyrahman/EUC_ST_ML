from sklearn.linear_model import LogisticRegression as logisticregression
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import metrics
import numpy as np


class LogisticRegression:
    """
    Logistic Regression.
    This class supports multi-class classification.
    Note : see https://en.wikipedia.org/wiki/Logistic_regression

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
        alpha : float
                Learning rate.
        accuracy_rate : float
                        accuracy rate of the selected training model.
        """
        range = 20
        # Generate 20 uniform random value for alpha(learning rate)
        alpha_range = np.random.uniform(0.003, 3, range)
        alpha_scores = []
        # For every value of alpha evaluate with k-fold cross validation.
        # where number of fold(cv = 10)
        for alpha in alpha_range:
            # Initialize Logistic regression
            lg = logisticregression(alpha)
            # cross validation
            scores = cross_val_score(lg, self.training_data, self.target_data, cv=10,scoring='accuracy'))                                    ))
            # Average the accuracy rate of 10 folds.
            alpha_scores.append(scores.mean())

        #%matplotlib inline
        #plt.plot(alpha_range, alpha_scores)
        #plt.xlabel('Value of alpha for Logistic Regression')
        #plt.ylabel('Cross-Validated Accuracy')
        #plt.show()
        alpha_scores = np.array(alpha_scores)
        index = alpha_scores.argmax(axis=0)
        alpha = alpha_range[index]
        accuracy_rate = alpha_scores[index]
        return alpha, accuracy_rate

    def train_model(self):
        """
        After evaluating the training model, train the model and save the model as
        .pkl file(compressed).
        :return:
        """
        alpha, accuracy_rate = self.select_model()
        # Initialize logistic regression with alpha(learning rate)
        lg = logisticregression(C=alpha)
        # Train the model.
        lg.fit(self.training_data, self.target_data)
        # Save the trained model as .pkl file.
        joblib.dump(value=lg, filename=self.intention_id+'.pkl', compress=1)
        print "Estimated Parameters of Logistic Regression"
        # Estimated parameters of logistic regression.
        print lg.get_params()

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
        lg = joblib.load(filename=self.intention_id+'.pkl')
        # predict new value and return.
        return lg.predict(predict_value)
