
from app.extensions import db
from app.models import CareerGoal, RoadmapTask


ROADMAP_TEMPLATES = {
    "python developer": {
        "beginner": [
            ("Python setup and basics", "Set up Python and practise print(), variables, and comments."),
            ("Data types and input", "Practise strings, numbers, type conversion, and input()."),
            ("Conditions", "Write programs using if, elif, else, and comparison operators."),
            ("Loops", "Practise for loops, while loops, and range()."),
            ("Lists and dictionaries", "Practise storing and updating collections."),
            ("Functions", "Write reusable functions with parameters and return values."),
            ("Mini-project", "Build a command-line quiz or expense tracker."),
        ],
        "intermediate": [
            ("Advanced functions", "Practise arguments, scope, and lambda functions."),
            ("Object-oriented Python", "Create classes, objects, and methods."),
            ("File handling", "Read and write text, CSV, and JSON files."),
            ("Exceptions and modules", "Handle errors and organise reusable modules."),
            ("SQL and Python", "Connect Python to a database and practise CRUD."),
            ("API development", "Build a small REST API using Flask."),
            ("Portfolio project", "Build and document a database-backed application."),
        ],
        "advanced": [
            ("Advanced Python", "Practise generators, decorators, and context managers."),
            ("Testing", "Write unit tests and practise mocking."),
            ("Application architecture", "Separate routes, services, models, and configuration."),
            ("Database optimisation", "Practise indexes, transactions, and query optimisation."),
            ("API security", "Implement validation and secure authentication."),
            ("Background processing", "Explore queues and scheduled tasks."),
            ("Production project", "Build, test, document, and deploy a Python service."),
        ],
    },
    "data analyst": {
        "beginner": [
            ("Data analysis foundations", "Learn datasets, data types, and analytical questions."),
            ("Excel fundamentals", "Practise formulas, sorting, filtering, and tables."),
            ("SQL basics", "Practise SELECT, WHERE, ORDER BY, and LIMIT."),
            ("Python for data", "Read CSV files and practise Python basics."),
            ("Pandas basics", "Load a dataset and inspect its columns."),
            ("Data visualisation", "Create simple charts and interpret patterns."),
            ("Mini-project", "Analyse a dataset and write three findings."),
        ],
        "intermediate": [
            ("Advanced SQL", "Practise JOINs, GROUP BY, subqueries, and common table expressions."),
            ("Pandas data cleaning", "Handle missing values, duplicates, and inconsistent data."),
            ("Exploratory data analysis", "Use statistics and charts to investigate a dataset."),
            ("Statistical analysis", "Practise distributions, correlation, and sampling."),
            ("Dashboard development", "Build a dashboard in Power BI or Tableau."),
            ("Business analysis", "Translate business questions into metrics and findings."),
            ("Portfolio project", "Analyse a dataset and present findings in a report or dashboard."),
        ],
        "advanced": [
            ("Advanced SQL analytics", "Practise window functions and complex analytical queries."),
            ("Experiment analysis", "Evaluate A/B tests and statistical uncertainty."),
            ("Data modelling", "Understand analytical tables and dimensional modelling."),
            ("Dashboard performance", "Improve measures, filters, and usability."),
            ("Forecasting fundamentals", "Build and evaluate a time-series baseline."),
            ("Automated reporting", "Create a repeatable Python pipeline with quality checks."),
            ("Capstone analysis", "Deliver a documented analysis with recommendations."),
        ],
    },
    "ai/ml engineer": {
        "beginner": [
            ("Python for AI", "Practise Python functions, collections, and modules."),
            ("NumPy foundations", "Work with arrays and vectorised operations."),
            ("Pandas foundations", "Load, inspect, and clean a dataset."),
            ("Math foundations", "Review vectors, matrices, probability, and statistics."),
            ("Visualise data", "Plot distributions and relationships."),
            ("Machine learning basics", "Understand features, labels, and training sets."),
            ("Mini-project", "Train and evaluate a simple ML model."),
        ],
        "intermediate": [
            ("Data preprocessing", "Build reproducible cleaning and preparation steps."),
            ("Model training", "Train baseline regression and classification models."),
            ("Model evaluation", "Compare metrics and inspect prediction errors."),
            ("Feature engineering", "Create and validate useful features."),
            ("Model selection", "Use cross-validation and tune parameters."),
            ("Model serving", "Expose a trained model through a Flask API."),
            ("Portfolio project", "Build and document an end-to-end ML application."),
        ],
        "advanced": [
            ("Deep learning foundations", "Implement and evaluate a neural-network baseline."),
            ("Experiment tracking", "Record model configurations and metrics."),
            ("ML data pipelines", "Build repeatable preprocessing and validation workflows."),
            ("Model deployment", "Package and serve a model reproducibly."),
            ("Monitoring", "Track prediction quality, drift, and service health."),
            ("Responsible AI", "Evaluate bias, privacy, and model limitations."),
            ("Production capstone", "Deliver a tested ML service with documentation."),
        ],
    },
}


def _normalise_career_path(career_path):
    value = " ".join(career_path.strip().lower().split())
    aliases = {
        "machine learning engineer": "ai/ml engineer",
        "ai ml engineer": "ai/ml engineer",
    }
    return aliases.get(value, value)


def _normalise_skill_level(skill_level):
    value = (skill_level or "beginner").strip().lower()
    if value not in {"beginner", "intermediate", "advanced"}:
        return "beginner"
    return value


def generate_weekly_roadmap(career_goal_id):
    goal = db.session.get(CareerGoal, career_goal_id)

    if goal is None:
        return None, "Career goal not found"

    existing_task = RoadmapTask.query.filter_by(
        career_goal_id=goal.id,
        week_number=1,
    ).first()

    if existing_task:
        return None, "A roadmap for week 1 already exists"

    career_path = _normalise_career_path(goal.career_path)
    skill_level = _normalise_skill_level(goal.current_skill_level)

    career_templates = ROADMAP_TEMPLATES.get(career_path)
    if career_templates is None:
        return None, "A roadmap template is not available for this career path yet"

    tasks = career_templates[skill_level]
    roadmap_tasks = [
        RoadmapTask(
            career_goal_id=goal.id,
            week_number=1,
            day_number=day_number,
            title=title,
            description=description,
            estimated_minutes=estimate_task_minutes(
    title,
    goal.daily_minutes,
),
        )
        for day_number, (title, description) in enumerate(tasks, start=1)
    ]

    try:
        db.session.add_all(roadmap_tasks)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return roadmap_tasks, None
def estimate_task_minutes(title, daily_minutes):
    """Estimate a realistic study session for a roadmap task."""
    title_lower = title.lower()

    if any(word in title_lower for word in (
        "mini-project",
        "portfolio project",
        "capstone",
        "production project",
    )):
        workload_factor = 1.5
    elif any(word in title_lower for word in (
        "project",
        "dashboard",
        "model training",
        "automated reporting",
    )):
        workload_factor = 1.25
    else:
        workload_factor = 1.0

    estimated = round(daily_minutes * workload_factor)

    # Keep one session within a practical range.
    return max(10, min(estimated, 90))