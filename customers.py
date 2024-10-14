from flask import Blueprint, request, jsonify

customers_blueprint = Blueprint('customers', __name__)

# List to keep track of customers, used in customer ID
customer = []

# Create customer
@customers_blueprint.route('/create-customer', methods=['POST'])
def create_customer():
    customer_data = request.get_json()
    customer_id = len(customer) + 1
    new_customer = {
        "age": customer_age,
        "name": customer_data.get('name'),
        "address": customer_data.get('address'),
    }
    customer.append(new_customer)
    return jsonify({"message": "Customer added", "customer": new_customer}), 201

# Update customer
@customer_blueprint.route('/update-custoemr', methods=['PUT'])
def update_customer(customer_id):
    customer_data = request.get_json()
    for i in customer:
        if i['id'] == customer_id:
            i['make'] = car_data.get('make', car['make'])
            i['model'] = car_data.get('model', car['model'])
            i['year'] = car_data.get('year', car['year'])
            i['location'] = car_data.get('location', car['location'])
            i['status'] = car_data.get('status', car['status'])
            return jsonify({"message": "Car updated", "car": car}), 200
    return jsonify({"message": "Car not found"}), 404
