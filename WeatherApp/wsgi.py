from .site import getApp

if __name__ == "__main__":
    getApp.run()


# $ gunicorn --bind 0.0.0.0:5000 'wsgi:create_app()'
