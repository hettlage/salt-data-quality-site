import pymysql as sql
import pandas as pd
import datetime
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure
from flask import current_app
from app import db

# setting date format to be used on the x axis of the plot
date_formatter = DatetimeTickFormatter(days=['%e %b %Y'], months=['%e %b %Y'], years=['%e %b %Y'])

# offset value to be added in timestamp in oder to get the exact uct for the database query
time_offset = 2082844800

#source for seeing
mean_source1 = ColumnDataSource()
median_source1=ColumnDataSource()

#source for ee50
mean_source = ColumnDataSource()
median_source=ColumnDataSource()

#source for fwhm
mean_source2=ColumnDataSource()
median_source2=ColumnDataSource()

difference_source=ColumnDataSource()
difference_source1=ColumnDataSource()

difference_source2=ColumnDataSource()
difference_source3=ColumnDataSource()

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"


# function to be called when onclick button is used
#@data_quality(name='seeing', caption=' ')
def update(start_date, end_date, binning):
    """Generate bokeh plots for seeing content using date range and optional binning query.

          This is showing two plots representing external seeing and internal seeing.The data plotted
          is queried from two databases(els_view and suthweather).

          For the first plot the median and average is calculated for both internal and external seeing.
          The second plot represents the difference between internal and external seeing.

          The start date for the range is inclusive, the end date exclusive, the binning is optional.

          Defaults can be supplied for the start and end date.

          The content is created if the form is valid, irrespective of whether a GET or POST request is made. Otherwise only
          the form is included.

          Params:
          -------
          default_start_date: date
              Default start date for the query.
          default_end_date: date
              Default end date for the query.
          optinal_binning: binning
          """
    global mean_source1,mean_source,median_source1,median_source, difference_source1,difference_source, difference_source2 , difference_source3, mean_source2, median_source2

    # if type of start/end date is date, turn it into a datetime,
    # set time of start/end date time to 12:00

    def convert_time(t):
        if type(t) == datetime.date:
            return datetime.datetime(t.year, t.month, t.day, 12, 0, 0, 0)
        else:
            return t.replace(hour=12, minute=0, second=0, microsecond=0)

    start_date = convert_time(start_date)
    end_date = convert_time(end_date)
    if binning is None:
        binning = ''

    first_timestamp = start_date.timestamp() + time_offset
    second_timestamp = end_date.timestamp() + time_offset

    # query data in mysql database
    sql1 = 'SELECT  str_to_date(datetime,"%%Y-%%m-%%d %%H:%%i:%%s") AS datetime, seeing  from seeing ' \
           '    where datetime >= str_to_date("{start_date_}","%%Y-%%m-%%d  %%H:%%i:%%s")' \
           '    and datetime <= str_to_date("{end_date_}","%%Y-%%m-%%d %%H:%%i:%%s") ' \
        .format(start_date_=str(start_date), end_date_=str(end_date))

    sql2 = 'select _timestamp_,ee50,fwhm,timestamp from tpc_guidance_status__timestamp where timestamp >= {start_date_}' \
           '   and timestamp<= {end_date_} and guidance_available="T"  ' \
           ' order by _timestamp_' \
        .format(start_date_=str(first_timestamp), end_date_=str(second_timestamp))

    df2 = pd.read_sql(sql2, db.get_engine(app=current_app, bind='els'))
    df1 = pd.read_sql(sql1, db.get_engine(app=current_app, bind='suthweather'))

    # setting index time for calculating mean and average
    df2.index = df2["_timestamp_"]
    df1.index = df1['datetime']

    # It seems that Pandas doesn't change the index type if the data frame is empty, which means that resampling
    # would fail for an empty data frame. As there will be no row for median or mean , it is safe to just use the
    # original data frame to avoid this problem.

    # for external seeing calculating median and mean
    if not df1.empty:
        mean1_all = df1.resample(str(binning) + 'T').mean()
    else:
        mean1_all = df1.copy(deep=True)
    source1 = ColumnDataSource(mean1_all)
    mean_source1.data = source1.data

    if not df1.empty:
        median1_all = df1.resample(str(binning) + 'T').median()
    else:
        median1_all = df1.copy(deep=True)
    source = ColumnDataSource(median1_all)
    median_source1.data = source.data

    # calculate mean and median for ee50
    if not df2.empty:
        mean_all = df2.resample(str(binning) + 'T').mean()
    else:
        mean_all = df2.copy(deep=True)
    source3 = ColumnDataSource(mean_all)
    mean_source.data = source3.data

    if not df2.empty:
        median_all = df2.resample(str(binning) + 'T').median()
    else:
        median_all = df2.copy(deep=True)
    source4 = ColumnDataSource(median_all)
    median_source.data = source4.data

    #calculate mean and median for fwhm
    if not df2.empty:
        mean_all1 = df2.resample(str(binning) + 'T').mean()
    else:
        mean_all1 = df2.copy(deep=True)
    source4 = ColumnDataSource(mean_all)
    mean_source2.data = source4.data

    if not df2.empty:
        median_all = df2.resample(str(binning) + 'T').median()
    else:
        median_all = df2.copy(deep=True)
    source5 = ColumnDataSource(median_all)
    median_source2.data = source5.data

    # calculate difference for external seeing against fwhm and ee50
    dataframes = [mean1_all, mean_all]
    add_dataframes = pd.concat(dataframes, axis=1)
    add_dataframes.index.name = '_timestamp_'
    add_dataframes['difference'] = add_dataframes['seeing'] - add_dataframes['ee50']
    datasource2 = ColumnDataSource(add_dataframes)
    difference_source.data = datasource2.data

    dataframes = [mean1_all, mean_all1]
    add_dataframes = pd.concat(dataframes, axis=1)
    add_dataframes.index.name = '_timestamp_'
    add_dataframes['difference1'] = add_dataframes['seeing'] - add_dataframes['fwhm']
    datasource1 = ColumnDataSource(add_dataframes)
    difference_source1.data = datasource1.data

    # #difference using the median
    # dataframes2 = [median_all, median1_all]
    # add_dataframes2 = pd.concat(dataframes2, axis=1)
    # add_dataframes2.index.name = '_timestamp_'
    # add_dataframes2['difference2'] = add_dataframes2['seeing'] - add_dataframes2['ee50']
    # datasource2 = ColumnDataSource(add_dataframes2)
    # difference_source2.data = datasource2.data
    #
    # dataframes3 = [median_all, median1_all]
    # add_dataframes3 = pd.concat(dataframes3, axis=1)
    # add_dataframes3.index.name = '_timestamp_'
    # add_dataframes3['difference3'] = add_dataframes3['seeing'] - add_dataframes3['fwhm']
    # datasource3 = ColumnDataSource(add_dataframes3)
    # difference_source3.data = datasource3.data

    # plot labels
    p = figure(title="external vs internal seeing ({binning} minute bins)".format(binning=binning), x_axis_type='datetime'
               , x_axis_label='datetime', y_axis_label='seeing',plot_width=1000, plot_height=500,tools=TOOLS)
    dif=figure(title='difference between average internal and external seeing ({binning} minute bins)'.format(binning=binning), x_axis_type='datetime',
               x_axis_label='datetime', y_axis_label='seeing',plot_width=1000, plot_height=500,tools=TOOLS)

    #plots
    # plots for external seeing
    p.circle(source=mean_source1, x='datetime',y='seeing', legend="external average" ,fill_color="white",color='green')
    p.line(source=median_source1, x='datetime',y='seeing', legend="external median" ,color='blue')

    #plots showing median and mean for ee50 and fwhm
    p.circle(source=mean_source, x='_timestamp_', y='ee50', legend='ee50 average')
    p.circle(source=mean_source, x='_timestamp_', y='fwhm', legend='fwhm average', color='red', fill_color='white')

    p.line(source=median_source, x='_timestamp_', y='ee50', legend='ee50 median', color='green')
    p.line(source=median_source, x='_timestamp_', y='fwhm', legend='fwhm median', color='orange')

    #for difference
    dif.circle(source=difference_source, x='_timestamp_', y='difference', legend='ee50_mean difference', color='red')
    dif.circle(source=difference_source1, x='_timestamp_', y='difference1', legend='fwhm_mean difference', fill_color='green')

    #
    # dif.circle(source=difference_source2, x='_timestamp_', y='difference2', legend='ee50_median difference', fill_color='blue')
    # dif.circle(source=difference_source3, x='_timestamp_', y='difference3', legend='fwhm_median difference', color='orange')

    p.xaxis.formatter = date_formatter
    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    dif.xaxis.formatter = date_formatter
    dif.legend.click_policy="hide"

    script, div = components(p)
    content1 = '<div>{script}{div}</div>'.format(script=script, div=div)

    script, div = components(dif)
    content2 = '<div>{script}{div}</div>'.format(script=script, div=div)

    return '{cont} {cont2}'.format(cont=content1,cont2=content2)
