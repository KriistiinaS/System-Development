from flask import Blueprint, request, jsonif, render_template, request, redirect, url_for
from user import findAllCars
from neo4j import GraphDatabase
from neo4j_driver import _get_connection

car_blueprint = Blueprint('cars', __name__)


# Read all cars
@webapi.route('/get-cars', methods=['GET'])
def query_records():
    return findAllCars()
    
# Create a car
@car_blueprint.route('/create-car', methods=['POST'])
def create_car():
    car_data = request.get_json()
    query = """
    CREATE (car:Car {make: $make, model: $model, year: $year, location: $location, status: 'available'})
    RETURN car
    """
    _get_connection().execute_query(query, make=car_data["make"], model_car_data["model"], year=car_data['year'], location=car_data['location'])
    return jsonify({"message": "Car added successfully!"}), 201

# Update car in Neo4j
@car_blueprint.route('/update-car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car_data = request.get_json()
    query = """
    MATCH (car:Car {id: $car_id})
    SET car.make = $make, car.model = $model, car.year = $year, car.location = $location, car.status = $status
    RETURN car
    """
    updated_car = _get_connection().execute_query(query, car_id=car_id, make=car_data['make'], model=car_data['model'], year=car_data['year'], location=car_data['location'], status=car_data['status'])
    if updated_car:
        return jsonify({"message": "Car updated", "car": updated_car}), 200
    return jsonify({"message": "Car not found"}), 404

# Delete car from Neo4j
@car_blueprint.route('/delete-car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    query = """
    MATCH (car:Car {id: $car_id})
    DETACH DELETE car
    RETURN car
    """
    deleted_car = _get_connection().execute_query(query, car_id=car_id)
    if deleted_car:
        return jsonify({"message": "Car deleted"}), 200
    return jsonify({"message": "Car not found"}), 404


