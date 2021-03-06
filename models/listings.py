from models.base import BaseModel
import datetime

class Listing(BaseModel):

    __collection_name__ = 'listings'

    def __init__(self, *args, **kwargs):
        self.text = kwargs.get("text")
        self.owner = kwargs.get("owner")
        self.created_at = kwargs.get("created_at")
        self.zipcode = kwargs.get("zipcode")
        super(Listing, self).__init__(*args, **kwargs)

    def serialize(self):
        return {"id": self._id,
                "text": self.text,
                "owner": self.owner,
                "zipcode": self.zipcode,
                "created_at": self.created_at}

    def save(self):
        if self._id:
            Listing.q.update({"_id": self._id},
                             {"$set": self.serialize()})
        else:
            self._id = Listing.q.insert(self.serialize())
            self.created_at = datetime.datetime.utcnow()
        return self._id


class ListingComment(BaseModel):

    __collection_name__ = "listing_comments"

    def __init__(self, *args, **kwargs):
        self.text = kwargs.get("text")
        self.is_private = kwargs.get("is_private")
        self.owner = kwargs.get("owner")
        self.is_private = kwargs.get("is_private")
        self.parent_id = kwargs.get("parent")
        self.listing = kwargs.get("listing")
        self.parent = kwargs.get("parent")
        self.created_at = kwargs.get("created_at")
        super(ListingComment, self).__init__(*args, **kwargs)

    def serialize(self):
        return {"id": self._id,
                "is_private": self.is_private,
                "parent": self.parent,
                "text": self.text,
                "owner": self.owner,
                "listing": self.listing,
                "children": self.children,
                "created_at": self.created_at}

    def save(self):
        if self._id:
            ListingComment.q.update({"_id": self._id},
                                    {"$set": self.serialize()})
        else:
            self._id = ListingComment.q.insert(self.serialize())
            self.created_at = datetime.datetime.utcnow()
        return self._id

    @property
    def children(self):
        children_comments = ListingComment.q.filter({"parent_id": self._id}).all()
        return [comment.serialize() for comment in children_comments]