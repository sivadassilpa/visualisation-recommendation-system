from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from database import connect_to_db

login_bp = Blueprint('login', __name__)

conn = connect_to_db()
cursor = conn.cursor()

@login_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Retrieve user from the database
    user = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Implement your session management or token generation logic here
    return jsonify({'message': 'Login successful'})
