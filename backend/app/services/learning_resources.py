
RESOURCE_CATALOG = {
    "sql": [
        {
            "title": "SQL Tutorial",
            "url": "https://www.postgresql.org/docs/current/tutorial.html",
            "type": "Documentation",
        },
        {
            "title": "SQL Practice",
            "url": "https://sqlbolt.com/",
            "type": "Interactive practice",
        },
    ],
    "pandas": [
        {
            "title": "Pandas Getting Started",
            "url": "https://pandas.pydata.org/docs/getting_started/index.html",
            "type": "Documentation",
        },
        {
            "title": "Pandas Exercises",
            "url": "https://www.kaggle.com/learn/pandas",
            "type": "Practice",
        },
    ],
    "data analysis": [
        {
            "title": "Kaggle Learn",
            "url": "https://www.kaggle.com/learn",
            "type": "Courses and practice",
        },
        {
            "title": "Matplotlib Tutorials",
            "url": "https://matplotlib.org/stable/tutorials/index.html",
            "type": "Documentation",
        },
    ],
    "statistical analysis": [
        {
            "title": "SciPy Statistics",
            "url": "https://docs.scipy.org/doc/scipy/tutorial/stats.html",
            "type": "Documentation",
        },
        {
            "title": "Khan Academy Statistics",
            "url": "https://www.khanacademy.org/math/statistics-probability",
            "type": "Lessons",
        },
    ],
    "dashboard": [
        {
            "title": "Power BI Learning",
            "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi",
            "type": "Official learning path",
        },
        {
            "title": "Tableau Training",
            "url": "https://www.tableau.com/learn/training",
            "type": "Training",
        },
    ],
    "python": [
        {
            "title": "Python Tutorial",
            "url": "https://docs.python.org/3/tutorial/",
            "type": "Official documentation",
        },
        {
            "title": "Python Practice",
            "url": "https://exercism.org/tracks/python",
            "type": "Exercises",
        },
    ],
    "pytorch": [
        {
            "title": "PyTorch Tutorials",
            "url": "https://docs.pytorch.org/tutorials/",
            "type": "Official tutorials",
        },
    ],
    "machine learning": [
        {
            "title": "Scikit-learn Tutorials",
            "url": "https://scikit-learn.org/stable/tutorial/index.html",
            "type": "Official tutorials",
        },
        {
            "title": "Kaggle Learn",
            "url": "https://www.kaggle.com/learn",
            "type": "Courses and practice",
        },
    ],
    "api": [
        {
            "title": "Flask Documentation",
            "url": "https://flask.palletsprojects.com/",
            "type": "Official documentation",
        },
        {
            "title": "OWASP API Security",
            "url": "https://owasp.org/www-project-api-security/",
            "type": "Security guide",
        },
    ],
    "testing": [
        {
            "title": "Pytest Documentation",
            "url": "https://docs.pytest.org/en/stable/",
            "type": "Official documentation",
        },
    ],
    "portfolio": [
        {
            "title": "Kaggle Datasets",
            "url": "https://www.kaggle.com/datasets",
            "type": "Project datasets",
        },
        {
            "title": "GitHub Skills",
            "url": "https://skills.github.com/",
            "type": "Practical tutorials",
        },
    ],
}

DEFAULT_RESOURCES = [
    {
        "title": "GitHub Skills",
        "url": "https://skills.github.com/",
        "type": "Practical tutorials",
    },
    {
        "title": "Kaggle Learn",
        "url": "https://www.kaggle.com/learn",
        "type": "Courses and practice",
    },
]


def get_learning_resources(title, career_path=""):
    """Return curated learning links relevant to a roadmap task."""
    text = f"{career_path} {title}".lower()

    # More specific keywords should be checked first.
    if "portfolio" in text or "capstone" in text or "mini-project" in text:
        keys = ["portfolio"]
    elif "pandas" in text or "data cleaning" in text:
        keys = ["pandas"]
    elif "sql" in text:
        keys = ["sql"]
    elif "statistical" in text or "statistics" in text:
        keys = ["statistical analysis"]
    elif "dashboard" in text or "visualisation" in text or "visualization" in text:
        keys = ["dashboard"]
    elif "pytorch" in text or "deep learning" in text or "neural network" in text:
        keys = ["pytorch"]
    elif "machine learning" in text or "model training" in text or "model evaluation" in text:
        keys = ["machine learning"]
    elif "api" in text or "flask" in text:
        keys = ["api"]
    elif "test" in text or "mocking" in text:
        keys = ["testing"]
    elif "python" in text or "function" in text or "programming" in text:
        keys = ["python"]
    elif "data analyst" in text or "exploratory" in text or "data analysis" in text:
        keys = ["data analysis"]
    else:
        return DEFAULT_RESOURCES

    return RESOURCE_CATALOG[keys[0]]
