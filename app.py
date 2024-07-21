import os
from flask import Flask, url_for, render_template, request, redirect, session , jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from papp import get_chatbot_response

app = Flask(__name__)
app.secret_key = "legobatman31#"

db_connection_string = os.environ.get("MONGODB_CONNECTION_STRING", "localhost:27017")

client = MongoClient(db_connection_string)
db = client["userauth"]
users_coll = db["users"]

def is_logged_in():
    return "username" in session

@app.route("/login/", methods=["GET", "POST"])
def login():
    text = " "
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users_coll.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session["username"] = username
            text = "Login successful."
            return redirect(url_for("chatbot1", username=session["username"]))
        else:
            text = "Invalid username or password. Please try again."

    return render_template("logreg.html")

@app.route("/register/", methods=["GET", "POST"])
def register():
    text = " "
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        if users_coll.find_one({"username": username}):
            text = "ue"
        else:
            if is_valid_password(password):
                users_coll.insert_one({"username": username, "password": generate_password_hash(password), "email":email})
                text = "rs"
            else:
                text="pe"

    return render_template("logreg.html", text=text)

@app.route("/logout/")
def logout():
    if is_logged_in():
        session.pop("username", None)

    return redirect(url_for("login"))

@app.route("/")
def home():
    if is_logged_in():

        return render_template("chatbot.html", username=session["username"])
    else:
        return render_template("index.html")

@app.route("/chatbot/<username>/", methods=["GET", "POST"])
def chatbot(username):
    if is_logged_in():
        if request.method == "POST":
                link1 = request.form.get("link1")
                link2 = request.form.get("link2")
                link3 = request.form.get("link3")
                
                users_coll.update_one({"username":username}, {"$set":{"link1":link1}})
                
                users_coll.update_one({"username":username}, {"$set":{"link2":link2}})
                
                users_coll.update_one({"username":username} , {"$set":{"link3":link3}})
                return redirect(url_for("chatbot1", username=username))

        return render_template('chatbot.html', username=username)
    else:
        return "Not logged in"

@app.route("/chatbot1/<username>/", methods=["GET", "POST"])
def chatbot1(username):
    username=session["username"]
    links=users_coll.find_one({"username":username})
    link1=links['link1']
    link2=links['link2']
    link3=links['link3']
    if is_logged_in():
        if request.method == "POST":
                msg = request.form.get("msg")
                
                response = get_chatbot_response(link1, link2, link3, msg)
                return jsonify(response=response)
        return render_template('chatbot.html', username=username, link1=link1[0:30], link2=link2[0:30], link3=link3[0:30])
    else:
        return "Not logged in"

def is_valid_password(password):
    # Check if password length is between 8 and 20 characters
    if len(password) < 8 or len(password) > 20:
        return False
    
    # Check if password contains at least one number
    has_number = False
    for char in password:
        if char.isdigit():
            has_number = True
            break
    
    return has_number




if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
