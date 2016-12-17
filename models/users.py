import bcrypt
from config import CRYPTING_PASSWORD
from models.base import BaseModel


class User(BaseModel):

    __collection_name__ = 'users'

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.zipcode = kwargs.get("zipcode")
        self.token = None
        super(User, self).__init__(*args, **kwargs)


    def set_email(self, email):
        User.q.database.users.update({"_id": self._id},
                        {"$set": {"email": email}})

    def set_token(self, token):
        User.q.database.users.update({"_id": self._id},
                        {"$set": {"token": token}})

    def set_password(self, password):
        password = password.encode("utf-8")
        hash = bcrypt.hashpw(b"%s" % password, CRYPTING_PASSWORD)
        User.q.database.users.update({"_id": self._id},
                         {"$set": {"password": hash}})

    def check_password(self, password):
        password = password.encode("utf-8")
        hash = bcrypt.hashpw(b'%s' % password, CRYPTING_PASSWORD)
        return hash == self.password

    def serialize(self):
        return {'id': self.id,
                "email": self.email,
                "username": self.username}


    def save(self):
        if self._id:
            User.q.database.users.update({"_id": self._id},
                            {"$set": self.serialize()})
        else:
            self._id = User.q.database.users.insert(self.serialize())
        return self._id