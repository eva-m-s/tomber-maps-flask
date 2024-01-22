from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
from data import graves, graveyards
from utils.path import Path

app = Flask(__name__)
CORS(app)


@app.route('/generate_path', methods=['POST'])
def generate_path():
    path_data = request.json
    graveyard_id = path_data.get('id')
    coords = path_data.get('coordinates')
    path_instance = Path(graveyard_id, graveyards, coords)
    path = path_instance.a_star_algorithm(coords)  # Provide start and stop coordinates
    if path:
        formatted_path = {
            'nodes': [[coord[0], coord[1]] for coord in path]
        }
        return jsonify(formatted_path)
    else:
        return jsonify({'error': 'Path not found'}), 404


@app.route('/api/graves', methods=['GET'])
def get_graves():
    return jsonify(graves)


@app.route('/api/graveyards', methods=['GET'])
def get_graveyards():
    return jsonify(graveyards)


if __name__ == '__main__':
    app.run(debug=True)
