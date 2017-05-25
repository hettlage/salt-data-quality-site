import datetime

from app.main.data_quality import default_data_quality_content_for_date_range


def title():
    return 'Order'


def content():
    return default_data_quality_content_for_date_range(__package__,
                                                       datetime.date.today() - datetime.timedelta(days=731),
                                                       datetime.date.today())
