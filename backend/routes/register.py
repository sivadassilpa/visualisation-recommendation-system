from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from backend.database import connect_to_db

register_bp = Blueprint("register", __name__)

conn = connect_to_db()
cursor = conn.cursor()


@register_bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Insert user into the database
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, password_hash),
    )
    conn.commit()

    return jsonify({"message": "User registered successfully"}), 201
