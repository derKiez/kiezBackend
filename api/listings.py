import datetime

from bson import ObjectId
from flask import Response, request
from utils import json_encode
from flask.views import MethodView
from models.listings import Listing, ListingComment
from auth import authorize


class ListingsView(MethodView):

    @authorize
    def get(self):
        zipcode = request.user.zipcode
        limit = request.args.get("limit", 20)
        offset = request.args.get("offset", 0)
        if not zipcode:
            return Response(status=400)
        listings = Listing.q.filter({"zipcode": zipcode})\
            .skip(offset)\
            .limit(limit)\
            .sort("created_at", -1).all()

        listings = list(listings)

        has_more = len(listings) >= 20
        offset = None
        if listings:
            offset = listings[-1]._id
        meta = {"next_offset": offset, "has_more": has_more}
        response_body = {"listings": [i.serialize() for i in listings],
                         "meta": meta}
        return Response(json_encode(response_body))

    @authorize
    def post(self):
        user = request.user
        data = request.json
        text = data.get("text")
        owner = request.user.serialize()
        zipcode = user.zipcode
        listing = Listing(text=text,
                          owner=owner,
                          zipcode=zipcode)
        listing.save()
        return Response(status=201)


class CommentListView(MethodView):

    @authorize
    def get(self, listing_id):
        listing = Listing.q.get(_id=ObjectId(listing_id))
        limit = request.args.get("limit", 20)
        offset = request.args.get("offset", 0)

        if not listing:
            return Response(status=404)

        listing_comments = ListingComment.q.filter(
            {"listing.id": ObjectId(listing_id)})\
            .skip(offset)\
            .sort("-created_at")\
            .limit(limit)\
            .all()

        comments = list(listing_comments)
        has_more = len(comments) >= 20
        offset = None
        if comments:
            offset = comments[-1]._id
        meta = {"next_offset": offset, "has_more": has_more}
        response_body = {"comments": [i.serialize() for i in comments],
                         "meta": meta}
        return Response(json_encode(response_body))


    @authorize
    def post(self, listing_id):
        listing = Listing.q.get(_id=ObjectId(listing_id))
        if not listing:
            return Response(status=404)
        data = request.json
        text = data.get("text")
        owner = request.user.serialize()

        comment = ListingComment(text=text,
                                 listing=listing.serialize(),
                                 owner=owner)
        comment.save()
        return Response(status=201)