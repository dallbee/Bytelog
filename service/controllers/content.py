from flask import Blueprint, abort, render_template
from .. import x

blueprint = Blueprint('content', __name__)


@blueprint.route('/', defaults={'id': 'index'})
@blueprint.route('/<id>')
def content(id):
    x["name"] = "tras"
    return x["name"]
    #return render_template('content.jinja', content=item.data, title=item.title, description=item.description)