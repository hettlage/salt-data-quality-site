import pandas as pd

from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter, DEFAULT_DATETIME_FORMATS
from bokeh.palettes import Spectral11
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.decorators import data_quality


def get_source(start_date, end_date, obsmode):
    filename = 'R%%'
    logic = " and OBSMODE='{obsmode}'  " \
            "   and DeltaX > -99 " \
            "   and FileName like '{filename}' " \
            "   and Object = 1  group by UTStart, HrsOrder" \
        .format(filename=filename, obsmode=obsmode)

    sql = "Select UTStart, HrsOrder, AVG(DeltaX) as avg, CONVERT(UTStart,char) AS Time " \
          "     from DQ_HrsArc join FileData using (FileData_Id) " \
          "     where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}" \
        .format(start_date=start_date, end_date=end_date, logic=logic)

    df = pd.read_sql(sql, db.engine)

    groups = pd.qcut(df["HrsOrder"].values, len(Spectral11))
    colors = [Spectral11[xx] for xx in groups.codes]
    df['colors'] = colors

    source = ColumnDataSource(df)
    return source


@data_quality(name='high_resolution', caption='')
def hrs_high_resolution_plot(start_date, end_date):
    """Return a <div> element with the High resolution AVG(DeltaX) vs time.

    The plot shows the AVG(DeltaX) for a set of time

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the High resolution AVG(DeltaX) vs time.
    """

    obsmode = 'HIGH RESOLUTION'
    source = get_source(start_date, end_date, obsmode)

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">AVERAGE: </span>
                        <span style="font-size: 15px;"> @avg</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HrsOrder: </span>
                        <span style="font-size: 15px;"> @HrsOrder</span>
                    </div>
                </div>
                """
    )

    # creates your plot
    date_formats = DEFAULT_DATETIME_FORMATS()
    date_formats['hours'] = ['%e %b %Y']
    date_formats['days'] = ['%e %b %Y']
    date_formats['months'] = ['%e %b %Y']
    date_formats['years'] = ['%e %b %Y']
    date_formatter = DatetimeTickFormatter(formats=date_formats)

    p = figure(title="High Resolution",
               x_axis_label='Date',
               y_axis_label='AVG(DeltaX)',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='avg', color='colors', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='medium_resolution', caption='')
def hrs_medium_resolution_plot(start_date, end_date):
    """
        Return a <div> element with the Medium resolution AVG(DeltaX) vs time.

        The plot shows the AVG(DeltaX) for a set of time

        Params:
        -------
        start_date: date
            Earliest date to include in the plot.
        end_date: date
            Earliest date not to include in the plot.

        Return:
        -------
        str:
            A <div> element with the Medium resolution AVG(DeltaX) vs time.
    """

    obsmode = 'MEDIUM RESOLUTION'
    source = get_source(start_date, end_date, obsmode)

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">AVERAGE: </span>
                        <span style="font-size: 15px;"> @avg</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HrsOrder: </span>
                        <span style="font-size: 15px;"> @HrsOrder</span>
                    </div>
                </div>
                """
    )

    # creates your plot
    date_formats = DEFAULT_DATETIME_FORMATS()
    date_formats['hours'] = ['%e %b %Y']
    date_formats['days'] = ['%e %b %Y']
    date_formats['months'] = ['%e %b %Y']
    date_formats['years'] = ['%e %b %Y']
    date_formatter = DatetimeTickFormatter(formats=date_formats)

    p = figure(title="Medium Resolution",
               x_axis_label='Date',
               y_axis_label='AVG(DeltaX)',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='avg', color='colors', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='low_resolution', caption='')
def hrs_low_resolution_plot(start_date, end_date):
    """
        Return a <div> element with the Low resolution AVG(DeltaX) vs time.

        The plot shows the AVG(DeltaX) for a set of time

        Params:
        -------
        start_date: date
            Earliest date to include in the plot.
        end_date: date
            Earliest date not to include in the plot.

        Return:
        -------
        str:
            A <div> element with the Low resolution AVG(DeltaX) vs time.
    """

    obsmode = 'LOW RESOLUTION'
    source = get_source(start_date, end_date, obsmode)

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">AVERAGE: </span>
                        <span style="font-size: 15px;"> @avg</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HrsOrder: </span>
                        <span style="font-size: 15px;"> @HrsOrder</span>
                    </div>
                </div>
                """
    )

    # creates your plot
    date_formats = DEFAULT_DATETIME_FORMATS()
    date_formats['hours'] = ['%e %b %Y']
    date_formats['days'] = ['%e %b %Y']
    date_formats['months'] = ['%e %b %Y']
    date_formats['years'] = ['%e %b %Y']
    date_formatter = DatetimeTickFormatter(formats=date_formats)

    p = figure(title="Low Resolution",
               x_axis_label='Date',
               y_axis_label='AVG(DeltaX)',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='avg', color='colors', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p
