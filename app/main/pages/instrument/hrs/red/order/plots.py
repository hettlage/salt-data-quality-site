import pandas as pd

from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter, DEFAULT_DATETIME_FORMATS
from bokeh.palettes import Plasma256
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.decorators import data_quality


def get_position_source(start_date, end_date, obsmode):
    logic = "   and HrsMode_Id = {obsmode} " \
            "   and FileName like 'RORDER%%' " \
        .format(obsmode=obsmode)
    sql = "select Date, y_upper, HrsOrder, CONVERT(Date,char) AS Time " \
          "     from DQ_HrsOrder join NightInfo using (NightInfo_Id) " \
          "     where Date > '{start_date}' and Date <'{end_date}' {logic}" \
        .format(start_date=start_date, end_date=end_date, logic=logic)
    df = pd.read_sql(sql, db.engine)
    colors = []
    if len(df) > 0:
        ord_min = df['HrsOrder'].min()
        ord_max = df['HrsOrder'].max()
        colors = [Plasma256[int((y - ord_min) * (len(Plasma256) - 1) / float(ord_max - ord_min))] for y in
                  df["HrsOrder"]]

    df['colors'] = colors

    source = ColumnDataSource(df)
    return source


@data_quality(name='hrs_order', caption='HRS Order')
def hrs_order_plot(start_date, end_date):
    """Return a <div> element with the Order plot.

    The plot shows the HRS order for obsmode High, low and medium over time

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the Order plot.
    """

    def get_source(obsmode):
        logic = "   and HrsMode_Id = {obsmode} " \
                "   and FileName like 'RORDER%%' " \
                "   group by Date " \
            .format(obsmode=obsmode)
        sql = "select Date, (Max(HrsOrder) - Min(HrsOrder)) as ord, CONVERT(Date, char) AS Time " \
              "     from DQ_HrsOrder join NightInfo using (NightInfo_Id) " \
              "     where Date > '{start_date}' and Date <'{end_date}' {logic}" \
            .format(start_date=start_date, end_date=end_date, logic=logic)
        df = pd.read_sql(sql, db.engine)

        source = ColumnDataSource(df)
        return source

    low_source = get_source(1)  # HrsMode_Id = 1 low
    med_source = get_source(2)  # HrsMode_Id = 2 med
    high_source = get_source(3)  # HrsMode_Id = 3 high

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HrsOrder(Max - Min): </span>
                        <span style="font-size: 15px;"> @ord</span>
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

    p = figure(title="HRS Order",
               x_axis_label='Date',
               y_axis_label='Max(HrsOrder) - Min(HrsOrder)',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=low_source, x='Date', y='ord', color='red', fill_alpha=0.2, legend='Low', size=10)
    p.scatter(source=med_source, x='Date', y='ord', color='orange', fill_alpha=0.2, legend='Medium', size=10)
    p.scatter(source=high_source, x='Date', y='ord', color='green', fill_alpha=0.2, legend='High', size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='hrs_order_position_high', caption=' ')
def hrs_order_position_plot(start_date, end_date):
    """
        Return a <div> element with the Order Position plot.

        The plot shows the HRS order for obsmode High resolution over time

        Params:
        -------
        start_date: date
            Earliest date to include in the plot.
        end_date: date
            Earliest date not to include in the plot.

        Return:
        -------
        str:
            A <div> element with the Order Position plot.
    """

    high_source = get_position_source(start_date, end_date, 3)  # HrsMode_Id = 3 high

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Y Upper: </span>
                        <span style="font-size: 15px;"> @y_upper</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HRS Order: </span>
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

    p = figure(title="HRS Order Position High Resolution",
               x_axis_label='Date',
               y_axis_label='y_upper',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=high_source, x='Date', y='y_upper', color='colors', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='hrs_order_position_medium', caption=' ')
def hrs_order_position_plot(start_date, end_date):
    """
        Return a <div> element with the Order Position plot.

        The plot shows the HRS order for obsmode High resolution over time

        Params:
        -------
        start_date: date
            Earliest date to include in the plot.
        end_date: date
            Earliest date not to include in the plot.

        Return:
        -------
        str:
            A <div> element with the Order Position plot.
    """

    high_source = get_position_source(start_date, end_date, 2)  # HrsMode_Id = 3 high

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Y Upper: </span>
                        <span style="font-size: 15px;"> @y_upper</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HRS Order: </span>
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

    p = figure(title="HRS Order Position Medium Resolution",
               x_axis_label='Date',
               y_axis_label='y_upper',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=high_source, x='Date', y='y_upper', color='colors', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='hrs_order_position_low', caption=' ')
def hrs_order_position_plot(start_date, end_date):
    """
        Return a <div> element with the Order Position plot.

        The plot shows the HRS order for obsmode High resolution over time

        Params:
        -------
        start_date: date
            Earliest date to include in the plot.
        end_date: date
            Earliest date not to include in the plot.

        Return:
        -------
        str:
            A <div> element with the Order Position plot.
    """

    high_source = get_position_source(start_date, end_date, 3)  # HrsMode_Id = 3 high

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Y Upper: </span>
                        <span style="font-size: 15px;"> @y_upper</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">HRS Order: </span>
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

    p = figure(title="HRS Order Position Low Resolution",
               x_axis_label='Date',
               y_axis_label='y_upper',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=high_source, x='Date', y='y_upper', color='colors', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p