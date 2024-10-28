from flask import Blueprint, request, jsonify

employee_blueprint = Blueprint('employee', __name__)

employees = []  # Store employee data here for demo

# Create employee
@employee_blueprint.route('/create-employee', methods=['POST'])
def create_employee():
    employee_data = request.get_json()
    employee_id = len(employees) + 1
    new_employee = {
        "id": employee_id,
        "name": employee_data.get('name'),
        "address": employee_data.get('address'),
        "branch": employee_data.get('branch'),
    }
    employees.append(new_employee)
    return jsonify({"message": "Employee added", "employee": new_employee}), 201

# Update employee
@employee_blueprint.route('/update-employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee_data = request.get_json()
    for i in employees:
        if i['id'] == employee_id:
            i['name'] = employee_data.get('name', i['name'])
            i['address'] = employee_data.get('address', i['address'])
            i['branch'] = employee_data.get('branch', i['branch'])
            return jsonify({"message": "Employee updated", "employee": i}), 200
    return jsonify({"message": "Employee not found"}), 404


# Delete car
@employee_blueprint.route('/delete-employee', methods=['DELETE'])
def delete_employee(employee_id):
    for i in employees:
        if i['id'] == employee_id:
            employees.remove(i)
            return jsonify({"message": "Employee deleted"}), 200
    return jsonify({"message": "Employee not found"}), 404
