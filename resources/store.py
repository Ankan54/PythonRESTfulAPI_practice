from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name', type=float, required=True, help='price can not be empty')
    # parser.add_argument('store_id', type=int, required=True, help='every item needs a store id')

    def get(self,name):
        store= StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'store {} does not exist'.format(name)}, 404
        return store.json(),200

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': 'store {} already exists'.format(name)}, 400
        store= StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while deleting store'}, 500

        return {'message': 'store created successfully',
                'name': store.name},201


    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'store {} does not exist'.format(name)}, 400
        try:
            store.delete_from_db()
        except:
            return {'message': 'An error occurred while deleting store'}, 500

        return {'message': 'store {} deleted successfully'.format(name)},200


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda store: store.json(), StoreModel.query.all()))}
