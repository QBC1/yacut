from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from .constants import ALLOWED_CHARACTERS, MAXIMUM_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json()
    invalid_name = InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()

    short_id = data['custom_id']

    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    if len(short_id) > MAXIMUM_LENGTH:
        raise invalid_name
    for symbol in short_id:
        if symbol not in ALLOWED_CHARACTERS:
            raise invalid_name

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    short_id_object = URLMap.query.filter_by(short=short_id).first()
    if short_id_object is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': short_id_object.original}), HTTPStatus.OK
