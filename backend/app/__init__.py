from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate
from app.routes.career import career_bp
from app.routes.roadmap import roadmap_bp
from app.routes.career_guidance import career_guidance_bp
from app.routes.career_chat import career_chat_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "https://frontend-nivi25.vercel.app"
                ]
            }
        }
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    from app.routes.health import health_bp
    from app.routes.opportunities import opportunities_bp
    from app.routes.match import match_bp
    app.register_blueprint(roadmap_bp, url_prefix="/api/v1")
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(opportunities_bp, url_prefix="/api/v1")
    app.register_blueprint(match_bp, url_prefix="/api/v1")
    app.register_blueprint(career_bp, url_prefix="/api/v1")
    app.register_blueprint(career_guidance_bp, url_prefix="/api/v1")
    app.register_blueprint(career_chat_bp, url_prefix="/api/v1")
    return app