from flask import Flask, jsonify, request, Response
from flask_caching import Cache
import json
import datetime

from data_base.session import create_session, global_init

global_init("test.sqlite")

from data_base.models.direction import Direction
from api.compare import calculate_academy_credit
from flask_cors import CORS

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)


@app.route('/api/direction_list', methods=['GET'])
@cache.cached(timeout=50, key_prefix='all_comments')
def get_numbers():
    db_sess = create_session()
    direction_list = [direction.name for direction in
                      db_sess.query(Direction).filter(Direction.curriculum != None).all()]
    return Response(json.dumps(direction_list, ensure_ascii=False),
                    status=200, content_type='application/json; charset=utf-8')


@app.route('/api/academic_credit_calculator', methods=['POST'])
def calculate_squares():
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400

    input_json = request.get_json()

    answer_json = calculate_academy_credit(input_json["direction_name"],
                                           input_json["semestr"],
                                           input_json["diciplines"])

    return Response(json.dumps(answer_json, ensure_ascii=False),
                    status=200, content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    app.run(host="0.0.0.0", )
