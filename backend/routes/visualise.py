from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from database import connect_to_db
from utils.profiler import profile_data
from context.user_profile import UserProfile
from context.data_context import DataContext

visualise_bp = Blueprint("visualise", __name__)


conn = connect_to_db()
cursor = conn.cursor()


@visualise_bp.route("/user-profile", methods=["POST"])
def userProfile():
    user_profiles = {}
    data = request.json
    user_id = data["username"]
    user_profiles[user_id] = UserProfile(
        data["familiarity"], data["profession"], data["interest"]
    ).to_dict()
    # save it to db
    return jsonify({"message": "User profile saved"}), 201


@visualise_bp.route("/data-profile", methods=["POST"])
def dataProfile():
    data_contexts = {}
    data = request.json
    data_id = data["data_id"]
    data_contexts[data_id] = DataContext(
        data["objective"],
        data["data_type"],
        data["patterns"],
        data["comparisons"],
        data["color_preferences"],
        data["usage"],
    ).to_dict()
    # save it to db
    return jsonify({"message": "Data context saved"}), 201
