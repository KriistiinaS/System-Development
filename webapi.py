# Code is a mix between inspiration from lecture 7 and 8, as well minor adjustments suggested by ChatGPT

from flask import Flask, render_template, jsonify
from flask_cors import CORS  # Import CORS
from routes.cars import car_blueprint
from routes.customers import customer_blueprint
from routes.employees import employee_blueprint

webapi = Flask(__name__)
CORS(webapi, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})  # Enable CORS 

@webapi.route("/")
def home():
    return render_template("view.html")

# Register blueprints for modular structure
webapi.register_blueprint(car_blueprint)
webapi.register_blueprint(customer_blueprint)
webapi.register_blueprint(employee_blueprint)

if __name__ == '__main__':
    webapi.run(debug=True)

