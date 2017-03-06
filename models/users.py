import bcrypt
from geohash import encode
from config import CRYPTING_PASSWORD
from models.base import BaseModel


class User(BaseModel):

    __collection_name__ = 'users'

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.latitude = kwargs.get("latitude")
        self.longitude = kwargs.get("longitude")
        self.geohash = kwargs.get("geohash")
        self.token = None
        super(User, self).__init__(*args, **kwargs)

    def set_email(self, email):
        User.q.update({"_id": self._id},
                      {"$set": {"email": email}})

    def set_token(self, token):
        User.q.update({"_id": self._id},
                      {"$set": {"token": token}})

    def set_password(self, password):
        password = password.encode("utf-8")
        hash = bcrypt.hashpw(b"%s" % password, CRYPTING_PASSWORD)
        User.q.update({"_id": self._id},
                      {"$set": {"password": hash}})

    def set_geohash(self, latitude, longitude, precision=7):
        geohash = encode(latitude, longitude, precision=precision)
        self.geohash = geohash
        User.q.update({"_id": self._id},
                      {"$set": {"geohash": geohash}})

    def check_password(self, password):
        password = password.encode("utf-8")
        hash = bcrypt.hashpw(b'%s' % password, CRYPTING_PASSWORD)
        return hash == self.password

    def serialize(self):
        return {'id': self.id,
                "email": self.email,
                "geohash": self.geohash,
                "username": self.username
                }

    def save(self):
        if self._id:
            User.q.update({"_id": self._id},
                          {"$set": self.serialize()})
        else:
            self._id = User.q.insert(self.serialize())
        return self._id