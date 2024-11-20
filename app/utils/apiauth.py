from flask import request
import os


def amIAllowed():
    STORED_API_KEY = os.environ.get('API_KEY')
    api_key = request.headers.get('X-API-KEY')
    if api_key and api_key == STORED_API_KEY:
        return True
    return False