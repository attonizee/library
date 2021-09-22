import os

from flask import Flask
from flask_login import LoginManager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/',
        SQLALCHEMY_DATABASE_URI = "postgresql://library:Xcya6b4u@localhost:5432/library_db", 
        SQLALCHEMY_TRACK_MODIFICATIONS = False      
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/test')
    def test_page():
        return 'Your app is work'

    from .database import db, init_db_command, Users
    db.init_app(app)
    with app.app_context():
        app.cli.add_command(init_db_command)

    from . import auth
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    from . import lib
    app.register_blueprint(lib.bp)
    app.add_url_rule('/', endpoint='index')

    return app