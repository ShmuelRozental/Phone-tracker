import os
from flask import current_app
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

def init_driver():
    uri = os.getenv('NEO4J_URI', 'bolt://neo4j:7687')
    username = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password')
    
    current_app.driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_pool_size=20)


def get_driver():
    if not hasattr(current_app, 'driver'):
        print("Driver not initialized.")
        raise ValueError("Driver not initialized.")
    print("Driver retrieved successfully.")
    return current_app.driver

def close_driver():
    if hasattr(current_app, 'driver'):
        current_app.driver.close()
        del current_app.driver
