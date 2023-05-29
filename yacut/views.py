from flask import render_template

from yacut import app
from .forms import YacutForm


@app.route('/')
def index_view():
    form = YacutForm()
    return render_template('index.html', form=form)
