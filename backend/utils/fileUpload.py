from collections import defaultdict
import itertools
import re

from flask import jsonify
from backend.database import connect_to_db

from backend.utils.dataTypes import DataTypeCategory, type_mapping
from backend.utils.responseParser import responseParser

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
def find_matching_rule(questionnaire, data_profile, user_id, dataProfileId):
    rules = []
    positive_feedback, negative_feedback = returnFeedbacks(user_id, dataProfileId)
    # rules = fetchAllPositiveRules(rules, positive_feedback)

    try:
        # Map data types

        objective = questionnaire["objective"]

        if (
            objective
            == "Exploratory Data Analysis (Summarize main characteristics of data)"
        ):
            rules = handleEDAObjective(
                data_profile, objective, negative_feedback, positive_feedback, rules
            )

        else:
            mapped_data_types = map_data_types(data_profile["data_types"])
            rules = []
            condition = f"objective = {objective}"
            rules_fetched = returnRulesFromDB(condition)
            print(rules_fetched)
            formattedRules = []
            for rule_fetched in rules_fetched:
                formattedRule = responseParser(cursor.description, rule_fetched)
                formattedRules.append(formattedRule)
            for index, rule in enumerate(formattedRules):
                info_types = re.split(r"\sAND\s|\sOR\s", rule["information_type"])
                columnDetails = []
                tempInfoTypes = info_types.copy()
                if rule["action"] == "Clustered Bar Chart":
                    number_columns = mapped_data_types[DataTypeCategory.NUMBERS]
                    category_columns = mapped_data_types[DataTypeCategory.CATEGORIES]
                    for category in category_columns:
                        column = []
                        column.append({category: DataTypeCategory.CATEGORIES})
                        for number in number_columns:
                            column.append({number: DataTypeCategory.NUMBERS})
                        columnDetails.append(column)
                    for columnSet in columnDetails:
                        formattedRules[index]["columnDetails"] = columnSet
                        current_rule = [rules_fetched[index]]
                        rules = returnFormattedRules(
                            current_rule,
                            negative_feedback,
                            positive_feedback,
                            rules,
                            columnSet,
                        )

                else:
                    for info_type in info_types:
                        for key, dtypes in mapped_data_types.items():
                            if info_type in key.value and len(dtypes) > 0:
                                tempInfoTypes.remove(info_type)
                                columnDetails.extend(
                                    [
                                        {dtype: key.value}
                                        for dtype in dtypes
                                        if key.value == info_type
                                    ]
                                )
                                print("info", tempInfoTypes)
                    if len(tempInfoTypes) == 0:
                        formattedRules[index]["columnDetails"] = columnDetails
                        current_rule = [rules_fetched[index]]
                        rules = returnFormattedRules(
                            current_rule,
                            negative_feedback,
                            positive_feedback,
                            rules,
                            columnDetails,
                        )

        rules = crossVerify(rules)
        return rules
    except Exception as e:
        print(e)


def crossVerify(rules):
    # Create a new list to store valid rules
    valid_rules = []

    for rule in rules:
        if rule["action"] == "Scatter Plot":
            # Cross check if data is sufficient for scatter plot
            if len(rule["column"]) > 1:
                valid_rules.append(rule)
        elif rule["action"] == "Histogram" and len(rule["column"]) > 1:
            for column in rule["column"]:
                valid_rules.append(
                    {"column": [column], "rule": rule["rule"], "action": rule["action"]}
                )
        else:
            valid_rules.append(rule)

    return valid_rules


def combine_word_cloud_entries(data):
    combined = defaultdict(lambda: {"column": [], "rule": None, "action": "Word Cloud"})

    for entry in data:
        if entry["action"] == "Word Cloud":
            key = frozenset(entry["rule"].items())
            combined[key]["rule"] = entry["rule"]
            combined[key]["column"].extend(entry["column"])
        else:
            combined[frozenset(entry["rule"].items())] = entry

    # Remove duplicates from column lists
    for key in combined:
        combined[key]["column"] = list(
            {frozenset(col.items()): col for col in combined[key]["column"]}.values()
        )

    return list(combined.values())


def handleEDAObjective(
    data_profile, objective, negative_feedback, positive_feedback, rules
):
    # For EDA, we need the analysis of all the columns
    mapped_data_types = map_data_types_to_info_type(data_profile["data_types"])
    all_columns = [(col, category) for col, category in mapped_data_types.items()]
    all_columns = [(col, category) for col, category in mapped_data_types.items()]

    # Handle single columns
    for col, cat in all_columns:
        condition = f"objective = {objective}"
        infoType = cat.value

        # Query the ruleset for single column
        rules_fetched = returnRulesFromDB(condition, infoType)
        if rules_fetched != []:
            columns = [{col: cat}]
            rules = returnFormattedRules(
                rules_fetched,
                negative_feedback,
                positive_feedback,
                rules,
                columns,
            )
    # Generate all pairs of columns
    column_pairs = list(itertools.combinations(all_columns, 2))
    # Loop through each pair of columns
    for (col1, cat1), (col2, cat2) in column_pairs:
        condition = f"objective = {objective}"
        infoType = (
            cat1.value if cat1.value == cat2.value else f"{cat1.value} AND {cat2.value}"
        )

        # Query the ruleset
        rules_fetched = returnRulesFromDB(
            condition, infoType
        )  # Fetch all matching rules
        if rules_fetched == []:
            # try reverting the info types
            infoType = (
                cat1.value
                if cat1.value == cat2.value
                else f"{cat2.value} AND {cat1.value}"
            )
            rules_fetched = returnRulesFromDB(condition, infoType)
        if rules_fetched != []:
            columns = [{col1: cat1}, {col2: cat2}]
            rules = returnFormattedRules(
                rules_fetched,
                negative_feedback,
                positive_feedback,
                rules,
                columns,
            )
    return rules


def returnFeedbacks(user_id, dataProfileId):
    existingFeedbacks = checkIfFeedbackExists(user_id, dataProfileId)
    positive_feedback = []
    negative_feedback = []

    for pref, rule_ids in existingFeedbacks:
        if pref:
            positive_feedback = rule_ids
        else:
            negative_feedback = rule_ids
    return positive_feedback, negative_feedback


def returnRulesFromDB(condition, infoType=None):
    if infoType:
        query = "SELECT * FROM rules WHERE condition = %s AND information_type = %s"
        cursor.execute(query, (condition, infoType))
    else:
        query = "SELECT * FROM rules WHERE condition = %s"
        cursor.execute(query, (condition,))

    rules_fetched = cursor.fetchall()  # Fetch all matching rules
    return rules_fetched


def returnFormattedRules(
    rules_fetched, negative_feedback, positive_feedback, rules, columns
):
    print("before rules...")
    for rule in rules_fetched:
        # Removing negative feedbacks
        if rule[0] not in negative_feedback:
            rule_dict = responseParser(cursor.description, rule)
            if rule[0] in positive_feedback:
                rules.insert(
                    0,
                    {
                        "column": columns,
                        "rule": rule_dict,
                        "action": rule_dict["action"],
                    },
                )
            else:
                rules.append(
                    {
                        "column": columns,
                        "rule": rule_dict,
                        "action": rule_dict["action"],
                    }
                )
    return rules


# Define the function to map data types of columns
def map_data_types(data_types_dict):
    # Initialize a dictionary to hold the mapped columns
    mapped_columns = {
        DataTypeCategory.NUMBERS: [],
        DataTypeCategory.CATEGORIES: [],
        DataTypeCategory.DATES: [],
        DataTypeCategory.BOOLEAN: [],
        DataTypeCategory.UNKNOWN: [],
        DataTypeCategory.WORDS: [],
    }

    # Extract and map data types
    for column, dtype in data_types_dict.items():
        dtype_str = str(dtype)
        if dtype_str in type_mapping[DataTypeCategory.NUMBERS]:
            mapped_columns[DataTypeCategory.NUMBERS].append(column)
        elif (
            dtype_str in type_mapping[DataTypeCategory.CATEGORIES]
            or dtype_str in type_mapping[DataTypeCategory.BOOLEAN]
        ):
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
        if dtype == "object":
            print("hey")
        else:
            for category, types in type_mapping.items():
                if dtype in types:
                    mapped_data_types[col] = category
                    break
            else:
                mapped_data_types[col] = "unknown"

    return mapped_data_types


def checkIfFeedbackExists(userProfileId, dataProfileId):
    try:
        # Check if the user profile exists for the given userId
        cursor.execute(
            "SELECT preferred, array_agg(ruleid) as ruleids FROM feedback WHERE userprofileid = %s AND dataprofileid = %s GROUP BY preferred",
            (userProfileId, dataProfileId),
        )
        existingFeedback = cursor.fetchall()
        conn.commit()
        return existingFeedback
    except Exception as e:
        print(e)
        conn.rollback()


def fetchAllPositiveRules(rules, positiveFeedback):
    try:
        positiveFeedback_str = ",".join(map(str, positiveFeedback))
        # Check if the user profile exists for the given userId
        cursor.execute(
            f"SELECT * FROM rules WHERE id IN ({positiveFeedback_str});",
        )
        positiveRules = cursor.fetchall()
        conn.commit()
        return positiveRules
    except Exception as e:
        print(e)
        conn.rollback()
