import numpy as np
import pymysql as db
import json


class FetchData:
    """
    Extract training dataset from local server database.

    Parameters
    ----------
    data_info_path : string
                     contains a json file path
                     #data_info_path = "selected_algo.json"
    """

    def __init__(self, data_info_path):
        self.data_info_path = data_info_path
        with open(self.data_info_path, 'rb') as f:
            self.data_info = json.load(f)
            f.close()

    def extract_info(self):
        """
        Extract all necessary info from json file.
        Note : see "selected_algo.json" file.
        :return:
        """
        self.domain = self.data_info["Domain"]
        self.sensor_name = self.data_info["Sensor_name"]
        self.algorithm_name = self.data_info["Algorithm_name"]
        self.output_attribute = self.data_info["Output_attribute"]
        self.traing_attribute = self.data_info["Training_attributes"]

    def extract_training_data(self):
        """
        Extract Training data from database.

        :return:
        dataset = numpy array
                  training dataset.
        """
        self.extract_info()
        dbname = self.domain[0]
        table_name = self.domain[1]
        # Connect to database.
        connection = db.Connection(host="localhost", user="root", db=dbname)
        dbhandler = connection.cursor()
        query = "select "
        for i in range(0, len(self.traing_attribute)):
            query += "`" + self.traing_attribute[i] + "`"
            if i != len(self.traing_attribute) - 1:
                query += ","
        query += "from `" + table_name + "`"
        dbhandler.execute(query=query)
        self.training_data = dbhandler.fetchall()
        # Convert to numpy array.
        self.training_data = np.array(self.training_data)
        # If output attribute is present then append it to dataset.
        if len(self.output_attribute) > 0:
            # Extract output attribute value from database.
            query = "select `" + self.output_attribute + "` from `" + table_name + "`"
            dbhandler.execute(query=query)
            self.target_data = dbhandler.fetchall()
            self.target_data = np.array(self.target_data)
            # Append after last column.
            self.dataset = np.append(self.training_data, self.target_data, axis=1)
        else:
            # If no output attribute.
            self.target_data = None
            self.dataset = self.training_data

        length = len(self.dataset)
        # remove last row for containing NULL values.
        self.dataset = np.delete(self.dataset, length-1, 0)
        return self.dataset

    def extract_training_info(self):
        """
        Extract trining info to make decision how to train the dataset.

        :return:
        domain : list
             List of domains. [domain, subdomain1, subdomain2, ...]
        sensor_name : list
                      List of sensor names.
        algorithm_name : string
                         selected algorithm name.
        """
        self.extract_info()
        return self.domain, self.sensor_name, self.algorithm_name
