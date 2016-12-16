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
    username = request.data.get("username")
    password = request.data.get("password")
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
        return Response(user.serialize())
    else:
        return Response(status=403)

def register():
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    zipcode = request.data.get("zipcode")
    if username and password and email and zipcode:
        data = {'username': username,
                'password': password,
                'email': email,
                'zipcode': zipcode}
        new_user = User(**data)
        token = "tok-%s" % uuid.uuid4().hex
        new_user.save()
        new_user.set_token(token)
        return Response(json_encode({'token': token}))
    return Response(status=200)

def logout():
    return Response(status=200)