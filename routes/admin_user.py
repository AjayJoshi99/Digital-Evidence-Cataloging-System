from flask import Blueprint, request, redirect, url_for, flash, render_template
from pymongo import MongoClient
import os

user_blueprint = Blueprint('user', __name__)
UPLOAD_FOLDER = 'uploads/'
client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']
users_collection = db['User_Login'] 

@user_blueprint.route('/add', methods=['POST'])
def add_user():
  error = ""
  username = request.form.get('username')
  password = request.form.get('password')
  type = request.form.get('dropdown')
  if True:
    if type == 'Analyst':
      a = db['Analyst'] 
      a.insert_one({"username": username, "password": password})
    else :
      i = db['Investigator'] 
      i.insert_one({"username": username, "password": password})
    error = f"User '{username}' added successfully"
    users_collection = db['History'] 
    files = list(users_collection.find())
    for file in files:
      file["_id"] = str(file["_id"]) 
    folder_structure = {}
    for root, dirs, file in os.walk(UPLOAD_FOLDER):
        relative_path = os.path.relpath(root, UPLOAD_FOLDER)
        if relative_path == ".":
          relative_path = ""
        folder_structure[relative_path] = file
    return render_template("AdminHome.html",folders=folder_structure, files= files)


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


