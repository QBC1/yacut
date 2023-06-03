import random

from .constants import ALLOWED_CHARACTERS
from .models import URLMap


def gen_short_id():
    return ''.join([
        random.choice(ALLOWED_CHARACTERS) for _ in range(6)
    ])


def get_unique_short_id():
    short_id = gen_short_id()
    while URLMap.query.filter_by(short=short_id).first():
        short_id = gen_short_id()
    return short_id