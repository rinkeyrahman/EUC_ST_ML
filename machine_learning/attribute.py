from __future__ import print_function
import scipy.stats as stats
from scipy.stats import chisquare
from scipy.stats import pearsonr
import pymysql
import pandas as pd
import numpy as np
import json
import sys
import config as cfg



SIGNIFICANCE_LEVEL=0.05

class Attribute:
  """
    This class maintains procedure of collecting user intention,
    dataset selection.

    Parameters
    ----------

    dataset: dict
             dataset information
    output_attr : string
                  name of output attribute
    attr_list : list
                list of selected attributes for training data set
    attr_no : int
              total number of selected attributes for training data set
    x_type : string
            data type of output attribute

  """
  def __init__(self):
    self.dataset={ "Dataset_name": "",

         "Type": "",

         "Attribute_characteristics":"",

         "Number_of_instances":"",

          "Number_of_attributes":"",

          "Missing_value":""
          }

    self.output_attr=""
    self.attr_list=[]
    self.attr_no=0



  def connect_database(self):
    """
        connect database according to selected domain.
        :return: cursor, database name and table name
    """
    self.db_name=cfg.user["Domain"][0]
    self.tb_name=cfg.user["Domain"][1]  
    db = pymysql.connect(cfg.mysql['host'],cfg.mysql['user'],cfg.mysql['password'],db=self.db_name)
    cursor = db.cursor()
    return cursor,self.db_name,self.tb_name

  def get_attribute_correlation(self,X,X_type,Y,Y_type,unique_value_x,unique_value_y):
    """
        determine correlation between output (X) and other attributes (Y) using three statistical methods.
        :return: p value
    """
    if(X_type=="categorical" and Y_type=="categorical"):
        if(unique_value_x==unique_value_y):
          print("Chisquare test...",file=sys.stderr)
          X_num=np.unique(X,return_counts=True)
          Y_num=np.unique(Y,return_counts=True)
          #print(X_num,Y_num, file=sys.stderr)
          print("Calculating p value...",file=sys.stderr)
          n=chisquare(X_num[1],Y_num[1])
          self.s=n[1]
        else:
          self.s=0
    elif(X_type=="quantitative" and Y_type=="quantitative"):
        print("Pearson's correlation...",file=sys.stderr)
        n=pearsonr(X,Y)
        print("Calculating p value...",file=sys.stderr)
        self.s=n[1]
    else:
        if(X_type=="categorical"):
              n=np.unique(X,return_counts=True)
              data1=X
              data2=Y
        else:
            n=np.unique(Y,return_counts=True)
            data1=Y
            data2=X
        #print(n,file=sys.stderr)
        var1=[]
        var2=[]
        print("One way analysis of variance...",file=sys.stderr)
        for i in range(len(data2)):
            if(n[0][1]==data1[i]):
               var1.append(data2[i])
            elif(n[0][2]==data1[i]):
              var2.append(data2[i])
        print("Calculating p value...",file=sys.stderr)
        n=stats.f_oneway(var1,var2)
        self.s=n[1]
    print("p value: ",self.s,file=sys.stderr)
    return self.s

  def determine_learning_problem(self):
      """
        determine whether the learning problem is supervised or unsupervised.
        :return: p value
      """
      self.x_type=""
      cursor,self.db_name,self.tb_name=self.connect_database()
      col="SHOW COLUMNS from %s"%(self.tb_name)
      cursor.execute(col)
      self.res=cursor.fetchall()
      keyword=[]
      s_num=cfg.user["Number_of_service"]
      for index in range(0,s_num):
            t=cfg.user["Services"][index]["Conditional_keywords"]
            keyword.append(t)
      print(keyword,file=sys.stderr)
      self.all_col={}
      print("Determining whether the learning problem is supervised or unsupervised",file=sys.stderr)
      l=len(keyword)-1
      for i in range(0,len(self.res)):
        col_name=self.res[i][0]
        self.all_col[col_name]=i
        print(col_name,file=sys.stderr)
        search="SELECT %s from %s WHERE "%(col_name,self.tb_name)
        for j in range(len(keyword)):
          if(j==l):
            search+="%s LIKE "%(col_name)
            search+= "'%"
            search+="%s"%(keyword[j])
            search+="%'"
          else:
            search+="%s LIKE "%(col_name)
            search+= "'%"
            search+="%s"%(keyword[j])
            search+="%' OR "
        cursor.execute(search)
        r=cursor.fetchall()
        if(r is not None):
          self.x_type=cfg.attr_info["Attribute_info"][i]["Type"]
          self.output_attr=col_name

          self.output=1

        else:
          self.output=0
      Attribute.x_type=self.x_type
      Attribute.output_attr=self.output_attr
      return self.output

  def supervised_attribute_set(self):
      """
        compare attribute set for supervised training data selection.
        :return:
      """
      self.x=[]
      self.d_type={}
      self.score={}
      cursor,self.db_name,self.tb_name=self.connect_database()
      print("The learning problem is supervised",file=sys.stderr)
      #type checking
      q="SELECT COUNT( DISTINCT %s )FROM %s"%(self.output_attr,self.tb_name)
      cursor.execute(q)
      unique_value=cursor.fetchall()
      self.unique_value_x=unique_value[0][0]
      Attribute.unique_value_x=self.unique_value_x
      value="SELECT %s from %s "%(self.output_attr,self.tb_name)
      cursor.execute(value)
      row=cursor.fetchall()
      for i in range(len(row)):
        t=row[i][0]
        self.x.append(t)
      x_init=pd.Series(self.x)
      type=x_init.dtype.name
      if(type=="object"):
        a=np.array(self.x)
        a_enc = pd.factorize(a)
        self.x=a_enc[0]

      print("Selecting training data set for machine learning...",file=sys.stderr)


      for i in range(0,len(self.res)):
        self.y=[]
        col_name=self.res[i][0]
        q="SELECT %s FROM %s"%(col_name,self.tb_name)
        cursor.execute(q)
        row=cursor.fetchall()
        for j in range(len(row)):
            t=row[j][0]
            self.y.append(t)
        y_init=pd.Series(self.y)
        type=y_init.dtype.name
        if(type=="object"):
          a=np.array(self.y)
          a_enc = pd.factorize(a)
          self.y=a_enc[0]
        self.y_type=cfg.attr_info["Attribute_info"][i]["Type"]
        if(self.output==1):
         if(col_name is not self.output_attr):
            print("Determining correlation between...",file=sys.stderr)
            print(col_name,"and",self.output_attr,file=sys.stderr)
            self.d_type[col_name]=self.y_type
            p="SELECT COUNT( DISTINCT %s )FROM %s"%(col_name,self.tb_name)
            cursor.execute(p)
            unique_value=cursor.fetchall()
            self.unique_value_y=unique_value[0][0]
            self.score[col_name]=self.get_attribute_correlation(self.x,self.x_type,self.y,self.y_type,self.unique_value_x,self.unique_value_y)

  def unsupervised_attribute_set(self):
      """
        compare attribute set for unsupervised training data selection.
        :return:
      """
      self.x=[]
      self.d_type={}
      self.score={}
      cursor,self.db_name,self.tb_name=self.connect_database()
      print("The learning problem is unsupervised",file=sys.stderr)
      sensor_data=cfg.user["Sensor_name"]
      sensor_data=sensor_data.replace(' ','_')
      q="SELECT COUNT( DISTINCT %s )FROM %s"%(self.output_attr,self.tb_name)
      cursor.execute(q)
      unique_value=cursor.fetchall()
      self.unique_value_x=unique_value[0][0]
      Attribute.unique_value_x=self.unique_value_x
      value="SELECT %s from %s "%(sensor_data,self.tb_name)
      cursor.execute(value)
      row=cursor.fetchall()
      for i in range(len(row)):
        t=row[i][0]
        self.x.append(t)
      x_init=pd.Series(self.x)
      type=x_init.dtype.name
      id=self.all_col[sensor_data]
      self.x_type=cfg.attr_info["Attribute_info"][id]["Type"]
      if(type=="object"):
        a=np.array(self.x)
        a_enc = pd.factorize(a)
        self.x=a_enc[0]
      print("Selecting training data set for machine learning...",file=sys.stderr)
      for i in range(0,len(self.res)):
        self.y=[]
        col_name=self.res[i][0]

        q="SELECT %s FROM %s"%(col_name,self.tb_name)
        cursor.execute(q)
        row=cursor.fetchall()
        for j in range(len(row)):
            t=row[j][0]
            self.y.append(t)
        y_init=pd.Series(self.y)
        type=y_init.dtype.name
        if(type=="object"):
          a=np.array(self.y)
          a_enc = pd.factorize(a)
          self.y=a_enc[0]
        self.y_type=cfg.attr_info["Attribute_info"][i]["Type"]

        if(col_name is not sensor_data):
             print("Determining correlation between...",file=sys.stderr)
             print(col_name,"and",sensor_data,file=sys.stderr)
             self.d_type[col_name]=self.y_type
             p="SELECT COUNT( DISTINCT %s )FROM %s"%(col_name,self.tb_name)
             cursor.execute(p)
             unique_value=cursor.fetchall()
             self.unique_value_y=unique_value[0][0]
             self.score[col_name]=self.get_attribute_correlation(self.x,self.x_type,self.y,self.y_type,self.unique_value_x,self.unique_value_y)


  def generate_attribute_set(self):
     """
        select training dataset by comparing p value with significance level.
        :return:
      """
     cursor,self.db_name,self.tb_name=self.connect_database()
     count=0
     Attribute.attr_dtype_list=[]
     select="SELECT "
     for key in self.score:
       count=count+1
       if(self.score[key]>=SIGNIFICANCE_LEVEL):
          self.attr_no=self.attr_no+1
          self.attr_list.append(key)
          Attribute.attr_dtype_list.append(self.d_type[key])
          select+="%s,"%key
          last_key=key

     select+="%s from %s "%(last_key,self.tb_name)
     print(select, file=sys.stderr)
     cursor.execute(select)
     s_res=cursor.fetchall()
     Attribute.attr_list=self.attr_list
     Attribute.attr_no=self.attr_no
     print("Selected attribute set:  ",Attribute.attr_list, file=sys.stderr)


  def dataset_information(self):
     """
        generate selected data set information.
        :return: data set information.
     """
     cursor,self.db_name,self.tb_name=self.connect_database()
     #dataset info
     self.dataset["Dataset_name"]=self.tb_name
     self.dataset["Type"]=self.db_name

     cat=0
     qn=0
     for i in range(len(Attribute.attr_dtype_list)):
      if(Attribute.attr_dtype_list[i]=="categorical"):
        cat=1
      elif(Attribute.attr_dtype_list[i]=="quantitative"):
        qn=1

     if(cat==1 and qn==1):
        self.dataset["Attribute_characteristics"]=["categorical","quantitative"]
     elif(cat==1 and qn==0):
        self.dataset["Attribute_characteristics"]=["categorical"]
     else:
        self.dataset["Attribute_characteristics"]=["quantitative"]
     q1="SELECT count(*) from %s"%self.tb_name
     cursor.execute(q1)
     i_res=cursor.fetchall()
     self.dataset["Number_of_instances"]=i_res[0][0]
     #self.dataset["Number_of_attributes"]=len(self.res)
     self.dataset["Missing_value"]=0

     with open('info/selected_dataset_info.json', 'w') as f:
       json.dump(self.dataset,f)
     return self.dataset

  def xtype(self):
     """
        :return: output attribute data type.
     """
     return Attribute.x_type

  def unique_x(self):
     """
        :return: unique values of output attribute(x).
     """
     return Attribute.unique_value_x

  def attribute_info(self):
      """
        :return: output attribute name, selected training attribute list, number of selected attribute.
      """
      return Attribute.output_attr,Attribute.attr_no,Attribute.attr_list

  def database_info(self):
      """
        collect database information.
        :return: database information.
      """
      cursor,self.db_name,self.tb_name=self.connect_database()
      return self.db_name,self.tb_name



