from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt, requests, json, os, datetime, time, random

# Flask CRUD API

# Create a Flask App
app = Flask(__name__)
api = Api(app)
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017", connect=True)
db = client.test
# Create a collection
users = db.users
# Create a Schema for user
class User(Resource):
    def post(self):
        # Get data from the request
        data = request.get_json()
        # Check if the user already exists
        if users.find_one({"username": data["username"]}):
            return {"message": "User already exists"}, 400
        # Hash the password
        hashed_password = bcrypt.hashpw(data["password"].encode("utf8"), bcrypt.gensalt())
        # Insert the user into the database
        users.insert({"username": data["username"], "password": hashed_password})
        return {"message": "User created successfully"}, 201
    def get(self):
        # Get data from the request
        data = request.get_json()
        # Check if the user already exists
        if not users.find_one({"username": data["username"]}):
            return {"message": "User does not exist"}, 400
        # Get the hashed password
        hashed_password = users.find_one({"username": data["username"]})["password"]
        # Check if the password is correct
        if bcrypt.hashpw(data["password"].encode("utf8"), hashed_password) != hashed_password:
            return {"message": "Incorrect password"}, 400
        # Generate a token
        token = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(50)])
        # Insert the token into the database
        users.update_one({"username": data["username"]}, {"$set": {"token": token}})
        return {"token": token}, 200
