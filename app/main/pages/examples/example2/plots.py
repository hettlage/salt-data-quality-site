import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource
from flask_wtf import Form
from wtforms.fields import DateField
from wtforms.validators import DataRequired

from app import db
from app.main.data_quality import data_quality


@data_quality(name='weather_downtime', caption='Weather downtime for May 2016.')
def weather_downtime_plot(start_date, end_date):
    """Return a <div> element with a weather downtime plot.

    The plot shows the downtime for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the weather downtime plot.
    """

    sql = 'SELECT Date, TimeLostToWeather FROM NightInfo' \
          '       WHERE Date >= \'{start_date}\' AND Date < \'{end_date}\' AND TimeLostToProblems IS NOT NULL' \
        .format(start_date=start_date, end_date=end_date)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    date_formatter = DatetimeTickFormatter(formats=dict(hours=['%e %b %Y'],
                                                        days=['%e %b %Y'],
                                                        months=['%e %b %Y'],
                                                        years=['%e %b %Y']))

    p = figure(title='Weather Downtime',
               x_axis_label='Date',
               y_axis_label='Downtime (seconds)',
               x_axis_type='datetime')
    p.scatter(source=source, x='Date', y='TimeLostToWeather')

    p.xaxis[0].formatter = date_formatter

    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)
