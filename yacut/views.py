import random
from string import ascii_lowercase, ascii_uppercase, digits

from flask import flash, redirect, render_template

from yacut import BASE_URL, app, db
from .forms import URLForm
from .models import URLMap

allowed_characters = ascii_lowercase + ascii_uppercase + digits


def gen_short_id():
    short_id_length = random.choice(range(1, 17))
    return ''.join([
        random.choice(allowed_characters) for _ in range(short_id_length)
    ])


def get_unique_short_id():
    short_id = gen_short_id()
    while URLMap.query.filter_by(short=short_id).first():
        short_id = gen_short_id()
    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_id = form.short.data

        for symbol in short_id:
            if symbol not in allowed_characters:
                flash('''Найдены неизвестные символы в вашем варианте.
                Используйте только латиницу и целые числа''')
                return render_template('index.html', form=form)

        if len(short_id) > 0:
            if URLMap.query.filter_by(short=short_id).first():
                flash(f'Ссылка {BASE_URL+short_id} уже занята')
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()

        short_id = URLMap(
            original=form.original.data,
            short=short_id
        )
        db.session.add(short_id)
        db.session.commit()
        return render_template(
            'index.html', form=form,
            short_url=BASE_URL + short_id.short
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_link_redirect(short):
    original = URLMap.query.filter_by(short=short).first_or_404().original
    return redirect(original)
