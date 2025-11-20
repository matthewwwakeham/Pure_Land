from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import uuid

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

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
    login_manager.init_app(app)
    
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    
    from .models import User, UserProfile, UserActivity, Dialogue
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(uuid.UUID(user_id))
    
    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    
    @app.route("/helloworld")
    def ping():
        return {"status": "ok"}
    
    return app