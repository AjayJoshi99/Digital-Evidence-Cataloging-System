from flask import Flask, render_template, request, Blueprint
from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']
collection = db['User_Login']

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/login", methods=['Post'])
def login_user():
    error = None
    username = request.form.get("username")
    password = request.form.get("password")
    user = collection.find_one({'username': username, 'password': password})
    if user :
        return render_template("home.html")
    else:
        error = "User doesnot exist !!!"
        return render_template("login.html",error = error)