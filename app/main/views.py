import importlib

from flask import render_template
from werkzeug.exceptions import NotFound

from . import main


DATA_QUALITY_ROUTE = '/data-quality/'


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/data-quality/<path:page>')
def data_quality_page(page):
    """Serve a data quality page.

    page must be a directory path relative to /app/main/pages, and the corresponding directory must be a package.

    Params:
    -------
    page: str
        Path of the directory containing the page content.

    """

    page = page.strip('/')
    page = page.replace('/', '.')  # turn directory path into package name
    try:
        dq = importlib.import_module('app.main.pages.' + page, __package__)
    except ImportError:
        raise NotFound
    return render_template('data_quality/data_quality_page.html', title=dq.title(), content=dq.content())

