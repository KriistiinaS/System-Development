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




