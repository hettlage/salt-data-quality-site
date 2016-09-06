import importlib

from flask import render_template
from werkzeug.exceptions import NotFound

from . import main


DATA_QUALITY_ROUTE = '/data-quality/'


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/data-quality/<item>')
def data_quality_page(item):
    try:
        dq = importlib.import_module('app.main.pages.' + item, __package__)
    except ImportError:
        raise NotFound
    return render_template('data_quality/data_quality_page.html', title=dq.title(), content=dq.content())

