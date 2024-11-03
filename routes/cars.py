from flask import Blueprint, request, jsonify
from model.model import *  # Ensure model functions are imported
from model.model import _get_connection  # Ensure model functions are imported
import json 

car_blueprint = Blueprint('cars', __name__)

# Read all cars 
@car_blueprint.route('/get-cars', methods=['GET'])
def query_records():
    return jsonify(list(findAllCars()))  # Convert generator to list for JSON serialization


# Save a car (fra forelesning)
@car_blueprint.route('/save_car', methods=["POST"])
def save_car_info():
    record = json.loads(request.data)
    print(record)
    return save_car(record['id'], record['make'], record['model'], record['status'], record['year'])


# Update car (fra forelesning)
# The method uses the registration number to find the car
# object from database and updates other informaiton from
# the information provided as input in the json object
@car_blueprint.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['id'], record['make'], record['model'], record['status'], record['year'])

# Delete car (fra forelesning)
# The method uses the registration number to find the car
# object from database and removes the records
@car_blueprint.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['id'])
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

    if cancel_order(customer_id, car_id):
        return jsonify({"message": "Order canceled successfully."}), 200
    else:
        return jsonify({"message": "Failed to cancel order. Please check your IDs."}), 400


# Return a car
@car_blueprint.route('/return-car', methods=['POST'])
def return_car():
    record = json.loads(request.data)  # Parse JSON data
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")
    status = record.get('status')

    if return_car(customer_id, car_id, status):
            return jsonify({"message": "Car returned successfully."}), 200
    else:
        return jsonify({"message": "Failed to return car. Please check your IDs."}), 400




