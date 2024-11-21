from flask import request
import os


def amIAllowed():
    try:
        STORED_API_KEY = os.environ.get('API_KEY')
        api_key = request.headers.get('x-api-key')
        if api_key and api_key == STORED_API_KEY:
            return True
        return False
    except Exception as e:
        # Log the exception if needed
        print(f"An error occurred: {e}")
        return False