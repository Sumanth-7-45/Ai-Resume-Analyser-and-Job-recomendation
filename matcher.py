import re

def match_resume(resume_text, required_skills, required_exp, required_edu):

    skills_list = [s.strip().lower() for s in required_skills.split(",")]

    matched_skills = []
    missing_skills = []

    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    skill_score = (len(matched_skills) / len(skills_list)) * 100 if skills_list else 0

    years_found = re.findall(r'(\d+)\s+year', resume_text)
    years_found = [int(y) for y in years_found]
    resume_exp = max(years_found) if years_found else 0

    required_exp = int(required_exp)

    if resume_exp >= required_exp:
        exp_score = 100
    else:
        exp_score = (resume_exp / required_exp) * 100

    edu_list = [e.strip().lower() for e in required_edu.split(",")]
    edu_score = 0

    for edu in edu_list:
        if re.search(r'\b' + re.escape(edu) + r'\b', resume_text):
            edu_score = 100
            break

    overall = round((skill_score + exp_score + edu_score) / 3, 2)

    if overall >= 75:
        status = "Shortlisted"
    elif overall >= 60:
        status = "Review"
    else:
        status = "Rejected"

    return {
        "overall": overall,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_exp": resume_exp,
        "status": status
    }