from flask import Blueprint, request, jsonify
from model.model import *  # Ensure model functions are imported
from model.model import _get_connection  # Ensure model functions are imported
import json 

car_blueprint = Blueprint('cars', __name__)

# Read all cars 
@car_blueprint.route('/get-cars', methods=['GET'])
def query_records():
    return jsonify(list(findAllCars()))  # Convert generator to list for JSON serialization

# Search car by registration number (fra forelesning)
@car_blueprint.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    record = json.loads(request.data)
    print(record)
    print(record['reg'])
    return findCarByReg(record['reg'])

# Save a car (fra forelesning)
@car_blueprint.route('/save_car', methods=["POST"])
def save_car_info():
    record = json.loads(request.data)
    print(record)
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])


# Update car (fra forelesning)
# The method uses the registration number to find the car
# object from database and updates other informaiton from
# the information provided as input in the json object
@car_blueprint.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# Delete car (fra forelesning)
# The method uses the registration number to find the car
# object from database and removes the records
@car_blueprint.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['reg'])
    return findAllCars()

# Check the status of the car
@car_blueprint.route('/check-car-status/<int:car_id>', methods=['GET'])
def check_car_status(car_id):
    is_available = check_car_availability(car_id)  # Call the model function
    if is_available:
        return jsonify({"status": "Car is available."})
    else:
        return jsonify({"status": "Car is currently booked."})

# Order a car
@car_blueprint.route('/order-car', methods=['POST'])
def order_car():
    record = json.loads(request.data)  # Parse JSON using json.loads(request.data)
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")

    # Check if the customer has already booked a car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:BOOKED]->(car:Car)
    RETURN car
    """
    booked_car = _get_connection().execute_query(query, customer_id=customer_id)
    if booked_car:
        return jsonify({"message": "Customer already has a booked car."}), 400

    # Update the car status to 'booked' and create the relationship
    query = """
    MATCH (car:Car {id: $car_id})
    WHERE car.status = 'available'
    SET car.status = 'booked'
    CREATE (customer:Customer {id: $customer_id})-[:BOOKED]->(car)
    RETURN car
    """
    result = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    nodes_json = [node_to_json(record["car"]) for record in result] if result else None  # Consistent use of nodes_json

    if nodes_json:
        return jsonify({"message": "Car booked successfully.", "car": nodes_json}), 200
    return jsonify({"message": "Car is not available."}), 404



# Cancel a car order
@car_blueprint.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    record = json.loads(request.data)  # Parse JSON data
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")

    # Check if the customer has booked the car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:BOOKED]->(car:Car {id: $car_id})
    RETURN car
    """
    booked_car = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    
    # If no booking relationship exists, return an error
    if not booked_car:
        return jsonify({"message": "Customer has not booked this car."}), 404

    # Cancel the booking and set the car's status to 'available'
    query = """
    MATCH (customer:Customer {id: $customer_id})-[r:BOOKED]->(car:Car {id: $car_id})
    DELETE r
    SET car.status = 'available'
    RETURN car
    """
    result = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    nodes_json = [node_to_json(record["car"]) for record in result] if result else None  # Consistent use of nodes_json

    if nodes_json:
        return jsonify({"message": "Car booking canceled successfully.", "car": nodes_json}), 200
    return jsonify({"message": "Error canceling booking."}), 500



# Rent a car
@car_blueprint.route('/rent-car', methods=['POST'])
def rent_car():
    record = json.loads(request.data)  # Parse JSON data
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")

    # Check if the customer has a booking for this car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:BOOKED]->(car:Car {id: $car_id})
    RETURN car
    """
    booked_car = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    
    # If no booking exists, return an error
    if not booked_car:
        return jsonify({"message": "Customer has not booked this car."}), 404

    # Update car status to 'rented' and change relationship from BOOKED to RENTED
    query = """
    MATCH (customer:Customer {id: $customer_id})-[r:BOOKED]->(car:Car {id: $car_id})
    DELETE r
    SET car.status = 'rented'
    CREATE (customer)-[:RENTED]->(car)
    RETURN car
    """
    result = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    nodes_json = [node_to_json(record["car"]) for record in result] if result else None  # Consistent use of nodes_json

    if nodes_json:
        return jsonify({"message": "Car rented successfully.", "car": nodes_json}), 200
    return jsonify({"message": "Error renting car."}), 500



# Return a car
@car_blueprint.route('/return-car', methods=['POST'])
def return_car():
    record = json.loads(request.data)  # Parse JSON data
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")
    car_status = record.get("car_status", "available")  # Default to 'available' if not provided

    # Check if the customer has rented the car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:RENTED]->(car:Car {id: $car_id})
    RETURN car
    """
    rented_car = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    
    # If no rental relationship exists, return an error
    if not rented_car:
        return jsonify({"message": "Customer has not rented this car."}), 404

    # Update car status based on return condition and delete the RENTED relationship
    query = """
    MATCH (customer:Customer {id: $customer_id})-[r:RENTED]->(car:Car {id: $car_id})
    DELETE r
    SET car.status = $car_status
    RETURN car
    """
    result = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id, car_status=car_status)
    nodes_json = [node_to_json(record["car"]) for record in result] if result else None  # Consistent use of nodes_json

    if nodes_json:
        return jsonify({"message": f"Car returned successfully with status '{car_status}'.", "car": nodes_json}), 200
    return jsonify({"message": "Error returning car."}), 500




