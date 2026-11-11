
QUESTION_BANK = {
    "python": [
        "What are the main features of Python?",
        "What is the difference between a list and a tuple?",
        "What are functions in Python?",
        "Explain the concept of inheritance in Python.",
        "What is the difference between == and is?"
    ],

    "java": [
        "What are the main features of Java?",
        "What is the difference between JDK, JRE and JVM?",
        "Explain the concept of inheritance.",
        "What is method overloading and overriding?",
        "What is the difference between an interface and an abstract class?"
    ],

    "sql": [
        "What is SQL?",
        "What is the difference between DELETE and TRUNCATE?",
        "Explain primary key and foreign key.",
        "What is the difference between WHERE and HAVING?",
        "What are SQL joins?"
    ],

    "html": [
        "What is HTML?",
        "What are HTML tags and attributes?",
        "What is the difference between div and span?",
        "What are semantic HTML elements?"
    ],

    "css": [
        "What is CSS?",
        "Explain the CSS box model.",
        "What is the difference between class and ID selectors?",
        "What is Flexbox in CSS?"
    ],

    "javascript": [
        "What is JavaScript?",
        "What is the difference between var, let and const?",
        "What is the difference between == and ===?",
        "What are JavaScript functions?"
    ],

    "machine learning": [
        "What is Machine Learning?",
        "What is the difference between supervised and unsupervised learning?",
        "What is overfitting?",
        "What is the purpose of training and testing datasets?",
        "What is a classification algorithm?"
    ],

    "deep learning": [
        "What is Deep Learning?",
        "What is an artificial neural network?",
        "What is an activation function?",
        "What is backpropagation?"
    ],

    "flask": [
        "What is Flask?",
        "What are routes in Flask?",
        "What is the purpose of an API?",
        "What is the difference between GET and POST requests?"
    ],

    "git": [
        "What is Git?",
        "What is the difference between Git and GitHub?",
        "What is a commit?",
        "What is the purpose of git push and git pull?"
    ],

    "react": [
        "What is React?",
        "What are components in React?",
        "What are props and state?",
        "What is the use of React hooks?"
    ],

    "mongodb": [
        "What is MongoDB?",
        "What is the difference between SQL and NoSQL?",
        "What is a collection in MongoDB?",
        "What is a document in MongoDB?"
    ]
}


def generate_questions(candidate_skills, questions_per_skill=3):

    generated_questions = []

    for skill in candidate_skills:

        skill = skill.lower().strip()

        if skill in QUESTION_BANK:

            questions = QUESTION_BANK[skill][:questions_per_skill]

            generated_questions.append({
                "skill": skill,
                "questions": questions
            })

    return generated_questions
