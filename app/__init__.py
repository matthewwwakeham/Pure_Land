from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(
        __name__,
    )
    
    if config_class:
        app.config.from_object(config_class)
    else: 
        from .config import Config
        app.config.from_object(Config)
        
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models so Alembic sees them
    from .models import User, UserProfile, UserActivity, Dialogue
    
    from.routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    @app.route("/helloworld")
    def ping():
        return {"status": "ok"}
    
    
    return app