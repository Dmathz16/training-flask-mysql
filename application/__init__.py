from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = ""
DB_NAME = "training_python_flask"

def create_app(test_config=None):
     
    app = Flask(__name__)
    
    app.secret_key = 'dwadwa'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app