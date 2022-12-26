from flask import Flask,jsonify,current_app
from pymongo import MongoClient
from flask import request


import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

client = MongoClient("mongodb://root:example@db:27017")
db = client.recipes

@app.route('/')
def hello():
	return current_app.send_static_file("index.html")

@app.route("/recipe", methods=['GET'])
def list_recipe():
    cursor = db.recipe.find()
    return JSONEncoder().encode(list(cursor))

@app.route("/recipe", methods=['POST'])
def add_recipe():
    # request.get_data(as_text=True) if body is raw data
    db.recipe.insert_one(dict(request.form))
    return "OK"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
