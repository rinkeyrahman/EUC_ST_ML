import pymysql as db
import json
import numpy as np


class Assemble:
    """
    To predict result for a service domain collects the End User data.
    first collects the trained attribute list from a json file "selected_algo.json"
    then according to the sequence of trained attribute list it assembles the end user
    value from "user_info.json" which contains user value from a form. If any value is
    missing in this json file that means the value is collected from sensors. Then
    collects the values from sensor database.

    Parameters
    ----------
    attribute_list_path : string
                          path name of "selected_algo.json"
    form_attribute_list_path : string
                               path name of "user_info.json"
    #attribute_list_path = "selected_algo.json"
    #form_attribute_list_path = "user_info.json"
    """

    def __init__(self, attribute_list_path, form_attribute_list_path):
        self.attribute_list_path = attribute_list_path
        self.form_attribute_list_path = form_attribute_list_path
        # Read json file.
        with open(self.attribute_list_path, 'rb') as f:
            self.attribute_list = json.load(f)
            f.close()
        with open(self.form_attribute_list_path, 'rb') as f:
            self.form_attribute = json.load(f)
            # Extract keys name from dictionary.
            self.form_attribute_keys = self.form_attribute.keys()
            f.close()

    def type_conversion(self):
        # Converts the numberstrings of end user value to numeric value.
        for i in range(0, len(self.form_attribute_keys)):
            # Check if the string contains digit.
            if self.form_attribute[self.form_attribute_keys[i]].isdigit() == True:
                # check if integer.
                if self.form_attribute[self.form_attribute_keys[i]].find('.') == -1:
                    self.form_attribute[self.form_attribute_keys[i]] = (
                        int(self.form_attribute[self.form_attribute_keys[i]]))

                else:
                    # Otherwise float.
                    self.form_attribute[self.form_attribute_keys[i]] = (
                        float(self.form_attribute[self.form_attribute_keys[i]]))

    def fetch_attribute_list(self):
        # Fetch trained attribute list
        self.attribute_list = self.attribute_list["Training_attributes"]
        # Reconstruct attribute name to match with end user form attribute name.
        # See user_info.json.
        for i in range(0, len(self.attribute_list)):
            self.attribute_list[i] = self.attribute_list[i].replace('_', ' ')
            self.attribute_list[i] = self.attribute_list[i].upper()

    def fetch_test_data(self):
        """
        To predict result gathers new test data from json file and sensor database.
        :return
        test_data : numpy array
                    real time value of end user.
        """
        self.fetch_attribute_list()
        self.type_conversion()
        # Connect to sensor database.
        connection = db.Connection(host="localhost", user="root", db="sensor")
        dbhandler = connection.cursor()
        test_data = []
        for i in range(0, len(self.attribute_list)):
            # If the value is in user_info.json file.
            if self.attribute_list[i] in self.form_attribute_keys == True:
                test_data.append(self.form_attribute[self.attribute_list[i]])
            else:
                # Value is in database.
                # Reconstruct attribute name to match with table column name.
                self.attribute_list[i] = self.attribute_list[i].replace(' ', '_')
                self.attribute_list[i] = self.attribute_list[i].lower()
                # Fetch last inserted value of that attribute.
                query = "select `"
                query += (self.attribute_list[i] + "`FROM `" + self.attribute_list[i]
                          + "` ORDER BY `" + self.attribute_list[i] + "` DESC LIMIT 1")
                dbhandler.execute(query=query)
                value = dbhandler.fetchall()
                print value
                # Append to test_data
                test_data.append(value[0][0])
                print test_data
        return np.array(test_data)
