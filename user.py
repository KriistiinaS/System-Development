#Code inspired from slide 42 in lecture 7
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+s://2c334182.databases.neo4j.io"
AUTH = ("neo4j", "MB20UmadlTYXGV3DiJB1FQh_B6xgzZfORfSahiSixSk")

def _get_connection() -> Driver:
  driver = GraphDatabase.driver(URI, auth=AUTH)
  driver.verify_connectivity()
  return driver
def node_to_json(node):
  node_properties = dict(node.items())
  return node_properties

def findAllCars():
  with _get_connection().session() as session:
    cars = session.run("MATCH (a:Car) RETURN a;")
    nodes_json = (node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json
