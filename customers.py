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
