from app.main.data_quality import seeing_content
import  datetime

def title():
    return 'Seeing'

def content():
    return seeing_content(default_start_date=datetime.date.today() - datetime.timedelta(days=7),default_end_date= datetime.date.today())