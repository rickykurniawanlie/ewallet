from models import db
from models import User

user_input = ""
while user_input != "quit":
  user_input = input("Input name or npm you wanna delete: ")
  if (user_input == "quit"):
    print(User.query.all())
  elif (user_input == "all"):
    print(User.query.all())
  elif (user_input.isdigit()):
    user = User.query.filter_by(user_id = user_input).first()
    db.session.delete(user)
    db.session.commit()
  else:
    user = User.query.filter_by(name = user_input).first()
    db.session.delete(user)
    db.session.commit()
  print ("Finished deleting")