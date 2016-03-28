# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
import hashlib
from initialize_registry import load_registry
from flask import Flask, request
from werkzeug.wsgi import SharedDataMiddleware
from libraries.sentry_client import SentryClient
load_registry()


app = Flask('robotics_scoring_system')
app.debug = True
app.secret_key = '9dBrJXZMW8E44yfODtLuxp5f0Yz2cFfPfUe2Cs2n'

APP_NAME = 'robotics_scoring_system'

app.config.update(
    APP_SESSION_NAME='robotics_scoring_system',
    SENTRY_DSN='https://858c1ce455dc43538c50f8ca3b3358ce:93608270372b4b939737b04a3c816612@app.getsentry.com/60618'
)
SentryClient.init_flask(app)

if app.config.get('ENV') == 'development':
    cacheStatic = False
else:
    cacheStatic = True

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/static': os.path.join(os.path.dirname(__file__), 'static'),
}, cache=cacheStatic)

# blueprints and views
from blueprints.main import main
app.register_blueprint(main)
from blueprints.authentication import authentication
app.register_blueprint(authentication, url_prefix='/auth')


def _get_etag():
    """
    Set an eTag value for the current page
    SHA1 should generate well-behaved etags
    The values that make up the string used for the ETag value are:
    the script root value
    the request path
    the current timestamp
    """
    now = datetime.utcnow().isoformat()
    etag_src = "%s--%s-%s" % (request.script_root, request.path, now,)
    etag = hashlib.sha1(etag_src.encode('utf8', 'replace')).hexdigest()
    return etag


@app.after_request
def cache_control(response):
    max_age = 1
    cache_control_str = "max-age=%s, private, must-revalidate" % max_age
    response.headers.add("Cache-Control", cache_control_str)
    etag = _get_etag()
    response.set_etag(etag)
    return response

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("System started")
    app.run()
