from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from database import connect_to_db

visualise_bp = Blueprint('visualise', __name__)

conn = connect_to_db()
cursor = conn.cursor()

@visualise_bp.route('/visualise', methods=['POST'])
def visualise():
    username = request.json.get('username')

    # # Retrieve user from the database
    # user = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    # user = cursor.fetchone()

    # if not user or not check_password_hash(user['password_hash'], password):
    #     return jsonify({'error': 'Invalid username or password'}), 401

    # # Implement your session management or token generation logic here
    return jsonify({'message': username})
