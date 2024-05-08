from flask import Flask, jsonify
from flask_cors import CORS
from database import connect_to_db, close_connection

app = Flask(__name__)
CORS(app)

conn = connect_to_db()
cursor = conn.cursor()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to your Flask API!"})

@app.teardown_appcontext
def teardown_db(exception):
    close_connection(conn, cursor)
    print("Connection to PostgreSQL closed")

from routes.login import login_bp
from routes.register import register_bp
from routes.visualise import visualise_bp

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(visualise_bp)

if __name__ == '__main__':
    app.run(debug=True)
