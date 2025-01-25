from flask import render_template, session, request, Blueprint, send_from_directory, request, redirect, url_for
from pymongo import MongoClient
import os, datetime

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
        flag = True

    elif selected_item == 'Analyst':
        collection = db['User_Login']
        user = collection.find_one({'username': username, 'password': password})
        if user:
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
            return render_template("analystHome.html",folders=folder_structure, files= files)
        flag = True

    elif selected_item == 'Investigator':
        collection = db['Investigator']
        user = collection.find_one({'username': username, 'password': password})
        if user:
            return render_template("home.html", files = files, val = 1)
        flag = True
    if flag:
        error = "User doesnot exist !!!"
        return render_template("login.html",error = error)

@login_blueprint.route("/logout", methods=['Post'])
def logout_user():
    username = session.get('username') 
    session.pop(username, None)
    return render_template('/login.html')

@login_blueprint.route('/view/<int:val>', methods=['POST'])
def view(val):
    username = session.get('username')
    file_name = request.form.get(f'file_name{val}')
    file_path = os.path.join(UPLOAD_FOLDER, username, file_name)
    print(file_path) 
    collection = db['History']
    collection.insert_one({"username" : username ,"filename": file_name, "metadata": "-", "time": datetime.datetime.utcnow(), "status":"Accessed" }) 
    return send_from_directory(os.path.join(UPLOAD_FOLDER, username), file_name)
    
@login_blueprint.route('/viewAll/<int:val>', methods=['POST'])
def viewAll(val):
    username = session.get('username')
    collection = db['History']
    upload_path = UPLOAD_FOLDER  
    file_name = request.form.get(f'file_name{val}')  
    collection.insert_one({"username" : username ,"filename": file_name, "metadata": "-", "time": datetime.datetime.utcnow(), "status":"Accessed" })
    for root, dirs, files in os.walk(upload_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"File found at: {file_path}")
            return send_from_directory(root, file_name)

@login_blueprint.route('/delete_file', methods=['POST'])
def delete_file():
    users_collection = db['History'] 
    print("Function is called!")
    username = session.get('username') 
    file_name = request.form.get('file_name')
    file_path = os.path.join(UPLOAD_FOLDER, username)
    file_path = os.path.join(file_path, file_name)
    users_collection.insert_one({"username" : username ,"filename": file_name, "metadata": "-", "time": datetime.datetime.utcnow(), "status":"Deleted" })
    print(file_path)
    if os.path.exists(file_path):
        print("Path exist !!")
        os.remove(file_path)
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