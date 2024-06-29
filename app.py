from flask import Flask, jsonify
from flask_cors import CORS
from backend.utils.create_ontology import test
from backend.database import connect_to_db, close_connection
import os
from backend.factories.bar_chart_factory import BarChartFactory
from backend.factories.line_chart_factory import LineChartFactory
from backend.factories.pie_chart_factory import PieChartFactory

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

conn = connect_to_db()
cursor = conn.cursor()


@app.route("/")
def index():
    return jsonify({"message": "Welcome to your Flask API!"})


@app.teardown_appcontext
def teardown_db(exception):
    close_connection(conn, cursor)
    print("Connection to PostgreSQL closed")


from backend.routes.endpoints import login_bp

app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(debug=True)
