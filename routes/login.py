from flask import Flask, render_template, session, request, Blueprint
from pymongo import MongoClient
import os

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/login", methods=['Post'])
def login_user():
    error = None
    selected_item = request.form.get('dropdown')
    username = request.form.get("username")
    password = request.form.get("password")
    flag = False
    session['username'] = username
    username = session.get('username') 
    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    files = os.listdir(user_folder) 
    if selected_item == 'Admin':
        collection = db['Admin']
        user = collection.find_one({'username': username, 'password': password})
        if user:
            return render_template("AdminHome.html")
        flag = True
    elif selected_item == 'User':
        collection = db['User_Login']
        user = collection.find_one({'username': username, 'password': password})
        if user:
            return render_template("home.html", files = files)
        flag = True
    elif selected_item == 'Investigator':
        collection = db['Investigator']
        user = collection.find_one({'username': username, 'password': password})
        if user:
            return render_template("home.html", files = files)
        flag = True
    if flag:
        error = "User doesnot exist !!!"
        return render_template("login.html",error = error)