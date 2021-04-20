import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__= 'users'

    id= db.Column(db.Integer, primary_key= True)
    username= db.Column(db.String(80)) #limit the size of text
    password= db.Column(db.String(80))

    def __init__(self, username, password): # as id is a primary key, it will be automatically assigned, no need to give id in object
        self.username= username
        self.password= password

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
        # connection= sqlite3.connect('data.db')
        # cursor= connection.cursor()
        #
        # query= "SELECT * FROM users WHERE username=?"
        # result= cursor.execute(query,(username,))  #parameter always have to be a tuple
        # row= result.fetchone()  # returns the first row, returns None if empty
        #
        # if row is not None:
        #     # user = cls(row[0],row[1],row[2])    alternative below
        #     user = cls(*row)
        # else:
        #     user= None
        #
        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))  # parameter always have to be a tuple
        # row = result.fetchone()  # returns the first row, returns None if empty
        #
        # if row is not None:
        #     # user = cls(row[0],row[1],row[2])    alternative below
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
