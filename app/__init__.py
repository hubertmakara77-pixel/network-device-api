from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    
    # Configuration simple,basics data base SQLite 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Pin up our data base to aplication
    db.init_app(app)

    # Register endpoint (paths)
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Create table in data base ( if they still exist)
    with app.app_context():
        db.create_all()

    return app