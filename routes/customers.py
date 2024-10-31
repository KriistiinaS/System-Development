from flask import Blueprint, request, jsonify
from model.model import *  # Ensure model functions are imported
from model.model import _get_connection

customer_blueprint = Blueprint('customers', __name__)

# Create/save a customer
@customer_blueprint.route('/save_customer', methods=['POST'])
def save_customer_info():
    record = json.loads(request.data)
    return jsonify(save_customer(record['name'], record['age'], record['address']))

# Read all customers
@customer_blueprint.route('/get-customers', methods=['GET'])
def query_customers():
    return jsonify(findAllCustomers())

# Update customer
@customer_blueprint.route('/update_customer', methods=['PUT'])
def update_customer_info():
    record = json.loads(request.data)
    return jsonify(update_customer(record['name'], record['age'], record['address']))

# Delete customer
@customer_blueprint.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data)
    delete_customer(record['name'])
    return jsonify(findAllCustomers())


# Check if a customer has booked a car
@customer_blueprint.route('/check-booking/<int:customer_id>', methods=['GET'])
def check_booking(customer_id):
    has_booked = check_if_customer_has_booked(customer_id)  # Call the model function
    if has_booked:
        return jsonify({"message": "Customer has booked a car and cannot book another."})
    else:
        return jsonify({"message": "Customer can book a car!"})

# Book the car
@customer_blueprint.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    
    if check_if_customer_has_booked(customer_id):
        return jsonify({"message": "Customer has already booked a car."}), 400
    
    if not check_car_availability(car_id):
        return jsonify({"message": "Car is not available."}), 400

    # Logic to book the car
    # You may want to create a relationship here to signify the booking
    with _get_connection().session() as session:
        session.run("""
            MATCH (c:Customer), (car:Car)
            WHERE c.id = $customer_id AND car.id = $car_id
            CREATE (c)-[:BOOKED]->(car)
        """, customer_id=customer_id, car_id=car_id)

    return jsonify({"message": "Car booked successfully!"})  # Modify based on your logic
