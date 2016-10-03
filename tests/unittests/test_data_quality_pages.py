import json

from flask import current_app, g, jsonify, request, url_for
from flask_login import login_user, logout_user

from app.decorators import stored_query_parameters
from app.main import main
from app.main.views import DATA_QUALITY_ROUTE
from tests.unittests.base import NoAuthBaseTestCase


@main.route('/echo-parameters', methods=['GET', 'POST', 'PUT'])
@stored_query_parameters(names=('a', 'b', 'c', 'd'))
def echo_parameters():
    merged = g.stored_query_parameters.copy()
    merged.update(request.values)
    return jsonify(merged)


@main.route('/other-page')
def other_page():
    return 'Other'


class DataQualityPagesTestCase(NoAuthBaseTestCase):
    def test_data_quality_page_has_data_quality_content(self):
        """
        When I access a data quality page
        Then the page contains data quality content
        """

        response = self.client.get('/data-quality/examples/example')
        self.assertEquals(200, response.status_code)
        self.assertTrue('class="data-quality"' in response.get_data(as_text=True))

    def test_data_quality_page_uses_title_from_package(self):
        """
        When I access a data quality page
        Then the page title is created by the page's __init__.py file
        """

        response = self.client.get('/data-quality/examples/example')
        self.assertTrue('Example Data Quality Page</title' in response.get_data(as_text=True))

    def test_data_quality_page_uses_content_from_package(self):
        """
        When I access a data quality page
        Then the page content is created by the page's __init__.py file
        """

        response = self.client.get('/data-quality/examples/example')
        self.assertTrue('This is an example.' in response.get_data(as_text=True))

    def test_accessing_non_existing_data_quality_page(self):
        """
        When I access a non-existing data quality page
        Then I get a page not found error
        """

        response = self.client.get('/data-quality/xthdsg73980ui')
        self.assertEquals(404, response.status_code)

    def test_query_parameters_are_remembered(self):
        """
        When I access a suitable page with get and post query parameters
        And I go to another page
        And I return to the page without passing query parameters
        Then the original query parameters are used.
        """

        # go to page
        params = dict(a='1', b='2', c='-42', d='Hello')
        response = self.client.post('{url}?a={a}&b={b}'.format(url='/echo-parameters',
                                                               a=params['a'],
                                                               b=params['b']),
                                    data=dict(c=params['c'], d=params['d']))
        self.assertEquals(200, response.status_code)
        self.assertEquals(params, json.loads(response.data.decode('utf-8')))

        # go to other page
        response = self.client.get('/other-page')
        self.assertEquals(200, response.status_code)

        # return to original page
        response = self.client.get('/echo-parameters')
        self.assertEquals(200, response.status_code)
        self.assertEquals(params, json.loads(response.data.decode('utf-8')))

    def test_stored_query_parameters_are_updated(self):
        """When I access a suitable page with get and post parameters
        And I access the page again with other parameter values
        Then the stored parameter values are updated with the new ones.
        """

        # go to page
        params = dict(a='1', b='2', c='-42', d='Hello')
        response = self.client.post('{url}?a={a}&b={b}'.format(url='/echo-parameters',
                                                               a=params['a'],
                                                               b=params['b']),
                                    data=dict(c=params['c'], d=params['d']))
        self.assertEquals(200, response.status_code)
        self.assertEquals(params, json.loads(response.data.decode('utf-8')))

        # go to the same page with some updated parameter values
        updated_params = dict(a='11', d='World')
        response = self.client.post('{url}?a={a}'.format(url='/echo-parameters',
                                                         a=updated_params['a']),
                                    data=dict(d=updated_params['d']))
        self.assertEquals(200, response.status_code)

        # go to other page
        response = self.client.get('/other-page')
        self.assertEquals(200, response.status_code)

        # return to original page
        merged = params.copy()
        merged.update(updated_params)
        response = self.client.get('/echo-parameters')
        self.assertEquals(200, response.status_code)
        self.assertEquals(merged, json.loads(response.data.decode('utf-8')))



