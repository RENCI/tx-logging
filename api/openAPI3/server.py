import connexion
import re
from jsonschema import draft4_format_checker

regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

match_iso8601 = re.compile(regex).fullmatch


@draft4_format_checker.checks('date-time')
def validate_iso8601(str_val):
    return match_iso8601( str_val ) is not None

    
def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='openapi/')
    app.add_api('my_api.yaml')
    return app
