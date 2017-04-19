import pandas as pd

from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter, DEFAULT_DATETIME_FORMATS
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.decorators import data_quality
from app.main.data_quality_plots import data_quality_date_plot


@data_quality(name='hbdet_arc_wave', caption='HRS Arc stability')
def hbdet_arc_wave_plot(start_date, end_date):
    """Return a <div> element with a HRS arc stability plot.

    The plot shows the HRS wavelenght as a function of pixel position for a set of time

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
    title = "HBDET Arc Stability"
    y_axis_label = 'Pixel Position'

    # creates your query
    table = 'DQ_HrsArc'
    column = 'x'
    obsmode = 'LOW RESOLUTION'
    wavelength = 6483.08
    logic = " and FileName like 'H%%' and OBSMODE like '{obsmode}' and wavelength={wavelength}"\
        .format(obsmode=obsmode, wavelength=wavelength)
    sql = "select UTStart, {column}, FileName, OBSMODE, CONVERT(UTStart,char) AS Time " \
          "     from {table} join FileData using (FileData_Id) " \
          "         where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}" \
        .format(column=column, start_date=start_date, end_date=end_date,
                table=table, logic=logic)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)
    print(sql)

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
                        <span style="font-size: 15px;"> @x</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Filename: </span>
                        <span style="font-size: 15px;"> @FileName</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Obs Mode: </span>
                        <span style="font-size: 15px;"> @OBSMODE</span>
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
    print(df)
    p.scatter(source=source, x='UTStart', y=column)

    p.xaxis[0].formatter = date_formatter

    return p
