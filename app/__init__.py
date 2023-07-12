import os
from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from app.models import db, login_manager
from config import config


mail = Mail()

def create_app(config = config.get('development')):
    """The Application Factory."""
    app = Flask(__name__)
    app.config.from_object(config)
    

    #initialize SQLALCHEMY
    #db = SQLAlchemy(app)---done at the models.py level already.
    db.init_app(app)
    db.app = app

    #initialize the login_manager
    login_manager.init_app(app)

    #initialize flask migrate extension
    migrate = Migrate(app, db)
    migrate.init_app(app)
    migrate.app =app

    #initiate flask mail extension
    mail.init_app(app)

    #initialize moment
    moment = Moment()
    moment.init_app(app)
    moment.app = app

    #initialize bootstrap
    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    #bootstrap.app=app

    # register blue prints
    from app.main  import main as main_bp
    app.register_blueprint(main_bp)

    # register authentication blueprint
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    #import and register the employee blueprint
    from app.employee import employee as employee_bp
    app.register_blueprint(employee_bp, url_prefix='/employee', templates_folder='employee')
    
    
    app.debug = True

    return app

