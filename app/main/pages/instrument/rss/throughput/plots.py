import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.palettes import Plasma256
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool

from app import db
from app.decorators import data_quality


# plot for RSS throughput
@data_quality(name='rss_throughput', caption=' ')
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

    date_formatter = DatetimeTickFormatter(microseconds=['%f'],
                                           milliseconds=['%S.%3Ns'],
                                           seconds=[':%Ss'],
                                           minsec=[':%Mm:%Ss'],
                                           minutes=['%H:%M:%S'],
                                           hourmin=['%H:%M:'],
                                           hours=["%H:%M"],
                                           days=["%d %b"],
                                           months=["%d %b %Y"],
                                           years=["%b %Y"])

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
            <div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Date: </span>
                    <span style="font-size: 15px;"> @Time</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Throughput: </span>
                    <span style="font-size: 15px;"> @StarsUsed</span>
                </div>
                <div>
                    <span style="font-size: 15px; font-weight: bold;">Star used: </span>
                    <span style="font-size: 15px;"> @RssThroughput</span>
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
               x_axis_label='Date',
               y_axis_label="RSS Throughput",
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=source, x='Date', y='{throughput_column}'.format(throughput_column=throughput_column),
              color='blue', fill_alpha=0.2, size=10)

    p.xaxis[0].formatter = date_formatter

    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)


@data_quality(name='wavelength', caption=' ')
def hbdet_bias_plot(start_date, end_date):
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
    data_list = []
    date_list = []

    def brake_by_date(data):
        _date = data["Date"].strftime('%Y-%m-%d')
        if _date not in data_list:
            date_dict = {'Name': [], 'Throughput': [], 'Center': [], 'Wavelength': [], "HMFW": []}
            data_list.append(_date)
            date_list.append(date_dict)
        ind = data_list.index(_date)
        date_list[ind]['Name'].append(data['Name'])
        date_list[ind]['Throughput'].append(data['Throughput'])
        date_list[ind]['Center'].append(data['Center'])
        date_list[ind]['Wavelength'].append(str('%.1f' % data['Center']))
        date_list[ind]['HMFW'].append(str('%.1f' %data['HMFW']))

    column = 'RssThroughputMeasurement'

    sql = 'select Date, Barcode, Barcode as Name,  RssThroughputMeasurement as Throughput' \
          '     from RssThroughputMeasurement ' \
          '         join Throughput using (Throughput_Id) ' \
          '         join NightInfo using (NightInfo_Id) ' \
          '         join RssFilter using(RssFilter_Id) ' \
        .format(start_date=start_date, end_date=end_date, column=column)

    df = pd.read_sql(sql, db.engine)
    file_df = pd.read_csv('rss_data.txt', delimiter="\t")

    file_df.columns = ['Barcode', 'Center', 'HMFW']

    df['Barcode_lower'] = df['Barcode'].str.lower()
    df['Barcode_lower'] = df['Barcode_lower'].str.replace(' ', '')

    file_df['Barcode_low'] = file_df['Barcode'].str.lower()
    file_df['Barcode_low'] = file_df['Barcode_low'].str.replace(' ', '')
    file_df['Barcode_low'] = file_df['Barcode_low'].str.replace('_', '')
    file_df['Center'] = file_df['Center'] / 10000

    results = pd.merge(df, file_df, left_on='Barcode_lower', right_on="Barcode_low", how='left')
    for index, row in results.iterrows():
        brake_by_date(row)

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                        <div>
                            <div>
                                <span style="font-size: 15px; font-weight: bold;">Name: </span>
                                <span style="font-size: 15px;"> @name</span>
                            </div>
                            <div>
                                <span style="font-size: 15px; font-weight: bold;">Pixel Center: </span>
                                <span style="font-size: 15px;"> @wavelength</span>
                            </div>
                            <div>
                                <span style="font-size: 15px; font-weight: bold;">HMFW: </span>
                                <span style="font-size: 15px;"> @hmfw</span>
                            </div>
                            <div>
                                <span style="font-size: 15px; font-weight: bold;">Throughput: </span>
                                <span style="font-size: 15px;"> @throughput</span>
                            </div>
                        </div>
                        """
    )

    # creates your plot

    p = figure(title="Plot name",
               x_axis_label='WaveLength(microns)',
               y_axis_label="Throughput",
               width=1000,
               tools=[tool_list, _hover],
               x_range=(0.4, 0.97))

    sot = sorted(range(len(data_list)), key=lambda k: data_list[k])

    for indx in reversed(sot):
        d = pd.DataFrame()
        d['name'] = date_list[indx]['Name']
        d['centers'] = date_list[indx]['Center']
        d['throughput'] = date_list[indx]['Throughput']
        d['wavelength'] = date_list[indx]['Wavelength']
        d['hmfw'] = date_list[indx]['HMFW']

        d['colors'] = [Plasma256[int(sot.index(indx) * (len(Plasma256) - 1) / float(len(sot)))]
                      for x in range(len(d['centers']))]
        source = ColumnDataSource(d)
        p.scatter(source=source, y='throughput', x='centers', color=d['colors'][0], fill_alpha=0.2, size=10, legend=data_list[indx])
        p.line(source=source, y='throughput', x='centers', color=d['colors'][0], line_width=1, legend=data_list[indx])

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.3
    p.legend.inactive_fill_alpha = 0.8
    return p  # data_quality_date_plot(start_date, end_date, title, column, table,