from flask import Blueprint, request, jsonify
from model.model import *  # Ensure model functions are imported
from model.model import _get_connection
import webapi

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


# Order a car
@car_blueprint.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data.get("customer_id")
    car_id = data.get("car_id")

    # Check if the customer has already booked a car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:BOOKED]->(car:Car)
    RETURN car
    """
    booked_car = _get_connection().execute_query(query, customer_id=customer_id)
    if booked_car:
        return jsonify({"message": "Customer already has a booked car."}), 400

    # Update the car status to 'booked'
    query = """
    MATCH (car:Car {id: $car_id})
    WHERE car.status = 'available'
    SET car.status = 'booked'
    CREATE (customer:Customer {id: $customer_id})-[:BOOKED]->(car)
    RETURN car
    """
    result = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    if result:
        return jsonify({"message": "Car booked successfully."}), 200
    return jsonify({"message": "Car is not available."}), 404


# Cancel a car order
@car_blueprint.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.get_json()
    customer_id = data.get("customer_id")
    car_id = data.get("car_id")

    # Check if the customer has booked the car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:BOOKED]->(car:Car {id: $car_id})
    RETURN car
    """
    booked_car = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    if not booked_car:
        return jsonify({"message": "Customer has not booked this car."}), 404

    # Cancel the booking and set car status to 'available'
    query = """
    MATCH (customer:Customer {id: $customer_id})-[r:BOOKED]->(car:Car {id: $car_id})
    DELETE r
    SET car.status = 'available'
    RETURN car
    """
    _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    return jsonify({"message": "Car booking canceled successfully."}), 200


# Rent a car
@car_blueprint.route('/rent-car', methods=['POST'])
def rent_car():
    data = request.get_json()
    customer_id = data.get("customer_id")
    car_id = data.get("car_id")

    # Check if the customer has a booking for this car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:BOOKED]->(car:Car {id: $car_id})
    RETURN car
    """
    booked_car = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    if not booked_car:
        return jsonify({"message": "Customer has not booked this car."}), 404

    # Update car status to 'rented'
    query = """
    MATCH (customer:Customer {id: $customer_id})-[r:BOOKED]->(car:Car {id: $car_id})
    DELETE r
    SET car.status = 'rented'
    CREATE (customer)-[:RENTED]->(car)
    RETURN car
    """
    _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    return jsonify({"message": "Car rented successfully."}), 200


# Return a car
@car_blueprint.route('/return-car', methods=['POST'])
def return_car():
    data = request.get_json()
    customer_id = data.get("customer_id")
    car_id = data.get("car_id")
    car_status = data.get("car_status", "available")  # Assume 'available' or 'damaged'

    # Check if the customer has rented the car
    query = """
    MATCH (customer:Customer {id: $customer_id})-[:RENTED]->(car:Car {id: $car_id})
    RETURN car
    """
    rented_car = _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id)
    if not rented_car:
        return jsonify({"message": "Customer has not rented this car."}), 404

    # Update car status based on return condition and delete rented relationship
    query = """
    MATCH (customer:Customer {id: $customer_id})-[r:RENTED]->(car:Car {id: $car_id})
    DELETE r
    SET car.status = $car_status
    RETURN car
    """
    _get_connection().execute_query(query, customer_id=customer_id, car_id=car_id, car_status=car_status)
    return jsonify({"message": "Car returned successfully with status '{}'.".format(car_status)}), 200



