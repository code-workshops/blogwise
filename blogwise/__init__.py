from werkzeug.utils import find_modules, import_string

from flask import Flask

from blogwise.models import connect_to_db


def app_factory(config_obj):
    """
    Create a new application instance.
    :param config_obj: `str` with dot notation (ex. 'app.settings.prod')
    :return: `Flask` app object
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Initialize modules
    connect_to_db(app)

    # Register all blueprints
    register_all_blueprints(app)

    # Return application process
    return app


def register_all_blueprints(app):
    """
    Searches the Views directory for blueprints and registers them.

    All views must have a `bp` attribute whose value is a Blueprint(). Ex.:
        `bp = Blueprint('my_view', __name__)`

    It will not be registered with the current application unless it has
    this attribute!

    :param app: The application for registration
    :return:
    """
    for view in find_modules('blogwise.views'):
        mod = import_string(view)
        uniq = set()
        if hasattr(mod, 'bp'):
            # Avoid duplicate imports
            if mod not in uniq:
                uniq.add(mod)
                app.register_blueprint(mod.bp)
    app.logger.info("Blueprints registered.")
