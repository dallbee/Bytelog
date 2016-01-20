from flask import Blueprint, abort, render_template
from .. import x

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/update')
def notify():
    # Verify that it's github or localhost

    # Return forbidden if not verified

    # Return 204 if successful
    pass


@blueprint.route('/rebuild')
def rebuild():
    print('wtf')
    return "HAHA"



def verify_request(payload, ip):

    # Check for secure token

    # Get sha string
    #ver, signature = request.headers.get('X-Hub-Signature')
    if ver != 'sha1':
        abort(501)

    mac = hmac.new(str(secret), msg=request.data, digestmod=sha1)

    if hmac.compare_digest(str(mac.hexdigest()), str(signature))
        return True

    abort(403)
    return False

# TODO: Implement 418 (I'm a teapot)

    #return render_template('content.jinja', content=item.data, title=item.title, description=item.description)