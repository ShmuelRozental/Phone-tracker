import os
from flask import Flask
from neo4j_driver import init_driver
from routes.interaction import phone_blueprint
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.register_blueprint(phone_blueprint)

if __name__ == '__main__':
    with app.app_context():
        init_driver(
        )
        app.run(host='0.0.0.0', port=5000, debug=True)