import pymysql as sql
import pandas as pd
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure
import os



#sdb connection
db_connection = sql.connect(host=os.getenv("HOST"), db=os.getenv('DATABASE1'), user= os.getenv('USER'), password=os.getenv('PASSWORD'))
sdb_con=sql.connect(host= os.getenv("HOST") , database=os.getenv('DATABASE2'), user= os.getenv('USER') , password=os.getenv('PASSWORD'))

#setting date format to be used on the x axis of the plot
date_formatter = DatetimeTickFormatter(days=['%e %b %Y'], months=['%e %b %Y'], years=['%e %b %Y'])

time_offset = 2082844800

mean_source1 = ColumnDataSource()
median_source1=ColumnDataSource()

mean_source = ColumnDataSource()
median_source=ColumnDataSource()

difference_source=ColumnDataSource()
difference_source1=ColumnDataSource()

TOOLS="pan,wheel_zoom,box_zoom,reset,save"


#function to be called when onclick button is used
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
    global mean_source1,mean_source,median_source1,median_source, difference_source1,difference_source

    first_timestamp = start_date.replace(hour=12).timestamp() + time_offset
    second_timestamp = end_date.replace(hour=12).timestamp() + time_offset

            # query data in mysql database
    sql1 = 'SELECT  str_to_date(datetime,"%Y-%m-%d %H:%i:%s") AS datetime, seeing  from seeing ' \
           '    where datetime >= str_to_date("{start_date_}","%Y-%m-%d  %H:%i:%s")' \
           '    and datetime <= str_to_date("{end_date_}","%Y-%m-%d %H:%i:%s") ' \
        .format(start_date_=str(start_date), end_date_=str(end_date))

    sql2 = 'select _timestamp_,ee50,fwhm,timestamp from tpc_guidance_status__timestamp where timestamp >= {start_date_}' \
           '   and timestamp<= {end_date_} and guidance_available="T"  ' \
           ' order by _timestamp_' \
        .format(start_date_=str(first_timestamp), end_date_=str(second_timestamp))

    df2 = pd.read_sql(sql2, con=sdb_con)
    df1 = pd.read_sql(sql1, con=db_connection)

    #seting index time for calcalating mean and average
    df2.index = df2["_timestamp_"]
    df1.index = df1['datetime']

    # for external seeing calculating median and mean
    mean1 = df1[['seeing']].mean()
    mean1_all = df1.resample(str(binning) + 'T').mean()
    source1 = ColumnDataSource(mean1_all)
    mean_source1.data = source1.data

    median1 = df1[['seeing']].median()
    median1_all = df1.resample(str(binning) + 'T').median()
    source = ColumnDataSource(median1_all)
    median_source1.data = source.data

    #calculate mean and median for fwhm,ee50
    mean = df2[['fwhm', 'ee50']].mean()
    mean_all = df2.resample(str(binning) + 'T').mean()
    source3 = ColumnDataSource(mean_all)
    mean_source.data = source3.data

    median = df2[['fwhm', 'ee50']].median()
    median_all = df2.resample(str(binning) + 'T').median()
    source4 = ColumnDataSource(median_all)
    median_source.data = source4.data

    #calculate difference for external seeing against fwhm and ee50
    dataframes = [mean1_all, mean_all]
    add_dataframes = pd.concat(dataframes, axis=1)
    add_dataframes.index.name = '_timestamp_'
    add_dataframes['difference1'] = add_dataframes['seeing'] - add_dataframes['fwhm']
    datasource = ColumnDataSource(add_dataframes)
    difference_source1.data = datasource.data

    #for difference with ee50
    add_dataframes['difference'] = add_dataframes['seeing'] - add_dataframes['ee50']
    datasource = ColumnDataSource(add_dataframes)
    difference_source.data = datasource.data

    #plot labels
    p = figure(title="external vs internal seeing ({binning} minute bins)".format(binning=binning), x_axis_type='datetime'
               , x_axis_label='datetime', y_axis_label='seeing',plot_width=1000, plot_height=500,tools=TOOLS)
    dif=figure(title='difference between average internal and external seeing ({binning} minute bins)'.format(binning=binning), x_axis_type='datetime',
               x_axis_label='datetime', y_axis_label='seeing',plot_width=1000, plot_height=500,tools=TOOLS)

    #plots
    #plots for external seeing
    p.circle(source=mean_source1, x='datetime',y='seeing', legend="external average" ,fill_color="white",color='green')
    p.line(source=median_source1, x='datetime',y='seeing', legend="external median" ,color='blue')

    #plots showing median and mean for ee50 and fwhm
    p.circle(source=mean_source, x='_timestamp_', y='ee50', legend='ee50 average')
    p.circle(source=mean_source, x='_timestamp_', y='fwhm', legend='fwhm average', color='red', fill_color='white')

    p.line(source=median_source, x='_timestamp_', y='ee50', legend='ee50 median', color='green')
    p.line(source=median_source, x='_timestamp_', y='fwhm', legend='fwhm median', color='orange')

    #for difference
    dif.circle(source=difference_source1, x='_timestamp_', y='difference1', legend='fwhm difference', fill_color='blue')
    dif.circle(source=difference_source, x='_timestamp_', y='difference', legend='ee50 difference', color='red')

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
