import pandas as pd

from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter, DEFAULT_DATETIME_FORMATS
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.decorators import data_quality
from app.main.data_quality_plots import data_quality_date_plot


@data_quality(name='ccd_temp', caption='')
def ccd_temp_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS CCD Temp"
    y_axis_label = 'Temperature (K)'

    # creates your query
    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 15px; font-weight: bold;">Date: </span>
                <span style="font-size: 15px;"> @Time</span>
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold;">Pixel Position: </span>
                <span style="font-size: 15px;"> @TEM_VAC</span>
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date',
               y_axis_label=y_axis_label,
               x_axis_type='datetime',
               tools=[tool_list, _hover])

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_xcam', caption='')
def temp_xcam_plot(start_date, end_date):
    """Return a <div> element with a HRS RCAM and BCAM temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS RCAM and HCAM Temp"
    y_axis_label = 'Temperature'

    # creates your query
    table = 'FitsHeaderHrs'
    column1 = 'TEM_BCAM'
    column2 = 'TEM_RCAM'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as TEMP, FileName, CONVERT(UTStart,char) AS Time " \
          "     from {table} join FileData using (FileData_Id) " \
          "         where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}"
    sql1 = sql.format(column=column1, start_date=start_date, end_date=end_date, table=table, logic=logic)
    sql2 = sql.format(column=column2, start_date=start_date, end_date=end_date, table=table, logic=logic2)

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
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=12)
    p.scatter(source=source2, x='UTStart', y='TEMP', color='red', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_air', caption='')
def temp_air_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS Air Temp"
    y_axis_label = 'Temperature (K)'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'TEM_AIR'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as TEMP, FileName, CONVERT(UTStart,char) AS Time " \
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
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=12)
    p.scatter(source=source2, x='UTStart', y='TEMP', color='red', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_vac', caption='')
def temp_vac_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS Vacuum Temp"
    y_axis_label = 'Temperature (K)'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'TEM_VAC'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as TEMP, FileName, CONVERT(UTStart,char) AS Time " \
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
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=12)
    p.scatter(source=source2, x='UTStart', y='TEMP', color='Red', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_rmir', caption='')
def temp_rmir_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS RMIR Temp"
    y_axis_label = 'Temperature (K)'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'TEM_RMIR'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as TEMP, FileName, CONVERT(UTStart,char) AS Time " \
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
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=12)
    p.scatter(source=source2, x='UTStart', y='TEMP', color='red', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_coll', caption='')
def temp_coll_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS COLL Temp"
    y_axis_label = 'Temperature'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'TEM_COLL'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as TEMP, FileName, CONVERT(UTStart,char) AS Time " \
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
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=12)
    p.scatter(source=source2, x='UTStart', y='TEMP', color='red', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_ech', caption='')
def temp_air_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS ECH Temp"
    y_axis_label = 'Temperature'

    # creates your query
    table = 'FitsHeaderHrs'
    column = 'TEM_ECH'
    logic = " and FileName like 'H%%'"
    logic2 = " and FileName like 'R%%'"
    sql = "select UTStart, {column} as TEMP, FileName, CONVERT(UTStart,char) AS Time " \
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
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    p.scatter(source=source, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=12)
    p.scatter(source=source2, x='UTStart', y='TEMP', color='red', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_ob', caption='')
def temp_air_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS OB Temp"
    y_axis_label = 'Temperature'

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                    <div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Date: </span>
                            <span style="font-size: 15px;"> @Time</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    #  p.scatter(source=source1, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p


@data_quality(name='temp_iob', caption='')
def temp_air_plot(start_date, end_date):
    """Return a <div> element with a HRS temperature plot.

    The plot shows the HRS temperature for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the temperature plot.
    """
    title = "HRS IOB Temp"
    y_axis_label = 'Temperature'

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                    <div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Date: </span>
                            <span style="font-size: 15px;"> @Time</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Temperature: </span>
                            <span style="font-size: 15px;"> @TEMP</span>
                        </div>
                        <div>
                            <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                            <span style="font-size: 15px;"> @FileName</span>
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

    p = figure(title=title,
               x_axis_label='Date', y_axis_label=y_axis_label,
               x_axis_type='datetime', tools=[tool_list, _hover])
    #  p.scatter(source=source1, x='UTStart', y='TEMP', color='blue', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    return p
