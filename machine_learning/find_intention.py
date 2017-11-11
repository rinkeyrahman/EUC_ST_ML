import json


class FindIntention:
    """
    Checks if the user call a service with a new intention or an existing intention.
    User intention is identified by set of sensors name and conditions user uses for
    a service. If the set of sensors name and conditional keys already exist then don't
    append it otherwise append it with a new intention id in "previous_intention.json".
    Here new intention id is a string as total number of previous intention.

    Parameters
    ----------
    current_user_intent_path : string
                               contains current user's used sensor name & conditional
                               key list.
                               current_user_intent_path = "user_intention.json".
    """

    def __init__(self, current_user_intent_path):
        self.user_intention_path = current_user_intent_path
        with open(self.user_intention_path, 'rb') as f:
            self.user_intention = json.load(f)
            f.close()

    def new_intention_info(self):
        """
        Gather information for current user intention using sensor list and
        conditional keywords.
        Note : See "user_intention.json".

        :return:
        sensor_name : list
                      List of sensor names.
        conditional_keys : list
                           List of conditional keywords.
        """
        sensor_name = self.user_intention['Sensor_name']
        temp_str = []
        conditional_keys = []
        # Extract all conditional keywords.
        for i in range(0, len(self.user_intention['Services'])):
            temp_str.append(self.user_intention['Services'][i]["Conditional_keywords"])
        # Filter and extract conditional keywords without repetitions.
        for i in range(0, len(temp_str)):
            if temp_str[i] in conditional_keys == False:
                conditional_keys.append(temp_str[i])
        return sensor_name, conditional_keys

    def is_intention_exist(self):
        """
        Checks if the intention is already exist or not.

        :return:
        -1 : if intention doesn't exist.
        intention id : id number if intention exist.
        """
        # Gather current intention info.
        sensor_name, conditional_keys = self.new_intention_info()
        # Gather previous intention info.
        previous_intention_path = "info/previous_intention.json"
        with open(previous_intention_path, 'rb') as f:
            previous_intention = json.load(f)
            f.close()
        # If no previous intention return -1.
        if len(previous_intention) == 0:
            return -1
        else:
            j = 0
            k = 0
            # Check all previous intent.
            for i in range(0, len(previous_intention)):
                # If the length of the set of sensors & conditional keys are same.
                if len(sensor_name) == (len(previous_intention[i]['Sensor_name'])
                                        and len(conditional_keys) ==
                                        len(previous_intention[i]['Conditional_keywords'])):
                    # check sensor name list with previous sensor name list.
                    for j in range(0, len(sensor_name)):
                        # If doesn't match then return -1.
                        if sensor_name[j] in previous_intention[i]['Sensor_name'] == False:
                            j -= 1
                            break
                    # Check conditional keys with all previous conditional keys.
                    for k in range(0, len(conditional_keys)):
                        # If doesn't match return -1.
                        if (conditional_keys[k] in previous_intention[i]
                                ['Conditional_keywords'] == False):
                            k -= 1
                            break
                    # If find any identical set of sensors & cond. keys then return
                    # intention id.
                    if j == len(sensor_name) -1 and k == len(conditional_keys) -1:
                        return previous_intention[i]["intention_id"]
        return -1

    def append_intention(self):
        """
        Append current user intention to previous intention json file.

        :return:
        bool : True(if append)
               False(if not append)
        intention_id : integer
                       intention id.
        conditional_keys : list
                           List of conditional keys.
        """
        # Get intention id.
        intention_id = self.is_intention_exist()
        conditional_keys = []
        # If intention doesn't exist.
        if intention_id == -1:
            # Open previous intention file.
            previous_intention_path = "info/previous_intention.json"
            with open(previous_intention_path) as f:
                previous_intention = json.load(f)
                # f.close()

            length = len(previous_intention)
            # Current intention info.
            sensor_name, conditional_keys = self.new_intention_info()
            # Create a dictionary of current user intention information.
            new_intent_info = {}
            new_intent_info["intention_id"] = str(length)
            new_intent_info["Sensor_name"] = sensor_name
            new_intent_info["Conditional_keywords"] = conditional_keys
            # Open the file to read.
            with open(previous_intention_path, 'r') as f:
                intent_data = json.load(f)
                f.close()
            # Append new intention.
            intent_data.append(new_intent_info)
            # Dumps the file.
            json.dumps(intent_data)
            # Open the previous intention file to write.
            with open(previous_intention_path, 'w') as f:
                # Write the appended file.
                json.dump(intent_data, f)
                f.close()
            # Return True, intention id and cond.keys.
            return True, str(length), conditional_keys
        return False, intention_id, conditional_keys
