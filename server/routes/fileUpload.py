from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from database import connect_to_db
import json

from utils.responseParser import responseParser
from utils.profiler import create_vega_chart, extract_profile, profile_data

fileUpload_bp = Blueprint("fileUpload", __name__)

conn = connect_to_db()
cursor = conn.cursor()

# Allowed file extensions
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def update_data_profile(userId, filename, dataProfile):
    try:
        # Check if the user profile exists for the given userId
        cursor.execute(
            "SELECT id FROM data_contexts WHERE userid = %s AND filename = %s",
            (userId, filename),
        )
        existing_profile = cursor.fetchone()

        if existing_profile:
            # Update the existing user profile
            print("existing profile : ", existing_profile)
            # return
            try:
                cursor.execute(
                    """
                    UPDATE data_contexts
                    SET
                        objective = %s,
                        patternsinterest = %s,
                        groupcomparison = %s,
                        colorpreferences = %s,
                        usecase = %s
                    WHERE userid = %s AND filename = %s
                """,
                    (
                        dataProfile["objective"],
                        dataProfile["patternsinterest"],
                        dataProfile["groupcomparison"],
                        dataProfile["colorpreferences"],
                        dataProfile["usecase"],
                        userId,
                        filename,
                    ),
                )
            except Exception as e:
                conn.rollback()
                print(e)

        else:
            print("new profile : ", dataProfile)
            print("dataProfile.objective", dataProfile["objective"])
            print("dataProfile.objective", dataProfile["patternsinterest"])
            print("dataProfile.objective", dataProfile["groupcomparison"])
            print("dataProfile.objective", dataProfile["colorpreferences"])
            print("dataProfile.objective", dataProfile["usecase"])
            # return
            # Insert a new user profile
            try:
                cursor.execute(
                    """
                    INSERT INTO data_contexts (userid, filename, objective, patternsinterest, groupcomparison, colorpreferences, usecase)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        userId,
                        filename,
                        dataProfile["objective"],
                        dataProfile["patternsinterest"],
                        dataProfile["groupcomparison"],
                        dataProfile["colorpreferences"],
                        dataProfile["usecase"],
                    ),
                )
            except Exception as e:
                conn.rollback()
                print(e)

        conn.commit()
        return jsonify({"message": "User profile updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@fileUpload_bp.route("/uploadFile", methods=["POST"])
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
        print("dataProfile", user_id, data_profile)

        # Save uploaded file to uploads/filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Metadata Extraction -> DataProfiling
        profile = profile_data(file_path)
        print(profile)
        if user_id:
            update_data_profile(user_id, filename, data_profile)
        if columns:
            selected_columns = columns.split(",")
        else:
            return jsonify({"error": "No columns selected"}), 400

        # Pending =>Save to database
        selected_data_profile = extract_profile(profile, selected_columns)
        # extract the metadat for selected columns
        # Find the matching rules

        rules = find_matching_rule(data_profile, selected_data_profile)
        vega_spec = create_vega_chart(rules[0]["action"])
        # data_profile is the Questionnaire response and profile is the metadata profiled

        return (
            jsonify(
                {
                    "message": "File uploaded successfully",
                    "filename": filename,
                    "vegaspec": vega_spec,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "File type not allowed"}), 400


def find_matching_rule(questionnaire, data_profile):
    rules = []
    try:
        print("inside find_matching_rule", questionnaire, data_profile)
        for key, value in data_profile["data_types"].items():
            # information_types = list(data_profile["data_types"].values())
            dtype = value
            objective = "Understanding general trends"
            info_type = "Numbers" if dtype in ["int64", "float64"] else "object"
            condition = (
                f"objective = '{objective}' AND information_type = '{info_type}'"
            )

            # Query the ruleset
            query = "SELECT * FROM rulesets WHERE condition = %s LIMIT 1"
            cursor.execute(query, (condition,))
            rule = cursor.fetchone()
            rule_dict = responseParser(cursor.description, rule)
            if rule:
                rules.append(
                    {"column": key, "rule": rule_dict, "action": rule_dict["action"]}
                )

        return rules
    except Exception as e:
        print(e)
