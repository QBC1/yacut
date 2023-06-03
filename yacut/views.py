from flask import flash, redirect, render_template

from yacut import app, db
from .constants import ALLOWED_CHARACTERS, BASE_URL
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        short_id = form.custom_id.data

        if short_id is None:
            short_id = get_unique_short_id()

        for symbol in short_id:
            if symbol not in ALLOWED_CHARACTERS:
                flash('Указано недопустимое имя для короткой ссылки')
                return render_template('index.html', form=form)

        if len(short_id) > 0:
            if URLMap.query.filter_by(short=short_id).first():
                flash(f'Имя {short_id} уже занято!')
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()

        short_id_object = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(short_id_object)
        db.session.commit()
        return render_template(
            'index.html', form=form,
            short_url=BASE_URL + short_id_object.short
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def short_link_redirect(short):
    original = URLMap.query.filter_by(short=short).first_or_404().original
    return redirect(original)
