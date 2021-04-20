from models.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username,password):
    # The authenticate function is used to authenticate a user.
    # That means, when a user gives us their username and password, what data we want to put into the JWT.
    # Remember, the data we put into the JWT will come back to us when the user sends it with each request.

    user= UserModel.find_by_username(username)  # using get function we can return a default value in case no match
    if user and safe_str_cmp(user.password,password): # this function helps if the strings are encoded
        return user

def identity(payload):
    # The identity function is used when we receive a JWT.
    # In any of our endpoints (except the /auth endpoint) the user can send us a JWT alongside their data.
    # They will do this by adding a header to their request: Authorization: JWT <JWT_VALUE_HERE>
    user_id= payload['identity']
    # The payload['identity'] contains the user's id property that we saved into the JWT when we created it.
    return UserModel.find_by_id(user_id)
