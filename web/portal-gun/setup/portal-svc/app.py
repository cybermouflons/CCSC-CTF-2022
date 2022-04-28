import dataclasses
import json
from flask import Flask, Response, request
from pkg_resources import require

import pymongo
import json

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://portaldb:27017")
db = client.portal

@dataclasses.dataclass
class Location:
    name: str
    type: str
    dimension: str

@app.route('/locations', methods=["GET"])
def locations():
    return Response(json.dumps([loc["name"] for loc in db.locations.find({})]), 200)

@app.route('/portal', methods=["POST"])
def portal():
    data = request.get_json(force=True)
    base_command = {"find": "locations"} # Make sure we are using "locations". TODO: Ensure that "flag" collection is protected.
    command = {**base_command, **data}
    try:
        if results := db.command(command)["cursor"]["firstBatch"]:
            location_obj = Location(name=results[0]["name"], type=results[0]["type"], dimension=results[0]["dimension"])
            return Response(json.dumps(dataclasses.asdict(location_obj)), 200)
        else:
            return Response(json.dumps({"error": "Not found"}), 404)
    except pymongo.errors.OperationFailure as e:
        return Response(json.dumps({"error": e.args[0]}), 500)
