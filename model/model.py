#Code inspired from slide 42 in lecture 7
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver

URI = "neo4j+s://2c334182.databases.neo4j.io"
AUTH = ("neo4j", "MB20UmadlTYXGV3DiJB1FQh_B6xgzZfORfSahiSixSk")

def _get_connection() -> Driver:
  driver = GraphDatabase.driver(URI, auth=AUTH)
  driver.verify_connectivity()
  return driver
def node_to_json(node):
  node_properties = dict(node.items())
  return node_properties

# Search for all cars
def findAllCars():
  with _get_connection().session() as session:
    cars = session.run("MATCH (a:Car) RETURN a;")
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json
  
# Search by registration number on car
def findCarByReg(reg):
  with _get_connection().session() as session:
    cars = session.run("MATCH (a:Car) where a.reg=Sreg RETURN a;", reg=reg)
    print(cars)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json

# Create/save car
def save_car(make, model, reg, year, capacity):
  cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, capacity:$capacity}) RETURN a;",
    make = make, model = model, reg = reg, year = year, capacity = capacity)
  nodes_json = [node_to_json(record["a"]) for record in cars]
  print(nodes_json)
  return nodes_json

# Update car
def update_car(make, model, reg, year, capacity):
  with _get_connection().session() as session:
    cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.capacity = $capacity RETURN a;",
      reg=reg, make=make, model=model, year=year, capacity=capacity)
    print(cars)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json

#Delete car
def delete_car(reg):
  _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", 
    reg = reg)
  

# Check the status of a car
def check_car_availability(car_id):
    with _get_connection().session() as session:
      result = session.run("""
    MATCH (car:Car {id: $car_id}) 
    OPTIONAL MATCH (customer:Customer)-[:BOOKED]->(car)
    RETURN COUNT(customer) = 0 AS is_available
""", car_id=car_id)
      is_available = result.single()[0]  # Get the boolean value
      return is_available

# ---------------------------------------------------------------------------
# CUSTOMERS

# Create/save customer
def save_customer(name, age, address):
    with _get_connection().session() as session:
        customer = session.run(
            "MERGE (c:Customer {name: $name, age: $age, address: $address}) RETURN c;",
            name=name, age=age, address=address
        )
        nodes_json = [node_to_json(record["c"]) for record in customer]
        print(nodes_json)
        return nodes_json

# Read all customers
def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) RETURN c;")
        nodes_json = [node_to_json(record["c"]) for record in customers]
        print(nodes_json)
        return nodes_json

# Update customer
def update_customer(name, age, address):
    with _get_connection().session() as session:
        customer = session.run(
            "MATCH (c:Customer {name: $name}) SET c.age = $age, c.address = $address RETURN c;",
            name=name, age=age, address=address
        )
        nodes_json = [node_to_json(record["c"]) for record in customer]
        print(nodes_json)
        return nodes_json

# Delete customer
def delete_customer(name):
    with _get_connection().session() as session:
        session.run("MATCH (c:Customer {name: $name}) DELETE c;", name=name)

# Check if a customer has booked a car
def check_if_customer_has_booked(customer_id):
    with _get_connection().session() as session:
        # Query to check if the customer has any bookings
        result = session.run("""
            MATCH (c:Customer)-[:BOOKED]->(car:Car)
            WHERE c.id = $customer_id
            RETURN count(car) > 0 AS has_booked
        """, customer_id=customer_id)
        
        # Fetch the result
        has_booked = result.single()[0]  # Returns True or False
        return has_booked


# --------------------------------------------------------------------------
#EMPLOYEE

# Create/save employee
def save_employee(name, address, branch):
    with _get_connection().session() as session:
        employee = session.run(
            "MERGE (e:Employee {name: $name, address: $address, branch: $branch}) RETURN e;",
            name=name, address=address, branch=branch
        )
        nodes_json = [node_to_json(record["e"]) for record in employee]
        print(nodes_json)
        return nodes_json

# Read all employees
def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) RETURN e;")
        nodes_json = [node_to_json(record["e"]) for record in employees]
        print(nodes_json)
        return nodes_json

# Update employee
def update_employee(name, address, branch):
    with _get_connection().session() as session:
        employee = session.run(
            "MATCH (e:Employee {name: $name}) SET e.address = $address, e.branch = $branch RETURN e;",
            name=name, address=address, branch=branch
        )
        nodes_json = [node_to_json(record["e"]) for record in employee]
        print(nodes_json)
        return nodes_json

# Delete employee
def delete_employee(name):
    with _get_connection().session() as session:
        session.run("MATCH (e:Employee {name: $name}) DELETE e;", name=name)
