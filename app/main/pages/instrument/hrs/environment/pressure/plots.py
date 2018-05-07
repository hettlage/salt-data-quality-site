import pandas as pd

from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.decorators import data_quality

# creates your plot
date_formatter = DatetimeTickFormatter(microseconds=['%f'],
                                       milliseconds=['%S.%2Ns'],
                                       seconds=[':%Ss'],
                                       minsec=[':%Mm:%Ss'],
                                       minutes=['%H:%M:%S'],
                                       hourmin=['%H:%M:'],
                                       hours=["%H:%M"],
                                       days=["%d %b"],
                                       months=["%d %b %Y"],
                                       years=["%b %Y"])


@data_quality(name='dew_pressure', caption=' ')
def dew_pressure_plot(start_date, end_date):
    """Return a <div> element with a HRS pressure plot.

    The plot shows the HRS pressure for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the pressure plot.
    """
    title = "DEW Pressure "
    y_axis_label = 'Pressure'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'PRE_DEW'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as PRESSURE, FileName, CONVERT(UTStart,char) AS Time " \
          "     from {table} join FileData using (FileData_Id) " \
          "         where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}"
    sql1 = sql.format(column=column, start_date=start_date, end_date=end_date, table=table, logic=logic)
    sql2 = sql.format(column=column, start_date=start_date, end_date=end_date, table=table, logic=logic2)
    df = pd.read_sql(sql1, db.engine)
    df2 = pd.read_sql(sql2, db.engine)
    source = ColumnDataSource(df)
    source2 = ColumnDataSource(df2)

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
            <div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Date: </span>
                    <span style="font-size: 15px;"> @Time</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Pressure: </span>
                    <span style="font-size: 15px;"> @PRESSURE</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                    <span style="font-size: 15px;"> @FileName</span>
                </div>
            </div>
        """
    )

    p = figure(title=title,
               x_axis_label='Date',
               y_axis_label=y_axis_label,
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='PRESSURE', color='blue', fill_alpha=0.2, size=12, legend='Blue Arm')
    p.scatter(source=source2, x='UTStart', y='PRESSURE', color='red', fill_alpha=0.2, size=10, legend='Red Arm')

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.3
    p.legend.inactive_fill_alpha = 0.8

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='vac_pressure', caption=' ')
def vac_pressure_plot(start_date, end_date):
    """Return a <div> element with a HRS pressure plot.

    The plot shows the HRS pressure for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the pressure plot.
    """
    title = "VAC Pressure "
    y_axis_label = 'Pressure'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'PRE_VAC'
    logic = " and FileName like 'H%%' "
    logic2 = " and FileName like 'R%%' "
    sql = "select UTStart, {column} as PRESSURE, FileName, CONVERT(UTStart,char) AS Time " \
          "     from {table} join FileData using (FileData_Id) " \
          "         where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}"
    sql1 = sql.format(column=column, start_date=start_date, end_date=end_date, table=table, logic=logic)
    sql2 = sql.format(column=column, start_date=start_date, end_date=end_date, table=table, logic=logic2)
    df = pd.read_sql(sql1, db.engine)
    df2 = pd.read_sql(sql2, db.engine)
    source = ColumnDataSource(df)
    source2 = ColumnDataSource(df2)

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
            <div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Date: </span>
                    <span style="font-size: 15px;"> @Time</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Pressure: </span>
                    <span style="font-size: 15px;"> @PRESSURE</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                    <span style="font-size: 15px;"> @FileName</span>
                </div>
            </div>
        """
    )

    p = figure(title=title,
               x_axis_label='Date',
               y_axis_label=y_axis_label,
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='PRESSURE', color='blue', fill_alpha=0.2, size=12, legend='Blue Arm')
    p.scatter(source=source2, x='UTStart', y='PRESSURE', color='red', fill_alpha=0.2, size=10, legend='Red Arm')

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.3
    p.legend.inactive_fill_alpha = 0.8

    p.xaxis[0].formatter = date_formatter

    return p
