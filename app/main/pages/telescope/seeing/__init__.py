import  datetime
from dateutil import parser
from flask import g, render_template
from app.decorators import store_query_parameters
from app.main.pages.telescope.seeing.seeing import update
from app.main.seeing_form import SeeingForm


def title():
    return 'Seeing'

def content():
    return seeing_content(default_start_date=datetime.date.today() - datetime.timedelta(days=7),default_end_date= datetime.date.today())

@store_query_parameters(names=('start_date', 'end_date','binning'))
def seeing_content(default_start_date=None, default_end_date=None):
    """Create seeing content for a date range query.

       The seeing  content (as created by _default_data_quality_content) is obtained for an optional binning interval and a date range, which
       the user can select in an input form .

       The start date for the range is inclusive, the end date exclusive.

       Defaults can be supplied for the start and end date.

       The content is created if the form is valid, irrespective of whether a GET or POST request is made. Otherwise only
       the form is included.

       Params:
       -------
       default_start_date: date
           Default start date for the query.
       default_end_date: date
           Default end date for the query.

       """

    form = SeeingForm(default_start_date, default_end_date)

    # update form data from stored parameters
    stored_params = g.stored_query_parameters
    if 'start_date' in stored_params and stored_params['start_date'] != '':
        form.start_date.data = parser.parse(stored_params['start_date'])
    if 'end_date' in stored_params and stored_params['start_date'] != '':
        form.end_date.data = parser.parse(stored_params['end_date'])
    if 'binning' in stored_params and stored_params['start_date'] != '':
        form.binning.data = stored_params['binning']

    if form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
        binning = form.binning.data
        query_results =update(start_date=start_date,end_date=end_date,binning=binning)
    else:
        query_results = ''
    return render_template('data_quality/data_quality_query_page.html', form=form.html(), query_results=query_results)
