# Code is a mix between inspiration from lecture 7 and 8, as well minor adjustments suggested by ChatGPT

from flask import Blueprint, request, jsonify
from model.model import *  # Ensure model functions are imported
from model.model import _get_connection  # Ensure model functions are imported
import json 

car_blueprint = Blueprint('cars', __name__)

# Read all cars 
@car_blueprint.route('/get-cars', methods=['GET'])
def query_records():
    return jsonify(list(findAllCars())), 200  # Convert generator to list for JSON serialization and return 200 OK

# Save a car
@car_blueprint.route('/save_car', methods=["POST"])
def save_car_info():
    record = request.get_json()
    print(record)
    car_data = save_car(record['id'], record['make'], record['model'], record['status'], record['year'], record['location'])
    return jsonify(car_data), 201  # Return 201 for created

# Update car
@car_blueprint.route('/update_car', methods=['PUT'])
def update_car_info():
    record = request.get_json()
    print(record)
    updated_car = update_car(record['id'], record['make'], record['model'], record['status'], record['year'], record['location'])
    return jsonify(updated_car), 200  # Return 200 OK

# Delete car
@car_blueprint.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = request.get_json()
    print(record)
    delete_car(record['id'])
    return jsonify(list(findAllCars())), 200  # Return updated list of cars and 200 OK

# Check the status of the car
@car_blueprint.route('/check-car-status/<int:car_id>', methods=['GET'])
def check_car_status(car_id):
    is_available = check_car_availability(car_id)  # Call the model function
    if is_available:
        return jsonify({"status": "Car is available."}), 200  # Return 200 OK
    else:
        return jsonify({"status": "Car is currently booked/rented."}), 200  # Return 200 OK

# Order a car
@car_blueprint.route('/order-car', methods=['POST'])
def order_car():
    record = request.get_json()
    customer_id = int(record.get("customer_id"))
    car_id = int(record.get("car_id"))
    
    # Check if customer has already booked a car
    if check_if_customer_has_booked(customer_id):
        return jsonify({"message": "Customer already has a booked car."}), 400  # Return 400 Bad Request

    # Check if the car is available
    if not check_car_availability(car_id):
        return jsonify({"message": "Car is not available."}), 404  # Return 404 Not Found
    
    # Check the result
    result = book_car(customer_id, car_id)

    car_nodes = result.single()  # Get the first record if available
    if car_nodes:
        car_data = car_nodes['car']  # Extract the car node
        nodes_json = node_to_json(car_data)  # Convert to JSON
        return jsonify({"message": "Car booked successfully.", "car": nodes_json}), 200  # Return 200 OK
    
    return jsonify({"message": "Failed to book the car."}), 500  # Return 500 Internal Server Error

# Cancel a car order
@car_blueprint.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    record = request.get_json()
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")

    if cancel_order(customer_id, car_id):
        return jsonify({"message": "Order canceled successfully."}), 200  # Return 200 OK
    else:
        return jsonify({"message": "Failed to cancel order. Please check your IDs."}), 400  # Return 400 Bad Request

# Rent a car
@car_blueprint.route('/rent-car', methods=['POST'])
def rent_car_route():
    record = request.get_json()
    customer_id = record.get('customer_id')
    car_id = record.get('car_id')

    # Call the model function
    message, status_code = rent_car(customer_id, car_id)  # Expect a tuple with a message and status code
    return jsonify(message), status_code  # Return the message and status code

# Return a car
@car_blueprint.route('/return-car', methods=['POST'])
def return_rented_car():
    record = request.get_json()
    customer_id = record.get("customer_id")
    car_id = record.get("car_id")

    if return_car(customer_id, car_id, car_condition):
        return jsonify({"message": "Car returned successfully."}), 200  # Return 200 OK
    else:
        return jsonify({"message": "Failed to return car."}), 400  # Return 400 Bad Request
