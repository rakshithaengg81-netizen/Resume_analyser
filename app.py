
import json
import os
import uuid
import sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from database import create_tables, get_db_connection

from services.resume_extractor import extract_text
from services.skill_analyser import extract_skills, analyse_skills
from services.video_recommender import recommend_videos
from services.interview_question_generator import generate_questions
from services.answer_evaluator import evaluate_answers


app = Flask(__name__)

CORS(app)

# Upload configuration

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Check file extension

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Home page route

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Resume Analyser Backend",
        "status": "success"
    })


# Health check API

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Resume Analyser Backend is running"
    })


# Resume analysis API

@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No resume uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "Please select a resume"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "status": "error",
            "message": "Only PDF and DOCX files are allowed"
        }), 400

    filename = secure_filename(file.filename)

    unique_filename = uuid.uuid4().hex + "_" + filename

    filepath = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    # Get and validate user ID

    user_id = request.form.get("user_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "User ID is required"
        }), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid user ID"
        }), 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            "SELECT id FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    finally:
        connection.close()

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    try:

        # Save uploaded resume temporarily

        file.save(filepath)

        # Extract resume text

        resume_text = extract_text(filepath)

        if not resume_text.strip():
            return jsonify({
                "status": "error",
                "message": "No readable text found in resume"
            }), 400

        # Identify candidate skills

        candidate_skills = extract_skills(resume_text)

        # Generate interview questions

        interview_questions = generate_questions(candidate_skills)

        # Recommend job roles

        job_recommendations = analyse_skills(candidate_skills)

        best_role = job_recommendations[0]

        missing_skills = best_role["missing_skills"]

        # Recommend learning videos

        video_recommendations = recommend_videos(missing_skills)

        # Save resume details in database

        db_connection = get_db_connection()

        try:

            cursor = db_connection.execute(
                """INSERT INTO resumes (user_id, filename)
                   VALUES (?, ?)""",
                (user_id, filename)
            )

            resume_id = cursor.lastrowid

            db_connection.execute(
                """INSERT INTO resume_analysis
                   (resume_id, extracted_skills,
                    job_recommendations, missing_skills)
                   VALUES (?, ?, ?, ?)""",
                (
                    resume_id,
                    json.dumps(candidate_skills),
                    json.dumps(job_recommendations),
                    json.dumps(missing_skills)
                )
            )

            db_connection.commit()

        finally:
            db_connection.close()

        # Return analysis result

        return jsonify({
            "status": "success",
            "message": "Resume analysed successfully",
            "extracted_skills": candidate_skills,
            "job_recommendations": job_recommendations,
            "video_recommendations": video_recommendations,
            "interview_questions": interview_questions
        }), 200

    except Exception:

        app.logger.exception("Resume analysis failed")

        return jsonify({
            "status": "error",
            "message": "Unable to analyse resume"
        }), 500

    finally:

        # Delete temporary uploaded file

        if os.path.exists(filepath):
            os.remove(filepath)


# Interview evaluation API

@app.route("/api/evaluate-interview", methods=["POST"])
def evaluate_interview():

    data = request.get_json()

    if not data or "answers" not in data:
        return jsonify({
            "status": "error",
            "message": "Please provide interview answers."
        }), 400

    answers = data["answers"]

    if not isinstance(answers, list):
        return jsonify({
            "status": "error",
            "message": "Answers must be provided as a list."
        }), 400

    result = evaluate_answers(answers)
    # Save interview attempt in database

    user_id = data.get("user_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "User ID is required"
        }), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid user ID"
        }), 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            "SELECT id FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404

        connection.execute(
            """INSERT INTO interview_attempts
            (user_id, questions, answers, preparedness_percentage)
            VALUES (?, ?, ?, ?)""",
            (
                user_id,
                json.dumps(data.get("questions", [])),
                json.dumps(answers),
                result["preparedness_percentage"]
            )
        )

        connection.commit()

    finally:
        connection.close()
    return jsonify({
        "status": "success",
        "message": "Interview evaluation completed",
        "evaluation": result
    }), 200


# User Registration API

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Please provide registration details."
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "status": "error",
            "message": "Name, email and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "status": "error",
            "message": "Password must contain at least 8 characters."
        }), 400

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()

    try:

        connection.execute(
            """INSERT INTO users (name, email, password)
               VALUES (?, ?, ?)""",
            (name, email, hashed_password)
        )

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Registration successful!"
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "status": "error",
            "message": "Email is already registered."
        }), 409

    finally:
        connection.close()


# User Login API

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Please provide login details."
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required."
        }), 400

    connection = get_db_connection()

    try:

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):

            return jsonify({
                "status": "success",
                "message": "Login successful!",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }
            }), 200

        return jsonify({
            "status": "error",
            "message": "Invalid email or password."
        }), 401

    finally:
        connection.close()


# Run backend server

if __name__ == "__main__":

    create_tables()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
