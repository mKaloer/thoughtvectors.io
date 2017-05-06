from functools import wraps
from hashlib import sha1
import hmac

from flask import Blueprint, request, abort
import requests

hooks_bp = Blueprint('hooks', __name__)

def _get_github_secret():
    return requests.get(GOOGLE_CLOUD_KEY_VALUE_PAIR_URL,
                        headers={
                            'Metadata-Flavor': 'Google'
                        }).json().get('github-jekyll-push-secret', None)


GOOGLE_CLOUD_KEY_VALUE_PAIR_URL = 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/?recursive=true&wait_for_change=false'
GITHUB_SECRET = _get_github_secret()


def validates_secret(f):
    """
    Decorator that validates github webhooks
    """
    @wraps(f)
    def val_secret(*args,**kwargs):
        # Code from https://github.com/carlos-jenkins/python-github-webhooks/blob/master/webhooks.py
        header_signature = request.headers.get('X-Hub-Signature')
        if header_signature is None:
            abort(403)

        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha1':
            abort(501)

        # HMAC requires the key to be bytes, but data is string
        mac = hmac.new(str(GITHUB_SECRET), msg=request.data, digestmod=sha1)
        if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
            abort(403)
        return f(*args, **kwargs)
    return val_secret


@hooks_bp.route('/build_jekyll', methods=["POST"])
@validates_secret
def build_jekyll():
    payload = request.get_json()
    if 'push' in payload['hook']['events']:
        # Create indicator file - will be read by Jekyll deployer
        open('/home(jekyll/do_update', 'w+')
