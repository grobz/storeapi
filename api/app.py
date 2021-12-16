from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import os
from mergedeep import merge, Strategy

app = Flask(__name__)

mongo_dbname = os.getenv("MONGO_DB", "restdb")
mongo_uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")

app.config["MONGO_DBNAME"] = mongo_dbname
app.config["MONGO_URI"] = f"{mongo_uri}/{mongo_dbname}"

mongo = PyMongo(app)


def saved_format(req):
    if "key" in req and "data" in req and "tags" in req:
        return {"key": req["key"], "data": req["data"], "tags": req["tags"]}
    else:
        return req


@app.route("/api/get", methods=["GET"])
def get_all_saved():
    saved = mongo.db.saved
    output = []
    for s in saved.find():
        output.append(saved_format(s))
    return jsonify({"result": output})


@app.route("/api/get/<key>", methods=["GET"])
def get_one_saved(key):
    saved = mongo.db.saved
    s = saved.find_one({"key": key})
    if not s:
        output = {"No such key"}
    return jsonify({"result": saved_format(s)})


@app.route("/api/add", methods=["POST"])
def add_saved():
    saved = mongo.db.saved
    req_json = request.get_json()
    if "key" not in req_json:
        return ("ERROR empty key", 400)
    if "tags" not in req_json:
        req_json["tags"] = {}
    saved.delete_one({"key": req_json["key"]})
    saved_id = saved.insert(req_json)
    new_saved = saved.find_one({"_id": saved_id})
    return jsonify({"result": saved_format(new_saved)})


@app.route("/api/update", methods=["PUT"])
def update_saved():
    saved = mongo.db.saved
    req_json = request.get_json()
    if "key" not in req_json:
        return ("ERROR empty key", 400)
    if "tags" not in req_json:
        req_json["tags"] = {}
    fo = saved.find_one({"key": req_json["key"]})
    saved_id = ""
    if not fo:
        saved_id = saved.insert(req_json)
    else:
        merge(fo, req_json, strategy=Strategy.REPLACE)
        saved.delete_one({"key": req_json["key"]})
        saved_id = saved.insert(fo)
    new_saved = saved.find_one({"_id": saved_id})
    return jsonify({"result": saved_format(new_saved)})


if __name__ == "__main__":
    app.run(debug=True)
