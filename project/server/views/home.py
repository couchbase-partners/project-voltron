from flask import Blueprint, request, make_response, redirect, jsonify
from project.server import app


home_bp : Blueprint = Blueprint('home', __name__)

@home_bp.route('/api/v1/home', methods=['GET'])
def home():
    resp = {}
    resp['status'] = 'success'
    resp['message'] = 'welcome home'
    return make_response(jsonify(resp)), 200