from .. import reader
from flask import Blueprint
from flask import abort
from flask import render_template
import subprocess

blueprint = Blueprint('api', __name__, url_prefix='/api')

# 'git', 'diff-tree', '--no-commit-id', '--name-only', '-r', '$refnum'
# git pull  // if error, rebase and do a rebuild

@blueprint.route('/update')
def notify():
    # Verify that it's github or localhost

    # Return forbidden if not verified

    # Shell out to git

    # Return 204 if successful
    return '', 204


@blueprint.route('/rebuild')
def rebuild():
    reader.clean()
    reader.build_all()
    return '', 204


"""
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
"""
# TODO: Implement 418 (I'm a teapot)