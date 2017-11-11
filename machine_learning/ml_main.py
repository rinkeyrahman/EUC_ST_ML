from __future__ import print_function
import os
import time
import sys
import webbrowser
import importlib
import fetch_data as fd
import find_intention as fi
from machine_learning import LogisticRegression


class MlMain:
    """
    This class maintains total procedure of collecting dataset, user intention,
    training model and Firebase application triggering.

    Parameters
    ----------
    dataset : list
              Training dataset.
    domain : list
             List of domains. [domain, subdomain1, subdomain2, ...]
    sensor_name : list
                      List of sensor names.
    algorithm_name : string
                         selected algorithm name.
    is_append_intention : bool
                          True(if intent append)
                          false(if not)
    intention_id : string
                   current user intention id
    conditional_keys : list
                        List of conditional keywords.
    """
    def __init__(self):
        self.dataset = []
        self.domain = []
        self.sensor_name = []
        self.algorithm_name = str
        self.is_append_intention = bool
        self.intention_id = str
        self.conditional_keys = []

    def assemble_info(self):
        """
        Collects information from other .py files for training.
        :return:
        """
        obj = fd.FetchData(data_info_path="watch/selected_algo.json")
        # Collect training dataset.
        self.dataset = obj.extract_training_data()
        print ("Extracting Dataset for training...")
        # Collects training information.
        self.domain, self.sensor_name, self.algorithm_name = obj.extract_training_info()
        obj = fi.FindIntention(current_user_intent_path="watch/user_intention.json")
        print ("Find user intention if exist otherwise append new user intention")
        # Intention status info.
        self.is_append_intention, self.intention_id, self.conditional_keys = (
            obj.append_intention())

    def feed_into_algorithm(self):
        """
        Sends training dataset and intention id to a selected Ml algorithm
        for training.
        :return:
        """
        self.assemble_info()
        # If new intention added then sends info to an algorithm for training.
        if self.is_append_intention == True:
            print ("New intention added and start training dataset on selected algorithm")
            algorithm = importlib.import_module(self.algorithm_name)
            obj = getattr(algorithm, self.algorithm_name)(self.dataset, self.intention_id)
            obj.train_model()
            # print ("Accuracy : ", obj.accuracy())

    def periodic_prediction(self):
        """
        Call the functions for new requirement prediction and send insight to Firebase.
        :return:
        """
        import prediction as pd
        obj = (pd.Prediction(domain=self.domain, intention_id=self.intention_id,
                             conditional_keys=self.conditional_keys))
        print ("Predicting real time value according to user given data")
        insight = obj.export_insights_firebase()

    def trigger(self):
        cached_stamp = 0
        filename = "watch/selected_algo.json"
        stamp = os.stat(filename).st_mtime
        if stamp != cached_stamp:
            cached_stamp = stamp
        print("file updated", file=sys.stderr)
        self.feed_into_algorithm()
        from twisted.internet import task
        from twisted.internet import reactor
        from datetime import datetime
        print("Redirecting to user info form ...", file=sys.stderr)
        url = "http://localhost:5000/form"
        webbrowser.open_new(url)
        time.sleep(60)
        self.periodic_prediction()
        time.sleep(3600)


obj = MlMain().trigger()


