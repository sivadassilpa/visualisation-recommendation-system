from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from backend.database import connect_to_db
import json

from backend.utils.dataTypes import DataTypeCategory, type_mapping
from backend.utils.responseParser import responseParser
from backend.utils.profiler import (
    create_vega_chart,
    extract_profile,
    profile_data,
    dataForSelectedColumns,
)

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
        # Save uploaded file to uploads/filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Metadata Extraction -> DataProfiling
        profile = profile_data(file_path)
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
        selectedData = dataForSelectedColumns(file_path, rules[0]["column"])
        vega_spec = create_vega_chart(rules[0]["action"], selectedData)
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


# Function to find matching rule
def find_matching_rule(questionnaire, data_profile):
    rules = []
    try:
        # Map data types
        mapped_data_types = map_data_types(data_profile["data_types"])
        print(mapped_data_types)

        objective = "Understanding general trends"

        # Loop through each data type category
        for info_type, columns in mapped_data_types.items():
            if not columns:
                continue

            # Construct the condition
            condition = (
                f"objective = '{objective}' AND information_type = '{info_type.value}'"
            )

            # Query the ruleset
            query = "SELECT * FROM rulesets WHERE condition = %s LIMIT 1"
            cursor.execute(query, (condition,))
            rules_fetched = cursor.fetchall()  # Fetch all matching rules
            for rule in rules_fetched:
                rule_dict = responseParser(cursor.description, rule)
                rules.append(
                    {
                        "column": columns,
                        "rule": rule_dict,
                        "action": rule_dict["action"],
                    }
                )

        return rules
    except Exception as e:
        print(e)


# Define the function to map data types of columns
def map_data_types(data_types_dict):
    # Initialize a dictionary to hold the mapped columns
    mapped_columns = {
        DataTypeCategory.NUMBERS: [],
        DataTypeCategory.CATEGORIES: [],
        DataTypeCategory.DATES: [],
        DataTypeCategory.BOOLEAN: [],
        DataTypeCategory.UNKNOWN: [],
    }

    # Extract and map data types
    for column, dtype in data_types_dict.items():
        dtype_str = str(dtype)
        if dtype_str in type_mapping[DataTypeCategory.NUMBERS]:
            mapped_columns[DataTypeCategory.NUMBERS].append(column)
        elif dtype_str in type_mapping[DataTypeCategory.CATEGORIES]:
            mapped_columns[DataTypeCategory.CATEGORIES].append(column)
        elif dtype_str in type_mapping[DataTypeCategory.DATES]:
            mapped_columns[DataTypeCategory.DATES].append(column)
        elif dtype_str in type_mapping[DataTypeCategory.BOOLEAN]:
            mapped_columns[DataTypeCategory.BOOLEAN].append(column)
        else:
            mapped_columns[DataTypeCategory.UNKNOWN].append(column)

    return mapped_columns
