
# Skills database for initial prototype

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "communication",
    "problem solving",
    "git",
    "react",
    "node.js"
]


# Job roles and their required skills

JOB_ROLES = {

    "Python Developer": [
        "python", "flask", "sql", "git"
    ],

    "Web Developer": [
        "html", "css", "javascript", "react"
    ],

    "Data Analyst": [
        "python", "sql", "pandas",
        "numpy", "data analysis"
    ],

    "Machine Learning Engineer": [
        "python", "machine learning",
        "deep learning", "numpy", "pandas"
    ],

    "Java Developer": [
        "java", "sql", "problem solving", "git"
    ]
}


# Identify skills from resume text

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return found_skills


# Analyse missing skills

def analyse_skills(candidate_skills):

    results = []

    for role, required_skills in JOB_ROLES.items():

        matched = [
            skill for skill in required_skills
            if skill in candidate_skills
        ]

        missing = [
            skill for skill in required_skills
            if skill not in candidate_skills
        ]

        percentage = (
            len(matched) / len(required_skills)
        ) * 100

        results.append({

            "job_role": role,

            "matched_skills": matched,

            "missing_skills": missing,

            "match_percentage": round(percentage, 2)

        })

    # Recommend roles with highest match

    results.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return results
