import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required= True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already exists'}, 400

        #user= UserModel(data['username'],data['password'])
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'user created successfully'}, 201

        # connection= sqlite3.connect('data.db')
        # cursor= connection.cursor()
        # query= "INSERT INTO users VALUES (NULL, ?,?)"
        # cursor.execute(query,(data['username'],data['password'])) #need to be a tuple
        #
        # connection.commit()
        # connection.close()
