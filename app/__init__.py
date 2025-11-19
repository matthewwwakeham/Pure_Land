from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    
    from.routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    @app.route("/helloworld")
    def ping():
        return {"status": "ok"}
    
    
    return app