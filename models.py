import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

file_path = os.path.abspath(os.getcwd())+"/ewallet.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
  user_id = db.Column(db.String(80), primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  saldo = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.name