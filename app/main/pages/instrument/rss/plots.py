import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter, DEFAULT_DATETIME_FORMATS
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

from app import db
from app.decorators import data_quality
from app.main.data_quality_plots import data_quality_date_plot

from math import pi

# One plot for zero articulation setting closed dome test
@data_quality(name='rss_straylight_zero', caption='')
def rss_straylight_zero_plot(start_date, end_date):
    return _rss_straylight_plot(0.0, start_date, end_date)


# One plot for ninety articulation setting closed dome test
@data_quality(name='rss_straylight_ninety', caption='')
def rss_straylight_ninety_plot(start_date, end_date):
    return _rss_straylight_plot(90.25, start_date, end_date)


def _rss_straylight_plot(articulation, start_date, end_date):
    """Return a <div> element with a RSS Straylight plot.

    The plots show the average counts in six detector regions of RSS taken
    from standard closed dome straylight tests (one plot for articulation=0, one for articulation=90.25)
    To measure stray light on RSS, we split up the product RSS frame into 6 regions:
     ___________
    |   |   |   |
    | 1 | 3 | 5 |
    |___|___|___|
    |   |   |   |
    | 2 | 4 | 6 |
    |___|___|___|

    The plot is made for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    articulation: degrees (float - %.2f)
        RSS camera articulation angle; either 0 or 90.25
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the plot.
    """

    # title with articulation angle to 2 decimal points
    title = "RSS Straylight @ {0:.2f} deg" .format(articulation)
    y_axis_label = 'Average Counts'

    # creates your query
    table = 'RssStrayLight'
    # query only selects rows with camang that are specified by articulation
    sql = "select UTStart,mean_z1,mean_z2,mean_z3,mean_z4,mean_z5,mean_z6 from RssStrayLight" \
          "       join FileData using (FileData_Id)" \
          "       join FitsHeaderRss using (FileData_Id)" \
          "       join FitsHeaderImage using (FileData_Id)" \
          "       where UTStart > '{start_date}' and UTStart <'{end_date}' and CAMANG='{camang}'"\
        .format(start_date=start_date, end_date=end_date, camang=articulation)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    # creates your plot
    date_formats = DEFAULT_DATETIME_FORMATS()
    date_formats['hours'] = ['%e %b %Y']
    date_formats['days'] = ['%e %b %Y']
    date_formats['months'] = ['%e %b %Y']
    date_formats['years'] = ['%e %b %Y']
    date_formatter = DatetimeTickFormatter(formats=date_formats)

    p = figure(title=title,
               x_axis_label='UTStart',
               y_axis_label=y_axis_label,
               x_axis_type='datetime')
    # creating line and circle sepearately; fill_alpha gives a bit of transparency to the circles
    # legends are easily added with legend=...
    p.line(x='UTStart', y='mean_z1', color='red', source=source, legend='z1')
    p.circle(x='UTStart', y='mean_z1', color='red', fill_alpha=0.2, size=10, source=source, legend='z1')

    p.line(x='UTStart', y='mean_z2', color='magenta', source=source, legend='z2')
    p.circle(x='UTStart', y='mean_z2', color='magenta', fill_alpha=0.2, size=10, source=source, legend='z2')

    p.line(x='UTStart', y='mean_z3', color='blue', source=source, legend='z3')
    p.circle(x='UTStart', y='mean_z3', color='blue', fill_alpha=0.2, size=10, source=source, legend='z3')

    p.line(x='UTStart', y='mean_z4', color='orange', source=source, legend='z4')
    p.circle(x='UTStart', y='mean_z4', color='orange', fill_alpha=0.2, size=10, source=source, legend='z4')

    p.line(x='UTStart', y='mean_z5', color='green', source=source, legend='z5')
    p.circle(x='UTStart', y='mean_z5', color='green', fill_alpha=0.2, size=10, source=source, legend='z5')

    p.line(x='UTStart', y='mean_z6', color='purple', source=source, legend='z6')
    p.circle(x='UTStart', y='mean_z6', color='purple', fill_alpha=0.2, size=10, source=source, legend='z6')

    p.xaxis[0].formatter = date_formatter

    return p


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
    table = 'PipelineDataQuality_CCD'
    logic = " and FileName like 'P%%' and Target_Name='BIAS'"
    y_axis_label = 'Bias Background Mean (e)'
    return data_quality_date_plot(start_date, end_date, title, column, table, logic=logic, y_axis_label=y_axis_label)

# plot for RSS throughput
@data_quality(name='rss_throughput', caption='RSS Throughput')
def rss_throughput_plot(start_date, end_date):
    """Return a <div> element with a plot displaying the Rss throughput.

    The plot shows the Rss throughput for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the Rss throughput plot.
    """

    return _throughput_plot('RssThroughput', 'RSS Throughput', start_date, end_date)


def _throughput_plot(throughput_column, title, start_date, end_date):
    """Return a <div> element with a throughput plot.

    The plot shows the throughput for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------RSS Throughput
    throughput_column: str
        Name of the column in the Throughput table whose data shall be used.
    title: str
        Plot title.
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    bokeh.model.Model:
        The throughput plot.
    """

    sql = 'SELECT Date, {throughput_column}, StarsUsed, IFNULL(Comments, "No comments") AS Comments, ' \
          ' CONVERT(Date,char) AS Time ' \
          '       FROM Throughput join NightInfo using(NightInfo_Id) ' \
          '       WHERE Date >= \'{start_date}\' AND Date < \'{end_date}\' AND {throughput_column} > 0' \
        .format(start_date=start_date, end_date=end_date, throughput_column=throughput_column)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    date_formatter = DatetimeTickFormatter(formats=dict(
        microseconds=['%f'],
        milliseconds=['%S.%3Ns'],
        seconds=[':%Ss'],
        minsec=[':%Mm:%Ss'],
        minutes=['%H:%M:%S'],
        hourmin=['%H:%M:'],
        hours=["%H:%M"],
        days=["%d %b"],
        months=["%d %b %Y"],
        years=["%b %Y"],
    ))

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
            <div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Date: </span>
                    <span style="font-size: 15px;"> @Time</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Star used: </span>
                    <span style="font-size: 15px;"> @StarsUsed</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Comment: </span>
                </div>
                <div>
                    <span style="font-size: 15px;"> @Comments</span>
                </div>
            </div>
            """
    )

    p = figure(title=title,
               x_axis_label='Time',
               y_axis_label="RSS throughput",
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='Date', y='{throughput_column}'.format(throughput_column=throughput_column),
              color='blue', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter
    p.xaxis.major_label_orientation = pi / 4

    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)
