from flask import Flask, render_template, request
import os
from resume_parser import extract_text
from matcher import match_resume
from job_matcher import fetch_jobs_from_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ATS ANALYZER
@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":

        file = request.files["resume"]
        skills = request.form["skills"]
        experience = request.form["experience"]
        education = request.form["education"]

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        resume_text = extract_text(file_path)

        result = match_resume(resume_text, skills, experience, education)

        return render_template("result.html", result=result)

    return render_template("index.html")


# SMART JOB FETCH (NO MANUAL INPUT)
@app.route("/jobs", methods=["GET", "POST"])
def jobs():

    jobs_list = []
    detected_skills = []

    if request.method == "POST":

        file = request.files["resume"]

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        resume_text = extract_text(file_path)

        jobs_list, detected_skills = fetch_jobs_from_resume(resume_text)

    return render_template("jobs.html", jobs=jobs_list, skills=detected_skills)


if __name__ == "__main__":
    app.run(debug=True)