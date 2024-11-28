from flask import Flask
from phone_tracker.app.neo4j import init_driver
from routes.interaction import phone_blueprint
from neo4j import GraphDatabase

app = Flask(__name__)

app.register_blueprint(phone_blueprint)


if __name__ == '__main__':
       with app.app_context():
        init_driver(
            app.config.get('NEO4J_URI'),
            app.config.get('NEO4J_USERNAME'),
            app.config.get('NEO4J_PASSWORD'),
        )
        app.run(host='0.0.0.0', port=5000, debug=True)  