from flask import Flask, render_template, request
from routes.login import login_blueprint
from routes.upload import upload

app = Flask(__name__, static_folder='uploads')  
app.register_blueprint(login_blueprint)
app.register_blueprint(upload)
app.secret_key = '123@Ajay'
@app.route("/")
def login():
    error = ""
    return render_template("login.html",error=error)

if __name__ == "__main__":
    app.run(debug=True)  
