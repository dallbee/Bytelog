from flask import Flask, render_template
from flask.ext.misaka import Misaka, markdown
from flask.ext.assets import Environment, Bundle
from .reader import Reader


md = Misaka()
assets = Environment()
reader = Reader('content', 'service/design/templates/cache')
reader.clean()
reader.build()


def create_app():
    app = Flask(
        __name__.split('.')[0],
        static_url_path='',
        static_folder='../public',
        template_folder='design/templates'
    )

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    register_controllers(app)
    register_errorhandlers(app)
    register_extensions(app)

    return app


def register_controllers(app):
    import pkgutil
    from . import controllers

    for loader, name, ispkg in pkgutil.iter_modules(path=controllers.__path__):
        if not ispkg:
            module = __import__(controllers.__name__ + '.' + name)
            app.register_blueprint(getattr(controllers, name).blueprint)


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{}.jinja'.format(error_code)), error_code

    for errcode in [403, 404, 500, 501]:
        app.errorhandler(errcode)(render_error)


def register_extensions(app):
    md.init_app(app)
    assets.init_app(app)