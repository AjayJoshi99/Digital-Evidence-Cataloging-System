from flask import Blueprint, request, redirect, url_for, flash, render_template
from pymongo import MongoClient

user_blueprint = Blueprint('user', __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']
users_collection = db['User_Login'] 

@user_blueprint.route('/add', methods=['POST'])
def add_user():
  error = ""
  username = request.form.get('username')
  password = request.form.get('password')
  if users_collection.find_one({"username": username}):
    error = "User already exists"
  else:
    users_collection.insert_one({"username": username, "password": password})
    error = f"User '{username}' added successfully"
  return render_template("AdminHome.html", error = error) 


@user_blueprint.route('/delete', methods=['POST'])
def delete_user():
  error = ""
  username = request.form.get('username')
  user = users_collection.find_one({"username": username})
  if not user:
    error = "User not found"
  else:
    users_collection.delete_one({"username": username})
    error = f"User '{username}' deleted successfully"
  return render_template("AdminHome.html", error = error) 
