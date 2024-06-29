import itertools
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
                dataProfileId = existing_profile[0]
            except Exception as e:
                conn.rollback()
                print(e)

        else:
            # Insert a new user profile
            try:
                cursor.execute(
                    """
                    INSERT INTO data_contexts (userid, filename, objective, patternsinterest, groupcomparison, colorpreferences, usecase)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
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
                dataProfileId = cursor.fetchone()[0]
            except Exception as e:
                conn.rollback()
                print(e)

        conn.commit()
        return dataProfileId
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


# Function to find matching rule
def find_matching_rule(questionnaire, data_profile):
    rules = []
    try:
        # Map data types

        objective = questionnaire["objective"]

        if objective == "Understanding general trends (Exploratory Data Analysis)":

            # For EDA, we need the analysis of all the columns
            mapped_data_types = map_data_types_to_info_type(data_profile["data_types"])
            all_columns = [
                (col, category) for col, category in mapped_data_types.items()
            ]
            # Generate all pairs of columns
            column_pairs = list(itertools.combinations(all_columns, 2))

            # Loop through each pair of columns
            for (col1, cat1), (col2, cat2) in column_pairs:
                condition = f"objective = {objective}"
                infoType = (
                    cat1.value
                    if cat1.value == cat2.value
                    else f"{cat1.value} AND {cat2.value}"
                )

                # Query the ruleset
                query = "SELECT * FROM rules WHERE condition = %s AND information_type = %s LIMIT 1"
                cursor.execute(query, (condition, infoType))
                rules_fetched = cursor.fetchall()  # Fetch all matching rules
                for rule in rules_fetched:
                    rule_dict = responseParser(cursor.description, rule)
                    rules.append(
                        {
                            "column": [{col1: cat1}, {col2: cat2}],
                            "rule": rule_dict,
                            "action": rule_dict["action"],
                        }
                    )
        else:
            mapped_data_types = map_data_types(data_profile["data_types"])

            # Loop through each data type category
            for info_type, columns in mapped_data_types.items():
                if not columns:
                    continue

                # Construct the condition
                condition = f"objective = {objective}"
                informationType = f"{info_type.value}"
                # Query the ruleset
                query = "SELECT * FROM rules WHERE condition = %s AND information_type = %s LIMIT 1"
                cursor.execute(query, (condition, informationType))
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


def map_data_types_to_info_type(data_types):
    mapped_data_types = {}

    for col, dtype in data_types.items():
        for category, types in type_mapping.items():
            if dtype in types:
                mapped_data_types[col] = category
                break
        else:
            mapped_data_types[col] = "unknown"

    return mapped_data_types
