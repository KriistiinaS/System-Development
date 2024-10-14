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
        "id": customer_id,
        "age": customer_age,
        "name": customer_data.get('name'),
        "address": customer_data.get('address'),
    }
    customer.append(new_customer)
    return jsonify({"message": "Customer added", "customer": new_customer}), 201

# Update customer
@customer_blueprint.route('/update-customer', methods=['PUT'])
def update_customer(customer_id):
    customer_data = request.get_json()
    for i in customer:
        if i['id'] == customer_id:
            i['age'] = customer_data.get('age', i['age'])
            i['name'] = customer_data.get('name', i['name'])
            i['address'] = customer_data.get('address', i['address'])
            return jsonify({"message": "Customer updated", "customer": i}), 200
    return jsonify({"message": "Customer not found"}), 404
