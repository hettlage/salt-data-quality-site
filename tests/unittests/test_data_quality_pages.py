from flask import current_app, url_for
from flask_login import login_user, logout_user

from app.main.views import DATA_QUALITY_ROUTE
from tests.unittests.base import NoAuthBaseTestCase


class DataQualityPagesTestCase(NoAuthBaseTestCase):
    def test_data_quality_page_has_data_quality_content(self):
        """
        When I access a data quality page
        Then the page contains data quality content
        """

        response = self.client.get('/data-quality/example')
        self.assertEquals(200, response.status_code )
        self.assertTrue('class="data-quality"' in response.get_data(as_text=True))

    def test_data_quality_page_uses_title_from_package(self):
        """
        When I access a data quality page
        Then the page title is created by the page's __init__.py file
        """

        response = self.client.get('/data-quality/example')
        self.assertTrue('Example Data Quality Page</title' in response.get_data(as_text=True))

    def test_data_quality_page_uses_content_from_package(self):
        """
        When I access a data quality page
        Then the page content is created by the page's __init__.py file
        """

        response = self.client.get('/data-quality/example')
        self.assertTrue('This is an example.' in response.get_data(as_text=True))

    def test_accessing_non_existing_data_quality_page(self):
        """
        When I access a non-existing data quality page
        Then I get a page not found error
        """

        response = self.client.get('/data-quality/xthdsg73980ui')
        self.assertEquals(404, response.status_code)



