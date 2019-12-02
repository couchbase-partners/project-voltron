from flask import Blueprint, request, make_response, redirect, jsonify
from project.server import app
from project.server import cb_media


titles_bp : Blueprint = Blueprint('titles', __name__)

@titles_bp.route('/api/v1/title', methods=['GET'])
def home():
    title_id = request.args.get('id')
    title = cb_media.get(title_id).value
    return make_response(jsonify(title)), 200