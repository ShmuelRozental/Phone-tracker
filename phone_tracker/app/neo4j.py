from neo4j import GraphDatabase
from flask import current_app

def init_driver(uri, username, password):
    current_app.driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_pool_size=20)
    return current_app.driver

def get_driver():
    if not hasattr(current_app, 'driver'):
        raise ValueError("Driver not initialized.")
    return current_app.driver

def close_driver():
    if hasattr(current_app, 'driver'):
        current_app.driver.close()
        del current_app.driver
