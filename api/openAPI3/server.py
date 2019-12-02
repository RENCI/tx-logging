import connexion
import re
from jsonschema import draft4_format_checker
import tx.connexion.utils

    
def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='openapi/')
    app.add_api('my_api.yaml')
    return app
