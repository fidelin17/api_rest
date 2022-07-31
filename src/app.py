from email import message
from mimetypes import MimeTypes
from urllib import response
from flask import Flask, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/python"
mongo = PyMongo(app)

@app.route('/users', methods=['POST']) #create user
def crearUsuario():
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']

    if username and password and email:
        hashed_password=generate_password_hash(password)
        id= mongo.db.users.insert_one(
            {'username':username,'email': email,'password':hashed_password}
        )
        response = {
            'id':str(id),
            'username':username,
            'password':hashed_password,
            'email':email
        }
        return response
    else:
        return not_fount()
        #{'messaje':'received'}

    return {'mensaje':'recibido'}

@app.route('/users', methods=['GET']) #get users
def getUsers():
    users=mongo.db.users.find()
    response= json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET']) #get by id
def getUser(id):
    user=mongo.db.users.find_one({"_id":ObjectId(id)}) 
    response= json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE']) #delete by id
def deleteUser(id):
    print(id)
    mongo.db.users.delete_one({"_id":ObjectId(id)}) 
    response=({'message':'user '+id+' deleted success'})
    return response

@app.route('/users/<id>', methods=['PUT']) #update user
def updateUser(id):
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']

    if username and password and email:
        hashed_password=generate_password_hash(password)
        mongo.db.users.update_one({"_id":ObjectId(id)},{'$set':{
            'username':username,
            'email':email,
            'password':hashed_password
        }}) 
        response=({'message':'user '+ id +'was update succsessfully'})
        return response
    else:
        return not_fount()
    

@app.errorhandler(404) #error
def not_fount(error=None):
    response=jsonify({
        'message':'Resource Not Found ' + request.url,
        'status':404
    }) 
    response.status.code= 404
    return response

if __name__ == "__main__":
    app.run(debug=True)