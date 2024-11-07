# Code is a mix between inspiration from lecture 7 and 8, as well minor adjustments suggested by ChatGPT

from flask import Blueprint, request, jsonify
from model.model import *
import json

# Define the blueprint for employees
employee_blueprint = Blueprint('employees', __name__)

# Create/save an employee
@employee_blueprint.route('/save_employee', methods=['POST'])
def save_employee_info():
    record = request.get_json()
    return jsonify(save_employee(record['name'], record['address'], record['branch'])), 201  # Return 201 for created

# Read all employees
@employee_blueprint.route('/get-employees', methods=['GET'])
def query_employees():
    return jsonify(findAllEmployees()), 200  # Return 200 OK

# Update employee
@employee_blueprint.route('/update_employee', methods=['PUT'])
def update_employee_info():
    record = request.get_json()
    updated_employee = update_employee(record['name'], record['address'], record['branch'])
    if updated_employee:  # Check if update was successful
        return jsonify(updated_employee), 200  # Return 200 OK
    else:
        return jsonify({"error": "Update failed."}), 400  # Return 400 for bad request

# Delete employee
@employee_blueprint.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = request.get_json()
    delete_employee(record['name'])
    return jsonify(findAllEmployees()), 200  # Return 200 OK with updated employee list
