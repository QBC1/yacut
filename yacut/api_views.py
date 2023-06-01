from http import HTTPStatus

from flask import jsonify, request

from yacut import ALLOWED_CHARACTERS, BASE_URL, app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json()
    try:
        data['custom_id']
    except KeyError:
        data['custom_id'] = get_unique_short_id()

    short_id = data['custom_id']

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage(f'Имя {BASE_URL+short_id} уже занято!')
    for symbol in short_id:
        if symbol not in ALLOWED_CHARACTERS:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({'url_map': url_map.to_dict()}), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    short_id_object = URLMap.query.filter_by(short=short_id).first()
    if short_id_object is None:
        raise InvalidAPIUsage('Указанный id не найден')
    return jsonify({'url': short_id_object.original}), HTTPStatus.OK
