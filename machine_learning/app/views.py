from __future__ import print_function
from flask import render_template, flash, redirect
from flask import Flask, jsonify, g
from app import app
from forms import LoginForm
import json
import sys
from flask import request
import pymysql


'''
@app.route('/base', methods=['GET'])
def base():
    pymysql.install_as_MySQLdb()
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="rest")

    cursor = db.cursor()
    cursor.execute("SELECT fname FROM forms")
    providers=cursor.fetchall()
    p=[]
    for i in range(len(providers)):
     print(providers[i][0],file=sys.stderr)
     p.append(providers[i][0])
    ret_data = {"value": request.args.get('click')}
    with open('data.txt', 'w') as outfile:
      json.dump(ret_data, outfile)
    db.close()
    return render_template("base.html",providers=providers)


'''
@app.route('/form', methods=['GET', 'POST'])
def form():

      with open('selected_algo.json') as data_file:
          selected= json.load(data_file)
      attr_no=selected["Number_of_training_attributes"]
      q=[]
      for i in range(attr_no):
       s=selected["Training_attributes"][i]
       s=s.replace('_',' ')
       if (s!= selected["Sensor_name"][0]):
          s1=s.upper()
          q.append(s1)

      return render_template('form.html',
                           title='Form',
                           q=q)

@app.route('/success', methods=['GET','POST'])
def success():

    if request.method == 'POST':
        with open('selected_algo.json') as data_file:
          selected= json.load(data_file)
        result=request.form
        dict={}
        attr_no=selected["Number_of_training_attributes"]
        for i in range(attr_no):
          s=selected["Training_attributes"][i]
          s=s.replace('_',' ')
          if (s!= selected["Sensor_name"][0]):
             s1=s.upper()
             dict[s1]=result[s1]
        with open('user_info.json', 'w') as outfile:
          json.dump(dict, outfile)
        return json.dumps({'message':'User created successfully !'})

