from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):    
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, index=True, unique=False) 
	email = db.Column(db.String(20), index=True, unique=True)
	password = db.Column(db.String(16), index=False, unique=False)
