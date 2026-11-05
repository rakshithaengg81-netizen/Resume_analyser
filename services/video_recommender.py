
VIDEO_RESOURCES = {
    "python": {
        "title": "Python for Beginners",
        "url": "https://www.youtube.com/results?search_query=Python+for+Beginners+full+course"
    },
    "java": {
        "title": "Java Programming Tutorial",
        "url": "https://www.youtube.com/results?search_query=Java+Programming+full+course"
    },
    "sql": {
        "title": "SQL Full Course",
        "url": "https://www.youtube.com/results?search_query=SQL+full+course+for+beginners"
    },
    "html": {
        "title": "HTML Tutorial",
        "url": "https://www.youtube.com/results?search_query=HTML+full+course"
    },
    "css": {
        "title": "CSS Tutorial",
        "url": "https://www.youtube.com/results?search_query=CSS+full+course"
    },
    "javascript": {
        "title": "JavaScript Tutorial",
        "url": "https://www.youtube.com/results?search_query=JavaScript+full+course"
    },
    "react": {
        "title": "React JS Tutorial",
        "url": "https://www.youtube.com/results?search_query=React+JS+full+course"
    },
    "machine learning": {
        "title": "Machine Learning for Beginners",
        "url": "https://www.youtube.com/results?search_query=Machine+Learning+for+Beginners"
    },
    "deep learning": {
        "title": "Deep Learning Tutorial",
        "url": "https://www.youtube.com/results?search_query=Deep+Learning+full+course"
    },
    "flask": {
        "title": "Flask Python Tutorial",
        "url": "https://www.youtube.com/results?search_query=Flask+Python+full+course"
    },
    "django": {
        "title": "Django Tutorial",
        "url": "https://www.youtube.com/results?search_query=Django+Python+full+course"
    },
    "mongodb": {
        "title": "MongoDB Tutorial",
        "url": "https://www.youtube.com/results?search_query=MongoDB+full+course"
    },
    "git": {
        "title": "Git and GitHub Tutorial",
        "url": "https://www.youtube.com/results?search_query=Git+and+GitHub+full+course"
    },
    "pandas": {
        "title": "Pandas Tutorial",
        "url": "https://www.youtube.com/results?search_query=Python+Pandas+full+course"
    },
    "numpy": {
        "title": "NumPy Tutorial",
        "url": "https://www.youtube.com/results?search_query=Python+NumPy+full+course"
    }
}


def recommend_videos(missing_skills):

    recommendations = []

    for skill in missing_skills:

        skill = skill.lower()

        if skill in VIDEO_RESOURCES:

            recommendations.append({
                "skill": skill,
                "video_title": VIDEO_RESOURCES[skill]["title"],
                "video_url": VIDEO_RESOURCES[skill]["url"]
            })

        else:
            recommendations.append({
                "skill": skill,
                "video_title": f"Learn {skill}",
                "video_url": (
                    "https://www.youtube.com/results?search_query="
                    + skill.replace(" ", "+")
                    + "+tutorial"
                )
            })

    return recommendations
