import datetime
from flask import Response, request
from utils import json_encode
from flask.views import MethodView
from models.listings import Listing
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
        created_at = datetime.datetime.now()
        zipcode = user.zipcode
        listing = Listing(text=text,
                          owner=owner,
                          created_at=created_at,
                          zipcode=zipcode)
        listing.save()
        return Response(status=201)