import datetime

from app.main.data_quality import default_data_quality_content_for_date_range


def title():
    return 'Robert Stobie Spectrograph'


def content():
    return default_data_quality_content_for_date_range(__package__,
                                                       datetime.date.today() - datetime.timedelta(days=1461),
                                                       datetime.date.today())
