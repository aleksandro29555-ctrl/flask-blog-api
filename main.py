from flask import Flask, jsonify, request
from model import User, Twit
import json

twits = []
next_id = 1
users = {}
next_user_id = 1

def find_twit(twit_id: int):
    for t in twits:
        if t.id == twit_id:
            return t
    return None
def find_twit_users(user_id: int):
    twit_users = []
    for t in twits:
        if t.author.user_id == user_id:
            twit_users.append(t)
    return twit_users
app = Flask(__name__)

@app.route("/user", methods=['POST'])

def create_user():
    global next_user_id
    user_json = request.get_json()
    user = User(next_user_id, user_json["username"])
    users[next_user_id] = user
    next_user_id += 1
    return jsonify(user.to_dict()), 201

@app.route("/user", methods=['GET'])

def read_user():
    return jsonify([{"id": u.user_id, "username": u.username} for u in users.values()]), 200

@app.route("/user/<int:user_id>/twits", methods=['GET'])

def read_twit_users(user_id):
    twit_users = find_twit_users(user_id)
    if not twit_users:
        return jsonify({"error": "not found"}), 404
    return jsonify([twit.to_dict() for twit in twit_users]), 200

@app.route("/twit", methods=['POST'])

def create_twit():
    '''{"body": "Hello World", "author": "@someguy"}'''
    global next_id
    twit_json = request.get_json()
    user = users.get(twit_json["author_id"])
    twit = Twit(next_id, twit_json["body"], user)
    next_id += 1
    twits.append(twit)
    return jsonify(twit.to_dict()), 201

@app.route("/twit", methods=['GET'])

def read_twit():
    return jsonify([twit.to_dict() for twit in twits])

@app.route("/twit/<int:twit_id>", methods=['PUT'])

def update_twit(twit_id):
    twit = find_twit(twit_id)
    if not twit:
        return jsonify({"error": "not found"}), 404
    data = request.get_json() or {}
    if "body" in data:
        twit.body = data["body"]
    if "author" in data:
        twit.author = User(data["author"])
    return jsonify(twit.to_dict()), 200

@app.route("/twit/<int:twit_id>", methods=["DELETE"])

def delete_twit(twit_id):
    for i, t in enumerate(twits):
        if t.id == twit_id:
            twits.pop(i)
            return jsonify({"status": "deleted", "id": twit_id}), 200

    return jsonify({"error": "not found"}), 404
        

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True, use_reloader=False)