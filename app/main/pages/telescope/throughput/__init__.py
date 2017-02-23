import datetime

from app.main.data_quality import default_data_quality_content_for_date_range


def title():
    return 'Telescope throughput'


def content():
    return default_data_quality_content_for_date_range(__package__,
                                                       datetime.date.today() - datetime.timedelta(days=4383),
                                                       datetime.date.today())

