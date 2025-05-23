from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class User(db.Model):    
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, index=True, unique=False) 
	email = db.Column(db.String(20), index=True, unique=True)
	password = db.Column(db.String(16), index=False, unique=False)
