from flask import Flask, render_template, request,Blueprint
from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']
collection = db['User_Login']

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['POST'])
def register_user():
    error = None
    if request.method == 'GET':
        return render_template("registration.html", error=error)
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_password')
    obj1 = collection.find_one({'username': username})
    obj2 = collection.find_one({'email' : email})
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
    if not re.match(password_regex, password):
        error = "password must be in standard form !!!"
        return render_template("registration.html", error = error)
        return 
    elif obj1 :
        error = "username is already taken !!!"
        return render_template("registration.html", error = error)
    elif obj2 :
        error = "Email is already in used !!!"
        return render_template("registration.html", error = error)
    elif password == confirm_pass:
        collection.insert_one({'username': username, 'password': password,'email' : email })
        return render_template("home.html")
    else:
        error = "invalid data !!!\nPlease enter valid details"
        return render_template("registration.html", error = error)