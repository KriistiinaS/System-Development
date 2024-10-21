#Code inspired from slide 42 in lecture 7
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver

URI = "neo4j+s://2c334182.databases.neo4j.io"
AUTH = ("neo4j", "MB20UmadlTYXGV3DiJB1FQh_B6xgzZfORfSahiSixSk")

def _get_connection() -> Driver:
  driver = GraphDatabase.driver(URI, auth=AUTH)
  driver.verify_connectivity()
  return driver

def find_car(car):
  data = _get_connection().execute_query("MATCH (a:Car) where a.car = $car RETURN a;", car=car)
  if len(data[0]) > 0:
    car = Car(car, data[0][0][0]["car"])
    return car
  else:
    return Car(car, "Not found in DB")

#make model year location status
class Car:
  def __init__(self, make, model):
    self.make = make
    self.model = model
