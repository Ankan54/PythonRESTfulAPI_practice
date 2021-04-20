from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='price can not be empty')
    parser.add_argument('store_id', type=int, required=True, help='every item needs a store id')

    @jwt_required()
    def get(self,name):
        try:
            item= ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred while finding the item'}, 500 #internal server error
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404


    def post(self,name):
        try:
            item= ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred while finding the item'}, 500

        if  item:
            return {'message': 'item already exists'}, 400
        #get request data
        request_data = Item.parser.parse_args()
        #item= {'name': name, 'price': request_data['price']}
        #item= ItemModel(name,request_data['price'],request_data['store_id'])
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while creating the record'}, 500

        return {'message': 'item created successfully',
                'name': item.name,
                'price': item.price,
                'store_id': item.store_id}, 201

    def delete(self,name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred while finding the item'}, 500

        if  item is None:
            return {'message': 'item \'{}\' doesn\'t exist'.format(name)}, 400

        try:
            item.delete_from_db()
        except:
            return {'message': 'An error occurred while deleting the record'}, 500

        return {'message': 'item \'{}\' is deleted'.format(name)}

    def put(self,name):
        # request_data= request.get_json()
        request_data= Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred while finding the item'}, 500

        if item is None:
            #new_item = {'name': name, 'price': request_data['price']}
            #new_item= ItemModel(name,request_data['price'],request_data['store_id'])
            new_item = ItemModel(name, **request_data)
            try:
                new_item.save_to_db()
                return {'message': 'item created successfully',
                        'name': new_item.name,
                        'price': new_item.price,
                        'store_id': new_item.store_id}, 201
            except:
                return {'message': 'An error occurred while creating the item'}, 500
        else:
            #updated_item = {'name': row[0], 'price': request_data['price']}
            #updated_item= ItemModel(item.name, request_data['price']) # making object of item as per Item model
            try:
                #updated_item.update_item()
                item.price= request_data['price']
                item.store_id= request_data['store_id']
                item.save_to_db()
                return {'message': 'item updated successfully',
                        'name': item.name,
                        'price': item.price,
                        'store_id': item.store_id}, 201
            except:
                return {'message': 'An error occurred while updating the item'}, 500


class ItemList(Resource):
    def get(self):
        # connection= sqlite3.connect('data.db')
        # cursor= connection.cursor()
        # query= "SELECT * FROM items"
        # result= cursor.execute(query)
        # items=[]
        # for row in result:
        #     items.append({'name':row[1], 'price':row[2]})
        # connection.close()
        # return {'items':items}
        return {'items': [item.json() for item in ItemModel.query.all()]}
