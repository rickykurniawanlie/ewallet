from flask import Flask, request, Response
from models import User
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import socket
import requests
import json
import yaml

ip_address = '0.0.0.0'
port = 5000
file_path = os.path.abspath(os.getcwd())+"/ewallet.db"
list_api = 'http://152.118.31.2/list.php'
yaml_file = sys.argv[1]
with open(yaml_file, 'r') as ymlfile:
  cfg = yaml.load(ymlfile)
base_path = cfg['basePath']
prod_json = str(cfg['produces'][0])
prod_xml = str(cfg['produces'][1])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.debug = True

@app.route(base_path + 'ping', methods=['POST'])
def ping():
  response = {}
  try:
    response['pong'] = 1
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
  except Exception as ex:
    print (ex)
    response['pong'] = -99
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)

@app.route(base_path + 'register', methods=['POST'])
def register():
  response = {}
  try:
    if (isQuorum()):
      # data = str(json.loads(request.get_json(force=True)))
      data = request.get_json(force=True)
      user_id = data['user_id']
      name = data['nama']
      new_user = User(user_id=user_id, name=name, saldo=0)
      try:
        db.session.add(new_user)
        db.session.commit()
        response['status_register'] = 1
        return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
      except Exception as ex:
        print (ex)
        response['status_register'] = -4
        return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
    else:
      response['status_register'] = -2
      return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
  except Exception as ex:
    print (ex)
    response['status_register'] = -99
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)

@app.route(base_path + 'getSaldo', methods=['POST'])
def getSaldo():
  response = {}
  try:
    if (isQuorum()):
      # data = json.loads(request.get_json(force=True).decode())
      data = request.get_json(force=True)
      user_id = data['user_id']
      user = User.query.filter_by(user_id = user_id).first()
      if (user == None):
        response['nilai_saldo'] = -1
        return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
      else:
        try:
          response['nilai_saldo'] = user.saldo
          return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
        except Exception as ex:
          print (ex)
          response['nilai_saldo'] = -4
          return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
    else:
      response['nilai_saldo'] = -2
      return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
  except Exception as ex:
    print (ex)
    response['nilai_saldo'] = -99
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)

def isQuorum():
  # r = requests.get(list_api).text
  # r_json = json.loads(r)
  # ================================
  # count = 0
  # with open('test.json') as data_file:    
  #   list_json = json.load(data_file)  
  # for entry in list_json:
  #   try:
  #     url = 'http://'+entry['ip']+':' + str(port) + '/ewallet/ping'
  #     r = requests.post(url).text
  #     r_json = json.loads(r)
  #     print (r_json['pong'])
  #     # print (url)
  #   except Exception as ex:
  #     print (ex)
  return True

if __name__ == '__main__':
  app.run(ip_address, port=port)