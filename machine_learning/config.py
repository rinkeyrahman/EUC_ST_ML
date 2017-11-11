import json

mysql = {'host': 'localhost',
         'user': 'root',
         'password': ''
         }

with open('watch/user_intention.json') as data_file:
         user= json.load(data_file)

with open('info/algorithm_info.json') as data_file:
         algo= json.load(data_file)

with open('info/attribute_info.json') as data_file:
         attr_info= json.load(data_file)
