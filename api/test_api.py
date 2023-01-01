from flask import Flask, Blueprint, request, jsonify
test_bp = Blueprint('test_api', __name__)

CREATORS = {"0": "Sheshank", "1": "Shubh", "2": "Kriya", "3": "Richard"}

@test_bp.route('/')
def home():
    return "<h1> Hello Dr. Pill! </h1>"

@test_bp.route('/test_page/')
def test():
    return "<h1> This is the test page. </h1>"

@test_bp.route('/creators', methods=['GET'])
def test_creators():
    return jsonify(CREATORS)
    