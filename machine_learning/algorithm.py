from __future__ import print_function
import json
import sys
import config as cfg
import attribute as attr



class Algorithm:
  """
    This class maintains procedure of algorithm selection.

    Parameters
    ----------

    algo: dict
          selected algorithm and training dataset information.
    algo_name : string
                  name of the selected algorithm.
  """
    
  def __init__(self):  
    self.algo={"Algorithm_name":"",
      "Sensor_name":"",
      "Domain":"",
      "Output_attribute":"",
      "Number_of_training_attributes":"",
      "Training_attributes":""
      }
    self.algo_name=""


  def supervised_algorithm_selection(self,output):
    """
        determine appropriate algorithm for supervised learning problem.
        :return: selected algorithm name.
    """
    obj=attr.Attribute()
    self.output=output
    self.x_type=obj.xtype()
    print(self.x_type,file=sys.stderr)
    self.unique_value_x=obj.unique_x()
    print(self.unique_value_x,file=sys.stderr)
    if(self.x_type=="categorical"):
      if(self.unique_value_x==2):
        self.predict_value="binary"
      else:
        self.predict_value="multiple"
    else:
     self.predict_value="single"

    self.dataset=obj.dataset_information()
    print(self.dataset,file=sys.stderr)
    l=len(cfg.algo["Algorithm"])
    for i in range(l):
      if(cfg.algo["Algorithm"][i]["Output_dataset"]==self.output):

        if(cfg.algo["Algorithm"][i]["Output_data_type"]==self.x_type):

            if(cfg.algo["Algorithm"][i]["Prediction_type"][0]==self.predict_value or cfg.algo["Algorithm"][i]["Prediction_type"][1]==self.predict_value):
                algo_l=len(cfg.algo["Algorithm"][i]["Training_data_type"])
                data_l=len(self.dataset["Attribute_characteristics"])

                if(algo_l==2 and data_l==2):

                   if(cfg.algo["Algorithm"][i]["Training_data_type"][0]==self.dataset["Attribute_characteristics"][0] and cfg.algo["Algorithm"][i]["Training_data_type"][1]==self.dataset["Attribute_characteristics"][1]):
                     self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

                elif(algo_l==1 and data_l==1):
                     if(cfg.algo["Algorithm"][i]["Training_data_type"]==self.dataset["Attribute_characteristics"]):
                       self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

                elif(algo_l==1 and data_l==2):
                   if(cfg.algo["Algorithm"][i]["Training_data_type"]==self.dataset["Attribute_characteristics"][0]):
                      self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

                elif(algo_l==2 and data_l==1):
                   if(cfg.algo["Algorithm"][i]["Training_data_type"][0]==self.dataset["Attribute_characteristics"]):
                      self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

    return self.algo_name


  def unsupervised_algorithm_selection(self,output):
    """
        determine appropriate algorithm for unsupervised learning problem.
        :return: selected algorithm name.
    """
    self.output=output
    self.predict_value="multiple"
    obj=attr.Attribute()
    self.dataset=obj.dataset_information()
    l=len(cfg.algo["Algorithm"])
    for i in range(l):
      if(cfg.algo["Algorithm"][i]["Prediction_type"][0]==self.predict_value or cfg.algo["Algorithm"][i]["Prediction_type"][1]==self.predict_value):
        algo_l=len(cfg.algo["Algorithm"][i]["Training_data_type"])
        data_l=len(obj.dataset["Attribute_characteristics"])
        if(algo_l==2 and data_l==2):
            if(cfg.algo["Algorithm"][i]["Training_data_type"][0]==self.dataset["Attribute_characteristics"][0] and cfg.algo["Algorithm"][i]["Training_data_type"][1]==self.dataset["Attribute_characteristics"][1]):
                self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

        elif(algo_l==1 and data_l==1):
            if(cfg.algo["Algorithm"][i]["Training_data_type"]==self.dataset["Attribute_characteristics"]):
                self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

        elif(algo_l==1 and data_l==2):
            if(cfg.algo["Algorithm"][i]["Training_data_type"]==self.dataset["Attribute_characteristics"][0]):
                self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

        elif(algo_l==2 and data_l==1):
            if(cfg.algo["Algorithm"][i]["Training_data_type"][0]==self.dataset["Attribute_characteristics"]):
                self.algo_name=cfg.algo["Algorithm"][i]["Algorithm_name"]

    return self.algo_name

  def generate_algorithm_info(self,output):
    """
        generate selected algorithm and related training data set information.
        :return:
    """
    obj=attr.Attribute()
    self.db_name,self.tb_name=obj.database_info()
    self.output_attr,self.attr_no,self.attr_list=obj.attribute_info()
    u_intent=cfg.user["Sensor_name"][0]
    self.algo["Sensor_name"]=[u_intent]
    self.algo["Domain"]=[self.db_name,self.tb_name]

    if(output==1):
      self.algo["Algorithm_name"]=self.supervised_algorithm_selection(1)
      self.algo["Output_attribute"]=self.output_attr
    else:
      self.algo["Algorithm_name"]=self.unsupervised_algorithm_selection(0)
      self.algo["Output_attribute"]="none"
    self.algo["Number_of_training_attributes"]=self.attr_no
    self.algo["Training_attributes"]=self.attr_list
    print(self.algo,file=sys.stderr)
    print("Generating selected algorithm info file...",file=sys.stderr)
    with open('watch/selected_algo.json','w') as data_file:
     json.dump(self.algo,data_file)

