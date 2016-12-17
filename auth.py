import uuid
from functools import wraps

from flask import Response, request
from models.users import User
from utils import json_encode


def authorize(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return wrapper

def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.q.get(username=username)
    if user.check_password(password):
        return Response(json_encode({"token": user.token}))
    else:
        return Response(status=403)

def whoami():
    token = request.args.get("token")
    if not token:
        return Response(status=403)
    user = User.q.get(token=token)
    if user:
        return Response(json_encode(user.serialize()))
    else:
        return Response(status=403)

def user_exists(username, email):
    user = User.q.get(username=username)
    if user:
        return True
    user = User.q.get(email=email)
    if user:
        return True



def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    zipcode = data.get("zipcode")
    if username and password and email and zipcode:
        if user_exists(username, email):
            return Response(json_encode({"message": "User already exists with this username or email"}),
                            status=400)
        data = {'username': username,
                'password': password,
                'email': email,
                'zipcode': zipcode}
        new_user = User(**data)
        token = "tok-%s" % uuid.uuid4().hex
        new_user.save()
        new_user.set_token(token)
        new_user.set_password(password)
        return Response(json_encode({'token': token}))
    return Response(status=200)

def logout():
    return Response(status=200)