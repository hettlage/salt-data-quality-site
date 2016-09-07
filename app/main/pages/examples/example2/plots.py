import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.main.data_quality import data_quality


@data_quality(name='weather_downtime', caption='Weather downtime for May 2016.')
def weather_downtime_plot():
    sql = 'SELECT Date, TimeLostToWeather FROM NightInfo' \
          '       WHERE Date >= \'2016-05-01\' AND Date <= \'2016-05-31\' AND TimeLostToProblems IS NOT NULL'
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
