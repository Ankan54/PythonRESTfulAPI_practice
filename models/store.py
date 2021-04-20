from db import db

class StoreModel(db.Model): #to map object with database
    __tablename__= 'stores'

    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100))

    items= db.relationship('ItemModel', lazy= 'dynamic') # back process for what we did for ItemModel class
    # lazy= dynamic will stop sqlalchemy to go into items table everytime we create a new store to
    # look for items for that store, now we will access items table through the JSON() method only

    def __init__(self, name):
        self.name= name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} #self.items has become a query builder

    def save_to_db(self):  # it will create and update through the same code
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * from __tablename__ where name=name LIMIT 1
