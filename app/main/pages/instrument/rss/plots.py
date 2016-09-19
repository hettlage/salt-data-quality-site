import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.main.data_quality import data_quality


@data_quality(name='rss_bias', caption='Mean RSS Bias Background levels')
def rss_bias_plot(start_date, end_date):
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
    title = "RSS Bias Levels"
    column = 'BkgdMean'
    start_date='2016-05-01'
    end_date='2016-06-01'
    sql = "select UTStart, {column} from PipelineDataQuality_CCD join FileData using (FileData_Id) where UTStart > '{start_date}' and UTStart <'{end_date}' and FileName like 'P%%' and Target_Name='BIAS'".format(column=column, start_date=start_date, end_date=end_date)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    date_formatter = DatetimeTickFormatter(formats=dict(hours=['%e %b %Y'],
                                                        days=['%e %b %Y'],
                                                        months=['%e %b %Y'],
                                                        years=['%e %b %Y']))

    p = figure(title=title,
               x_axis_label='Date',
               y_axis_label='Bias Background Mean (e)',
               x_axis_type='datetime')
    p.scatter(source=source, x='UTStart', y=column)

    p.xaxis[0].formatter = date_formatter

    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)

