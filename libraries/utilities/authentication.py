from constants import settings


class AuthenticationUtilities(object):
    @staticmethod
    def user_is_logged_in(session):
        email = session.get('email')
        return email in settings.ALLOWED_ADMINS
