from flask import Flask, render_template, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

#Model
class User(db.Model):    
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, index=True, unique=False) 
	email = db.Column(db.String(20), index=True, unique=True)
	password = db.Column(db.String(16), index=False, unique=False)
    
#JWT Middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
               auth_header = request.headers['Authorization']
               if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]
        if not token:
             return jsonify({'message': 'Token in missing'}), 401
        
        try:
             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
             current_user = User.query.get(data['id'])
        except Exception:
             return jsonify({'message': 'Token is invalid or expired'})
        
        return f(current_user, *args, **kwargs)
     
    return decorated
             


with app.app_context():
    db.create_all()



#API Endpoints
@app.route('/', methods=['GET'])
def home():
     return jsonify({'success': True})

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({'success': True, 'id': current_user.id, 'email': current_user.email})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not check_password_hash(user.password, data.get('password')):
         return jsonify({'message': 'Invalid email or password'})
    
    token = jwt.encode({
         'id': user.id,
         'email': user.email,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'success': True, 'token': token})


@app.route('/register', methods=['POST'])
def register():
    data= request.json #data that user gives in a json format
    if not data.get('email') or not data.get('password'):
         return jsonify({'message': 'Email and password are required'})
    
    if User.query.filter_by(email=data['email']).first():
         return jsonify({'message': 'User already registered'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'User registered successfully'})


if __name__ == '__main__':
    app.run(debug=True)
#https://inloop.github.io/sqlite-viewer/
#view database
