from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample route to test the API
@app.route('/')
def home():
    return "Welcome to my API!"

if __name__ == '__main__':
    app.run(debug=True)
