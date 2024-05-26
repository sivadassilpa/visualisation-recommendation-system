from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from database import connect_to_db
import json

from utils.profiler import profile_data

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
    print("here")
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

        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        profile = profile_data(file_path)
        print(profile)
        if user_id:
            update_data_profile(user_id, filename, data_profile)
        if columns:
            selected_columns = columns.split(",")
        else:
            return jsonify({"error": "No columns selected"}), 400

        # Handle file processing and column data as needed
        # For example, you can read the file and process it here

        return (
            jsonify(
                {
                    "message": "File uploaded successfully",
                    "filename": filename,
                    "columns": selected_columns,
                    "profile": profile,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "File type not allowed"}), 400
