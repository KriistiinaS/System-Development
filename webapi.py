from flask import Flask
from cars import car_blueprint
from customers import customers_blueprint
from employees import employee_blueprint

webapi = Flask(__name__)

@webapi.route("/")
def home():
    return "<p>Welcome to the Car Rental!</p>"

# Register blueprints for modular structure
webapi.register_blueprint(car_blueprint)
webapi.register_blueprint(customers_blueprint)
webapi.register_blueprint(employee_blueprint)

if __name__ == '__main__':
    webapi.run(debug=True)

