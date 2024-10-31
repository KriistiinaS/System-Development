from flask import Blueprint, request, jsonify
from model.model import *

# Define the blueprint for employees
employee_blueprint = Blueprint('employees', __name__)

# Create/save an employee
@employee_blueprint.route('/save_employee', methods=['POST'])
def save_employee_info():
    record = json.loads(request.data)
    return jsonify(save_employee(record['name'], record['address'], record['branch']))

# Read all employees
@employee_blueprint.route('/get-employees', methods=['GET'])
def query_employees():
    return jsonify(findAllEmployees())

# Update employee
@employee_blueprint.route('/update_employee', methods=['PUT'])
def update_employee_info():
    record = json.loads(request.data)
    return jsonify(update_employee(record['name'], record['address'], record['branch']))

# Delete employee
@employee_blueprint.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data)
    delete_employee(record['name'])
    return jsonify(findAllEmployees())

