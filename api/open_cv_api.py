from flask import Flask, Blueprint, request, jsonify
import open_cv
test_bp = Blueprint('test_api', __name__)

CREATORS = {"0": "Sheshank", "1": "Shubh", "2": "Kriya", "3": "Richard"}

@test_bp.route('/')
def home():
    return "<h1> Hello Dr. Pill! </h1>"

@test_bp.route('/scan_label/')
def scan_label():
    data = open_cv.main()
    return data

@test_bp.route('/creators', methods=['GET'])
def test_creators():
    return jsonify(CREATORS)