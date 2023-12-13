from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
#Error handlers
from werkzeug.exceptions import BadRequest
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import DataError, IntegrityError

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

    # Error handlers
    @app.errorhandler(KeyError)
    def key_error(key_error):
        return {'error': f'The field {key_error} is required'}, 400
    
    @app.errorhandler(BadRequest)
    def default_error(e):
        return {'error': e.description}, 400
    
    @app.errorhandler(DataError)
    def Not_found_error(e):
        return {'error': str(e)}, 404
    
    @app.errorhandler(IntegrityError)
    def integrity_error(e):
        return {'error': e.orig.pgerror}, 404
    
    @app.errorhandler(ValidationError)
    def validation_error(e):
        return {'error': e.messages}, 400
    
    @app.errorhandler(403)
    def Unauthorised_error(e):
        return {"error" : e.description}, 403
    
    @app.errorhandler(404)
    def Not_found_error(e):
        return {'error': e.description}, 404

    # print(app.url_map)
    return app