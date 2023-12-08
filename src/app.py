from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
 

def create_app():
    
    # create flask app object
    app = Flask(__name__)

    ## Configure app
    app.config.from_object("config.app_config")

    # Disable sorting json keys 
    app.json.sort_keys = False

    # Initiate app objects
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Activate controller blueprints
    from controllers import registerable_controllers    
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    # print(app.url_map)
    return app