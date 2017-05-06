from flask import Flask
from . import hooks

application = Flask(__name__)
application.register_blueprint(hooks.hooks_bp, url_prefix='/api/hooks')

@application.route("/api/foo")
def hello():
    return "bar"


if __name__ == "__main__":
    application.run()
