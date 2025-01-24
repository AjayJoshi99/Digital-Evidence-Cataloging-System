from flask import Blueprint, request, session, jsonify, render_template
import os

upload = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_FOLDER = 'uploads/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload.route('/', methods=['GET', 'POST'])
def upload_file():
    username = session.get('username') 
    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        file_path = os.path.join(user_folder, file.filename)
        file.save(file_path)
        return render_template("upload.html")

    return render_template("upload.html")

