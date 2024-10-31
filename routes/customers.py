from flask import Blueprint, request, jsonify
from model.model import *  # Ensure model functions are imported
from model.model import _get_connection
import webapi

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

