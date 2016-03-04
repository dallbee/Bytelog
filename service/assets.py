from flask_assets import Bundle
from flask_assets import Environment


def init_app(app):
    assets = Environment(app)

    styles = Bundle(
        'main.scss',
        filters='scss',
        output='main.css',
        depends='**/*.scss'
    )

    scripts = Bundle(
        '*.js',
        filters=('slimit'),
        output='main.js'
    )

    assets.register('styles', styles)
    assets.register('scripts', scripts)

    # TODO: Move this config to an environment file
    assets.load_path = ['service/design/styles', 'service/design/scripts']
    assets.config['SASS_STYLE'] = 'compressed'
    assets.url_expire = False
    assets.auto_build = True
