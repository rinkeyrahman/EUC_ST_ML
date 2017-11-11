from sklearn.externals import joblib


class Prediction:
    """
    Predict the result of real time value of end user. First load the trained model using
    intention id then predict current user value. If the result is in user's
    conditional keys then send the insight to Firebase.

    Parameters
    ----------
    domain : list
             List of domains. [domain, subdomain1, subdomain2, ...]
    intention_id : string
    conditional_keys : list
                       user's condition list to provide services.

    """

    def __init__(self, domain, intention_id, conditional_keys):
        self.domain = domain
        self.intention_id = intention_id
        self.conditional_keys = conditional_keys

    def predict_user_data(self):
        """
        Fetch current user value. then load the trained model using intention id and
        predict result.
        :return:
        list of insight.
        """
        import end_user_value as euv
        # Fetch current user data.
        test_data = euv.Assemble("watch/selected_algo.json", "watch/user_info.json").fetch_test_data()
        # Load trained model.
        clf = joblib.load(filename=self.intention_id+'.pkl')
        # Predict and return result.
        return clf.predict(test_data)

    def export_insights_firebase(self):
        """
        If the predicted value match with user's conditional keys then trigger
        Firebase application.
        :return:
        """
        insight = self.predict_user_data()
        print insight
        # if result is in conditional keys.
        if insight in self.conditional_keys:
            import fire_base
            # Send values to Firebase class
            obj = fire_base.FireBase(domain=self.domain, insight=insight)
            # Export to application.
            obj.export_insights()
