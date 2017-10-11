from flask import Flask, request, Response
from models import User
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import socket
import json
import yaml

ip_address = str(socket.gethostbyname(socket.gethostname()))
file_path = os.path.abspath(os.getcwd())+"/ewallet.db"
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
      data = json.loads(request.data.decode())
      user_id = data['user_id']
      name = data['nama']
      register_return = data['registerReturn']
      new_user = User(user_id=user_id, name=name)
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

def isQuorum():
  return True

if __name__ == '__main__':
  app.run(ip_address, port=5000)