#conectando a BBDD

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warnings
db = SQLAlchemy(app)

#declaring the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    title = db.Column(db.String(80), index = True, unique = True) # book title
    #Checkpoint #1: insert your code here
    author_surname = db.Column(db.String(80), index = True, unique = False) #author surname
    month = db.Column(db.String(20), index = True, unique = False) #the month of book suggestion
    year = db.Column(db.Integer, index = True, unique = False) #the year of book suggestion
    author_name = db.Column(db.String(50), index = True, unique = False)
    
    #Get a nice printout for Book objects
    def __repr__(self):
        return "{} in: {},{}".format(self.title, self.month,self.year)


@app.route('/')
@app.route('/home')
def home():
    return "Congrats! You have just made your first Flask-SQLAlchemy model declaration!"


'''

When you ran your application in the previous exercises you might have realized that there is no database file created in the application folder. The reason is simple: we need to explicitly initialize the database according to the models declared.

We can initialize our database in two ways:

1: Using the interactive Python shell.

    In the command-line terminal, navigate to the application folder and enter Python’s interactive mode:

$ python3

    Import the database instance db from app.py:

>>> from app import db

(this assumes the application file is called app.py) *Create all database tables according to the declared models:

>>> db.create_all()

2: From within the application file.

    After all the models have been specified the database is initialized by adding db.create_all() to the main program. The command is written after all the defined models.

The result of db.create_all() is that the database schema is created representing our declared models. After running the command, you should see your database file in the path and with the name you set in the SQLALCHEMY_DATABASE_URI configuration field.
'''