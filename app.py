from flask import Flask, jsonify, request, render_template
from pymongo  import MongoClient

app= Flask(__name__)

# _________________________Connecting MongoDB_________________________
client= MongoClient("mongodb+srv://prithik:Indian@cluster0.gyp783r.mongodb.net/?retryWrites=true&w=majority&appName=cluster0")
db= client["anokha"]
users= db["users"]

# _________________________Connecting REACT_________________________
# Login Page

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    db.users.delete_one({"admin_email":"yukthi@gmail.com"})
    db.users.insert_one({"admin_email":"yukthi@gmail.com", "current_user": username})
    
    user= db.users.find_one({"email": username, "password": password})
    
    if user:
        return jsonify({"response": "login"}), 200

    return jsonify({"response": "nologin"}), 200

#SignUp Page
@app.route("/api/signup", methods=["POST"])
def signup():    
    data= request.json    
    username= data.get('username')
    password= data.get('password')
    preferred_language= data.get('preferredLanguage')
    age= data.get('age')
    gender= data.get('gender')
    phone_number= data.get('phoneNumber')
    email= data.get('email')
    disability= data.get('disabilities')
    
    db.users.delete_one({"admin_email":"yukthi@gmail.com"})
    db.users.insert_one({"admin_email":"yukthi@gmail.com", "current_user": username})
    
    if db.users.find_one({'username': username}):
        return jsonify({"response": "Mail ID already registered"})

    user_data = {'Name': username, 'password': password, 'age':age,'preferred_language':preferred_language, 'gender':gender, "phone_number": phone_number, "email": email, "disability": disability}
    db.users.insert_one(user_data)
    
    return jsonify({"response": "signup"})

if __name__== "__main__":
    app.run(debug= True)