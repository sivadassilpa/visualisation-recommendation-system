import json
import os
from flask import Blueprint, current_app, jsonify, request
import numpy as np
from werkzeug.security import check_password_hash
from backend.database import connect_to_db
from backend.utils.fileUpload import (
    allowed_file,
    find_matching_rule,
    update_data_profile,
)
from backend.utils.profiler import (
    create_vega_chart,
    dataForSelectedColumns,
    extract_profile,
    profile_data,
    convert_int64_to_int,
)
from backend.utils.responseParser import responseParser
from werkzeug.utils import secure_filename

login_bp = Blueprint("login", __name__)

conn = connect_to_db()
cursor = conn.cursor()


@login_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # Retrieve user from the database
    user = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

    user = cursor.fetchone()
    print("user", user[2], password, conn)
    if user:
        user_dict = responseParser(cursor.description, user)
        print("User details:", user_dict, user_dict["id"])
    # if not user or not check_password_hash(user['password_hash'], password):
    if not user or not (user_dict["password_hash"] == password):
        return jsonify({"error": "Invalid username or password"}), 401
    else:
        print("user_dict[id]", user_dict["id"])
        cursor.execute(
            "SELECT * FROM userprofile WHERE userid = %s", (user_dict["id"],)
        )
        userProfile = cursor.fetchone()
        print("userProfileResponse", userProfile)
        userProfileResponse = responseParser(cursor.description, userProfile)
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "userProfile": userProfileResponse,
                    "userId": user_dict["id"],
                }
            ),
            200,
        )


@login_bp.route("/update-user-profile", methods=["POST"])
def updateUserProfile():
    userId = request.json.get("userId")
    userProfile = request.json.get("userProfile")

    if not userId or not userProfile:
        return jsonify({"error": "Invalid data"}), 400

    # Parse the userProfile data into a dictionary
    profile_data = {item["title"]: item["optionSelected"] for item in userProfile}

    # Map the profile_data to the corresponding columns in the userprofile table
    familiarity = profile_data.get("familiarity", "I prefer not to answer")
    profession = profile_data.get("profession", "I prefer not to answer")
    interest = profile_data.get("interests", "I prefer not to answer")
    country = profile_data.get("country", "I prefer not to answer")

    try:
        # Check if the user profile exists for the given userId
        cursor.execute("SELECT id FROM userprofile WHERE userid = %s", (userId,))
        existing_profile = cursor.fetchone()

        if existing_profile:
            # Update the existing user profile
            cursor.execute(
                """
                UPDATE userprofile
                SET familiarity = %s,
                    profession = %s,
                    interest = %s,
                    country = %s
                WHERE userid = %s
            """,
                (familiarity, profession, interest, country, userId),
            )
        else:
            # Insert a new user profile
            cursor.execute(
                """
                INSERT INTO userprofile (userid, familiarity, profession, interest, country)
                VALUES (%s, %s, %s, %s, %s)
            """,
                (userId, familiarity, profession, interest, country),
            )

        conn.commit()
        return jsonify({"message": "User profile updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@login_bp.route("/insert-rules", methods=["POST"])
def insert_rule():
    try:
        data = request.json
        rule_name = data.get("ruleName")
        description = data.get("description")
        condition = data.get("condition")
        information_type = data.get("informationType")
        action = data.get("action")

        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO public.rules (rule_name, description, condition, information_type, action)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (rule_name, description, condition, information_type, action),
        )

        conn.commit()
        return jsonify({"message": "Rule inserted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@login_bp.route("/uploadFile", methods=["POST"])
def upload_file():
    # Improvements : Saving could be avoided and object file could be directly used.
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        columns = request.form.get("columns")
        data_profile_str = request.form.get("dataProfile")
        if data_profile_str:
            data_profile = json.loads(data_profile_str)
            user_id = data_profile.get("userId")
            data_profile = data_profile.get("dataProfile")

        else:
            data_profile = {}
            user_id = None
            data_profile = None
        # Save uploaded file to uploads/filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Metadata Extraction -> DataProfiling
        profile = profile_data(file_path)
        if user_id:
            dataProfileId = update_data_profile(user_id, filename, data_profile)
        if columns:
            selected_columns = columns.split(",")
        else:
            return jsonify({"error": "No columns selected"}), 400

        # Pending =>Save to database
        selected_data_profile = extract_profile(file_path, profile, selected_columns)
        # extract the metadat for selected columns
        # Find the matching rules

        rules = find_matching_rule(
            data_profile, selected_data_profile, user_id, dataProfileId
        )
        vega_specs = []
        for rule in rules:
            selectedData = dataForSelectedColumns(file_path, rule["column"])
            vega_spec = create_vega_chart(
                rule["rule"]["action"], selectedData, rule["column"]
            )
            vega_specs.append({"vegaSpec": vega_spec, "ruleId": rule["rule"]["id"]})
        # data_profile is the Questionnaire response and profile is the metadata profiled
        vega_specs = convert_int64_to_int(vega_specs)
        return (
            jsonify(
                {
                    "message": "File uploaded successfully",
                    "filename": filename,
                    "vegaspec": vega_specs,
                    "dataProfileId": int(dataProfileId),
                    "userId": int(user_id),
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "File type not allowed"}), 400


@login_bp.route("/insert-feedback", methods=["POST"])
def insert_feedback():
    try:
        data = request.json
        ruleId = data.get("ruleId")
        userProfileId = data.get("userProfileId")
        dataProfileId = data.get("dataProfileId")
        preference = data.get("preference")

        conn = connect_to_db()
        cursor = conn.cursor()
        # Check if the user profile exists for the given userId
        cursor.execute(
            "SELECT id FROM feedback WHERE ruleId = %s AND userProfileId = %s AND dataProfileId = %s",
            (
                ruleId,
                userProfileId,
                dataProfileId,
            ),
        )
        existing_profile = cursor.fetchone()

        if existing_profile:
            # Update the existing user profile
            cursor.execute(
                """
                UPDATE feedback
                SET preferred = %s,
                 WHERE ruleId = %s AND userProfileId = %s AND dataProfileId = %s
            """,
                (
                    preference,
                    ruleId,
                    userProfileId,
                    dataProfileId,
                ),
            )
        else:
            cursor.execute(
                """
            INSERT INTO feedback (ruleId, userProfileId, dataProfileId, preferred)
            VALUES (%s, %s, %s, %s)
            """,
                (ruleId, userProfileId, dataProfileId, preference),
            )

        conn.commit()
        return jsonify({"message": "Feedback table updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
