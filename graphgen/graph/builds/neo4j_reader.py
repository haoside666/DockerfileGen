from queue import Queue

from graphgen.config.definitions import ROOT_DIR
from graphgen.config.db_config import *

from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PWD))

    def close(self):
        self.driver.close()

    def run_script(self, script):
        with self.driver.session() as session:
            session.run(script)
        print("执行脚本成功")


if __name__ == "__main__":
    conn = Neo4jConnection()
    with open(f"{ROOT_DIR}/graph/script/script.cypher", "r") as file:
        cypher_script = file.read()
    conn.run_script(cypher_script)
    conn.close()
