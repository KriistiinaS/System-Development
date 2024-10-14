from flask import Flask, request, jsonify

webapi = Flask(__name__)

# Temporary storage for cars
cars = []

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

# Read all cars
@webapi.route('/cars', methods=['GET'])
def get_cars():
    return jsonify({"cars": cars})

# Update and delete would follow similar logic.

if __name__ == '__main__':
    webapi.run(debug=True)


