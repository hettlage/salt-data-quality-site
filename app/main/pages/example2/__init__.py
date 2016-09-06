from app.main.data_quality import default_data_quality_page


def title():
    return 'Example 2'


def content():
    return default_data_quality_page(__package__)
