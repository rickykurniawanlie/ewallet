from flask import Flask, request, Response
import sys
import socket
import json
import yaml

ip_address = str(socket.gethostbyname(socket.gethostname()))
yaml_file = sys.argv[1]
with open(yaml_file, 'r') as ymlfile:
  cfg = yaml.load(ymlfile)
base_path = cfg['basePath']
prod_json = str(cfg['produces'][0])
prod_xml = str(cfg['produces'][1])

app = Flask(__name__)
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
    data = json.loads(request.data.decode())
    user_id = data['user_id']
    name = data['nama']
    register_return = data['registerReturn']
    response['status_register'] = 1
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)
  except Exception as ex:
    print (ex)
    response['status_register'] = -99
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200, mimetype=prod_json)



if __name__ == '__main__':
  app.run(ip_address, port=8080)