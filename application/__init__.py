from flask import Flask
from pymongo import MongoClient
from flask_login import LoginManager

"""
web app init
"""


# render secret to hide db password
dbpass = ""
with open("dbpassword", "r") as file:
    dbpass = file.readline()

# mongo connection
client = MongoClient(f"mongodb+srv://admin:{dbpass}@cluster0.b6ssuyd.mongodb.net/?retryWrites=true&w=majority")
db = client.db
logins = db.logins
tasks = db.tasks

login_manager = LoginManager()

def create_app():
    """
    Flask app init

    Returns:
        app (Flask): Flask app
    """
    app = Flask(__name__, template_folder=".")
    app.secret_key = b'\xa9\xb8\xc3dC\xec\x01\x8b\xba\xc6\xf4\tTB\x00@'
    
    # init login
    login_manager.init_app(app)

    # main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    return app




