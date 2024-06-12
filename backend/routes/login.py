from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from backend.database import connect_to_db
from backend.utils.responseParser import responseParser

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
