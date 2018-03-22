from flask import Flask, jsonify, request
import pymongo
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from models.accounts import Account

#define app Flask
app = Flask(__name__)
#connect flask to mongodb
conn = pymongo.MongoClient('0.0.0.0',27017)
#get database
db = conn.dbtest

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = '12345'  # Change this!
jwt = JWTManager(app)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    usertbl = db.user
    usercur = usertbl.find({"username" : username, "password" : password})
    if usercur.count() == 0:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

#Get account
@app.route('/getall', methods=['GET'])
@jwt_required
def getall():
    acctbl = db.accounts
    data = acctbl.find()
    if data:
        rs = []
        for i in data:
            acc = Account(i['account_number'], i['firstname'], i['lastname'],i['gender'],i['age'], i['email'],
                          i['city'], i['address'], i['state'],i['employer'], i['balance'])
            rs.append(acc)
        return jsonify({
            "data" : [x.tojson() for x in rs],
            "size" : len(rs),
            "msg"  : 'get data successed'
        }), 200
    else:
        return jsonify({
            "data" : None,
            "size" : 0,
            "msg"  : 'get data failed'
        }), 404
#method post : add new accounts
@app.route('/addnew', methods=['POST'])
@jwt_required
def addnew():
    current_username = get_jwt_identity()
    if isadmin(current_username):
        if request.method == 'POST':
            data = request.json
            acc = Account(data['account_number'], data['firstname'], data['lastname'], data['gender'], data['age'],
                          data['email'],data['city'], data['address'], data['state'], data['employer'], data['balance'])
            acctbl = db.accounts
            acctbl.insert(acc.tojson())
            return jsonify({
                'msg': 'insert successed'
            }), 201
    else:
        return jsonify({
            "msg": 'Access permission denied'
        }), 400

#method put : update an account
@app.route('/update/<id>', methods=['PUT'])
@jwt_required
def update(id):
    current_username = get_jwt_identity()
    if isadmin(current_username):
        if request.method == 'PUT':
            data = request.json
            acc = Account(data['account_number'], data['firstname'], data['lastname'], data['gender'], data['age'],
                          data['email'], data['city'], data['address'], data['state'], data['employer'],
                          data['balance'])
            acctbl = db.accounts
            acctbl.update_one({"account_number" : id}, { "$set" : acc.tojson()})

            return jsonify({
                'msg': 'update successed'
            }), 201
    else:
        return jsonify({
            "msg": 'Access permission denied'
        }), 400

def isadmin(username):
    usertbl = db.user
    usercur = usertbl.find({"username": username})
    if usercur.count() > 0:
        for u in usercur:
            if u["usertype"] == 1:
                return True
            else:
                return False
if __name__ == '__main__':
    app.run(port=5000)


