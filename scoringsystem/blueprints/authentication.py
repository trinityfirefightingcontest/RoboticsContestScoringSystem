# -*- coding: utf-8 -*-

import requests
from flask import (
    Blueprint, current_app, session, request,
    redirect, url_for, flash,
)
from oauth2client.client import OAuth2WebServerFlow, Error
from constants import settings


authentication = Blueprint('auth', __name__)


def is_logged_in(active_session):
    return 'credentials' in active_session


@authentication.before_request
def redirect_if_logged_in():
    if request.path == url_for('.sign_out'):
        pass
    elif is_logged_in(session):
        return redirect(url_for('main.index'))


@authentication.route('/sign-out')
def sign_out():
    session.clear()
    flash('You have been signed out', 'info')
    return redirect(url_for('main.index'))


def _get_web_server_flow():
    # Dynamically build redirect uri given current host.  Allowed hosts are
    # set in the google api console.
    redirect_uri = _build_redirect_uri(request)

    # Instantiate same flow object each time.  Since each step doesn't modify
    # the state of the flow object, using the same one is not necessary.
    return OAuth2WebServerFlow(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        scope=settings.OAUTH2_SCOPE,
        redirect_uri=redirect_uri,
        approval_prompt='force'
    )


@authentication.route('/oauth2-login')
def oauth2_login():
    flow = _get_web_server_flow()
    authorize_url = flow.step1_get_authorize_url()
    return redirect(authorize_url)


@authentication.route('/oauth2-callback')
def callback():
    if 'code' in request.args:
        flow = _get_web_server_flow()
        # Exchange auth code for OAuth2Credentials containing access token
        try:
            credentials = flow.step2_exchange(request.args.get('code'))
            email, white_listed = _is_white_listed(credentials)
            if white_listed:
                # Store credentials on session to signify login
                session['email'] = email
                return redirect(url_for('main.home'))
            else:
                message = "Not a valid email address."
        except Error:
            message = (
                "Could not gain credentials from Google. Please try again."
            )
    else:
        message = "Could not extract authorization code from Google callback."
    session.clear()
    _oauth2_error_handler(message)
    return redirect(url_for('main.signin'))


def _build_redirect_uri(request):
    if request.scheme == 'https':
        return "https://{0}/auth/oauth2-callback".format(request.host)
    else:
        return "http://{0}/auth/oauth2-callback".format(request.host)


def _is_white_listed(credentials):
    access_token = credentials.access_token
    profile_uri = settings.PROFILE_URI
    result = requests.get(profile_uri, params={'access_token': access_token})
    email = result.json()['email']
    return email, email in settings.ALLOWED_ADMINS


def _oauth2_error_handler(message):
    current_app.logger.error('OAuth2 Error: %s' % message)
    flash(message, 'error')
