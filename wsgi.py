from nmp_web import app as application


def create_app():
    return application


if __name__ == "main":
    application.run()
