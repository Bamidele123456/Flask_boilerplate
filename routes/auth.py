from flask import Blueprint, request, jsonify
from ..extensions import users_collection
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({
        "username": data["username"],
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    user = users_collection.find_one({"username": data["username"]})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({"message": "Login successful"}), 200
