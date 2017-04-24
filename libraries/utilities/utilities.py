# -*- coding: utf-8; -*-


class Utilities(object):

    @staticmethod
    def safe_cast(val, to, default=None):
    	try:
    		return to(val)
    	except (ValueError, TypeError):
    		return default
