from flask import Blueprint, request, session, jsonify, render_template, send_from_directory
import os, datetime
from pymongo import MongoClient

upload = Blueprint('upload', __name__, url_prefix='/upload')
client = MongoClient("mongodb://localhost:27017/")
db = client['Flask']
collection = db['History']
ckeck = db['Investigator']

UPLOAD_FOLDER = 'uploads/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload.route('/', methods=['GET', 'POST'])
def upload_file():
    username = session.get('username') 
    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    file = request.files.get('file')
    file_name = request.form.get('file_name') 
    metadata = request.form.get('metadata')
    username = session.get('username') 
    val =0
    if ckeck.find({"username":username}):
        val = 1
    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    files = os.listdir(user_folder) 

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        file_extension = os.path.splitext(file.filename)[1]
        safe_file_name = f"{file_name}{file_extension}"
        file_path = os.path.join(user_folder, safe_file_name)
        file.save(file_path)
        collection.insert_one({"username" : username ,"filename": file_name, "metadata": metadata, "time": datetime.datetime.utcnow(), "status":"Uploaded" })
        if val :
            return render_template("home.html", files = files)
        return render_template("analystHome.html", files = files)

    return render_template("upload.html")



