from flask import Flask, render_template, request
from routes.register import register_blueprint 
from routes.login import login_blueprint

app = Flask(__name__)  
  
app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)

@app.route("/")
def login():
    error = ""
    return render_template("login.html",error=error)

@app.route("/register")
def register():
    error = ""
    return render_template("registration.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)  
