from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connecting to MongoDB
client = MongoClient("mongodb+srv://prithik:Indian@cluster0.gyp783r.mongodb.net/?retryWrites=true&w=majority&appName=cluster0")
db = client["anokha"]
users = db["users"]

# Index Page
@app.route("/")
def index():
    return render_template("index.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = users.find_one({"email": username, "password": password})
        
        if user:
            users.update_one({"admin_email": "yukthi@gmail.com"}, {"$set": {"current_user": username}}, upsert=True)
            return jsonify({"response": "success"}), 200  # Respond with success
        return jsonify({"response": "nologin"}), 200
    
    return render_template("login.html")

# SignUp Page
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    return render_template("signup.html")

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json    
    username = data.get('username')
    password = data.get('password')
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    
    if users.find_one({'email': email}):
        return jsonify({"response": "Mail ID already registered"})
    
    user_data = {
        'Name': username, 
        'password': password,  
        "phone_number": phone_number, 
        "email": email
    }
    users.insert_one(user_data)
    
    users.update_one({"admin_email": "yukthi@gmail.com"}, {"$set": {"current_user": username}}, upsert=True)
    
    return jsonify({"response": "signup"})

# Home Page
@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)