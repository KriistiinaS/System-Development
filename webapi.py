from flask import Flask
from cars import car_blueprint
from customers import customer_blueprint
from employees import employee_blueprint

webapi = Flask(__name__)

# Register blueprints for modular structure
webapi.register_blueprint(car_blueprint)
webapi.register_blueprint(customer_blueprint)
webapi.register_blueprint(employee_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

# Read all cars
@webapi.route('/cars', methods=['GET'])
def get_cars():
    return jsonify({"cars": cars})

# Create a car
@webapi.route('/create-car', methods=['POST'])
def create_car():
    car_data = request.get_json()
    car_id = len(cars) + 1
    new_car = {
        "id": car_id,
        "make": car_data.get('make'),
        "model": car_data.get('model'),
        "year": car_data.get('year'),
        "location": car_data.get('location'),
        "status": "available"
    }
    cars.append(new_car)
    return jsonify({"message": "Car added", "car": new_car}), 201

# Update car
@webapi.route('/update-car', methods=['PUT'])
def update_car(car_id):
    car_data = request.get_json()
    for car in cars:
        if car['id'] == car_id:
            car['make'] = car_data.get('make', car['make'])
            car['model'] = car_data.get('model', car['model'])
            car['year'] = car_data.get('year', car['year'])
            car['location'] = car_data.get('location', car['location'])
            car['status'] = car_data.get('status', car['status'])
            return jsonify({"message": "Car updated", "car": car}), 200
    return jsonify({"message": "Car not found"}), 404

# Delete car
@webapi.route('/delete-car', methods=['DELETE'])
def delete_car(car_id):
    for car in cars:
        if car['id'] == car_id:
            cars.remove(car)
            return jsonify({"message": "Car deleted"}), 200
    return jsonify({"message": "Car not found"}), 404

if __name__ == '__main__':
    webapi.run(debug=True)


