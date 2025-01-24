from flask import Blueprint, request, redirect, url_for, flash, render_template
from pymongo import MongoClient

user_blueprint = Blueprint('user', __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']
users_collection = db['User_Login'] 

@user_blueprint.route('/add', methods=['POST'])
def add_user():
  username = request.form.get('username')
  password = request.form.get('password')
  if users_collection.find_one({"username": username}):
    flash("User already exists", "error")
  else:
    users_collection.insert_one({"username": username, "password": password})
    flash(f"User '{username}' added successfully", "success")
  return render_template("AdminHome.html") 


@user_blueprint.route('/delete', methods=['POST'])
def delete_user():
  username = request.form.get('username')
  user = users_collection.find_one({"username": username})
  if not user:
    flash("User not found", "error")
  else:
    users_collection.delete_one({"username": username})
    flash(f"User '{username}' deleted successfully", "success")
  return render_template("AdminHome.html") 
