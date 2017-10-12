import requests
import json
from models import User

port = 80

def ping():
  ip_address = input("Input IP to ping on: ")
  url = 'http://'+ip_address+':' + str(port) + '/ewallet/ping'
  r = requests.post(url).text
  r_json = json.loads(r)
  print ('return: ' + str(r_json['pong']))

def get_saldo():
  ip_address = input("Input IP to get saldo from: ")
  all_user = User.query.all()
  print ('Select your user id from your database')
  for index, user in enumerate(all_user):
    index += 1
    print (str(index) + '. ' + str(user.name) + ' : ' + str(user.user_id))
  user_id = input('Please input the user id: ')
  url = 'http://'+ip_address+':' + str(port) + '/ewallet/getSaldo'
  payload = {"user_id": str(user_id)}
  r = requests.post(url, data=json.dumps(payload)).text
  r_json = json.loads(r)
  nilai_saldo = r_json['nilai_saldo']
  if (nilai_saldo == -1):
    try:
      url = 'http://'+ip_address+':' + str(port) + '/ewallet/register'
      user_name = User.query.filter_by(user_id=user_id).first().name
      payload = {"user_id": str(user_id), "nama": str(user_name)}
      r = requests.post(url, data=json.dumps(payload)).text
      r_json = json.loads(r)
      status = r_json['status_register']
      if (status == -2):
        print ('Quorum not enough dari register')
      elif (status == -4):
        print ('Sorry.. Database error dari register')
      elif (status == -99):
        print ('Unknown problem Captain!!! dari register')
      else:
        print ("Successfully registered to: " + ip_address)
    except Exception as ex:
      print (ex)
  elif (nilai_saldo == -2):
    print ('Quorum not enough dari getsaldo')
  elif (nilai_saldo == -4):
    print ('Sorry.. Database error dari getsaldo')
  elif (nilai_saldo == -99):
    print ('Unknown problem Captain!!! dari getsaldo')
  else:
    print ('Nilai saldo di ' + str(ip_address) + ' : ' + str(r_json['nilai_saldo']))

user_input = ""
while user_input != "quit":
  user_input = input("User input: ")
  if user_input == "ping":
    ping()
  elif user_input == "getsaldo":
    get_saldo()
  else:
    print ("Invalid input")
    