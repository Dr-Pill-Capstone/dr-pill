from flask import Flask, Blueprint

from test_api import test_bp

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(test_bp, url_prefix='/api/v1/test')
    app.run(debug=True)
