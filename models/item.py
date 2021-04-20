#import sqlite3
from db import db

class ItemModel(db.Model): #to map object with database
    __tablename__= 'items'

    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100))
    price= db.Column(db.Float(precision=2))
    store_id= db.Column(db.Integer, db.ForeignKey('stores.id'))

    store= db.relationship('StoreModel') # it joins the tables based on the foreign key

    def __init__(self, name, price, store_id):
        self.name= name
        self.price= price
        self.store_id= store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    def save_to_db(self):  # it will create and update through the same code
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = 'INSERT INTO items VALUES (?,?)'
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()

    # def update_item(self, price):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     query = 'UPDATE items SET price=? WHERE name=?'
    #     cursor.execute(query, (price, self.name))
    #
    #     connection.commit()
    #     connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = 'DELETE FROM items WHERE name=? collate nocase'
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * from __tablename__ where name=name LIMIT 1
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items where name=? collate nocase"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row)
        # return row
