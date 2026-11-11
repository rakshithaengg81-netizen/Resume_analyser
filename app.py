
import os
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from services.resume_extractor import extract_text
from services.skill_analyser import extract_skills, analyse_skills
from services.video_recommender import recommend_videos
from services.interview_question_generator import generate_questions
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
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )
# Home page route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Resume Analyser Backend",
        "status": "success"
    })

# Test backend API

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

    unique_filename = (
        uuid.uuid4().hex + "_" + filename
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    try:

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
        interview_questions = generate_questions(candidate_skills)
        job_recommendations = analyse_skills(candidate_skills)

        best_role = job_recommendations[0]

        missing_skills = best_role["missing_skills"]

        video_recommendations = recommend_videos(missing_skills)

        return jsonify({
    "status": "success",
    "message": "Resume analysed successfully",
    "extracted_skills": candidate_skills,
    "job_recommendations": job_recommendations,
    "video_recommendations": video_recommendations,
    "interview_questions": interview_questions
})

    except Exception as e:

        app.logger.exception("Resume analysis failed")

        return jsonify({
            "status": "error",
            "message": "Unable to analyse resume"
        }), 500

    finally:

        if os.path.exists(filepath):
            os.remove(filepath)


# Run backend server

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
