# -*- coding: utf-8; -*-

from constants import settings


class AuthenticationUtilities(object):
    @staticmethod
    def user_is_logged_in(session):
        email = session.get('email')
        return True
        return email in settings.ALLOWED_ADMINS
