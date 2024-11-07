# Code inspired from slide 42 in lecture 7 as well as some adjustments made by ChatGPT

from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
import json

URI = "neo4j+s://1ac4c339.databases.neo4j.io"
AUTH = ("neo4j", "F0bz3KFbwNTMF_Y_RTgy0VBpiWeAviD_kphn4BK3tYY")

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
  
# Create/save car
def save_car(id, make, model, status, condition, year, location):
  with _get_connection().session() as session:
    cars = _get_connection().session.run("MERGE (a:Car{id: $id, make: $make, model: $model, status: $status, condition: $condition, year: $year, location: $location}) RETURN a;",
      id = id, make = make, model = model, status = status, condition = condition, year = year, location = location)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json

# Update car
def update_car(id, make, model, status, condition, year, location):
  with _get_connection().session() as session:
    cars = session.run("MATCH (a:Car{id:$id}) SET a.make=$make, a.model=$model, a.status=$status, a.condition=$condition, a.year=$year , a.location=$location RETURN a;",
            id = id, make = make, model = model, status = status, condition = condition, year = year, location = location)
    print(cars)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json

#Delete car
def delete_car(id):
    with _get_connection().session() as session:  # Get a session
      session.run("MATCH (a:Car{id: $id}) DELETE a;", id=id)


# Check the status of a car (availability)
def check_car_availability(car_id):
    with _get_connection().session() as session:
        result = session.run(
            "MATCH (car:Car {id: $car_id}) RETURN car.status AS status",
            car_id=car_id
        )
        
        # Retrieve the status
        record = result.single()
        
        if record:
            status = record["status"]
            print(f"Car ID: {car_id}, Status: {status}")  # Debug output
            return status == "available"  # Returns True if the car is available
        else:
            print(f"Car ID: {car_id} not found.")  # Debug output
            return True  # If no car is found, consider it available

# Check condition of car
def check_car_condition(car_id):
    with _get_connection().session() as session:
        result = session.run(
            "MATCH (car:Car {id: $car_id}) RETURN car.condition AS condition",
            car_id=car_id
        )

        # Retrieve car condition
        record = result.single()

        if record:
            condition = record["condition"]
            if condition is None:
                print(f"Car ID: {car_id} has no condition set.")  # Debug output
                return False  # Return False if condition is not set
            print(f"Car ID: {car_id}, Condition: {condition}")  # Debug output

            if condition == "damaged":
                return False
            else:
                return True
        else:
            print(f"Car ID: {car_id} not found.")  # Debug output
            return False  # If car doesn't exist, return False


def book_car(customer_id, car_id):
    #Update the car status to 'booked' and create the relationship
    query = """
    MATCH (car:Car {id: $car_id})
    WHERE car.status = 'available' AND car.condition <> 'damaged'
    MATCH (customer:Customer {id: $customer_id})
    SET car.status = 'booked'
    MERGE (customer)-[:BOOKED]->(car)
    RETURN car
    """
    result = _get_connection().session().run(query, customer_id=customer_id, car_id=car_id)
    return result

# Cancel an order
def cancel_order(customer_id, car_id):
    with _get_connection().session() as session:
        result = session.run("""
            MATCH (customer:Customer {id: $customer_id})-[b:BOOKED]->(car:Car {id: $car_id})
            DELETE b 
            SET car.status = 'available'
            RETURN COUNT(b) AS bookings_deleted
            """, customer_id=customer_id, car_id=car_id)

        # Get the count of deleted bookings
        bookings_deleted = result.single()
        return bookings_deleted["bookings_deleted"] > 0 if bookings_deleted else False

# Rent car
def rent_car(customer_id, car_id):   
    # Convert IDs to integers
    customer_id = int(customer_id)
    car_id = int(car_id)

    # Check if the customer has booked the car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[b:BOOKED]->(car:Car {id: $car_id})
    RETURN car, customer
    """
    result = _get_connection().session().run(query, customer_id=customer_id, car_id=car_id)
    record = result.single()

    # Check if the booking exists
    if record is None:
        return {"error": "This customer did not book the car."}, 403
    else:
        # Update the car status to 'rented' and create the relationship
        update_query = """
        MATCH (car:Car {id: $car_id})
        MATCH (customer:Customer {id: $customer_id})
        MATCH (customer)-[b:BOOKED]->(car)
        SET car.status = 'rented'
        MERGE (customer)-[:RENTED]->(car)
        DELETE b
        RETURN car
        """
        update_result = _get_connection().session().run(update_query, customer_id=customer_id, car_id=car_id)

        if update_result.single() is None:
            return {"error": "Could not update car status."}, 500

        return {"message": "Car rented successfully."}, 200


# Return a car
def return_car(customer_id, car_id, car_condition):
    with _get_connection().session() as session:
        
        # Checking that customer has rented the car
        query = """
        MATCH (customer:Customer {id: $customer_id})-[r:RENTED]->(car:Car {id: $car_id})
        RETURN car, customer
        """
        result = session.run(query, customer_id=customer_id, car_id=car_id)
        record = result.single()
        
        # Check if the rental exists
        if record is None:
            return {"error": "This customer did not rent the car."}, 403

        # Checking if car is damaged
        if car_condition == 'damaged':
            update_query = """
            MATCH (c:Customer)-[b:RENTED]->(car:Car {id: $car_id})
            WHERE c.id = $customer_id
            SET car.status = 'damaged', car.condition = 'damaged'
            DELETE b
            """
        else:
            update_query = """
            MATCH (c:Customer)-[b:RENTED]->(car:Car {id: $car_id}) 
            WHERE c.id = $customer_id 
            SET car.status = 'available' , car.condition = 'ok'
            DELETE b
            """
        
        update_result = session.run(update_query, customer_id=customer_id, car_id=car_id)

        # Check how many relationships were deleted
        deleted_count = update_result.consume().counters.relationships_deleted
        return deleted_count > 0  # Return True if successful
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
