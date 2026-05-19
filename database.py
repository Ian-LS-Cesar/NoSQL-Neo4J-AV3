from neo4j import GraphDatabase
import os

URI = os.getenv("APP_NEO4J_URI", "bolt://neo4j-db:7687")
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

class Neo4jHandler:
    def __init__(self):
        # Create driver instance
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def execute_read(self, query: str, parameters: dict = None):
        """Execute a read (query) and return list of dicts."""
        parameters = parameters or {}
        with self.driver.session() as session:
            result = session.run(query, **parameters)
            return [record.data() for record in result]

    def execute_write(self, query: str, parameters: dict = None):
        """Execute a write transaction and return list of dicts."""
        parameters = parameters or {}
        with self.driver.session() as session:
            result = session.run(query, **parameters)
            return [record.data() for record in result]

    def close(self):
        self.driver.close()

db = Neo4jHandler()