import os


def get_flask_env():
    is_debug = os.getenv("FLASK_DEBUG", "1")
    if is_debug == "1":
        return "development"
    else:
        is_testing = os.getenv("FLASK_TESTING", "0")
        if is_testing == "1":
            return "testing"
        else:
            return "production"
