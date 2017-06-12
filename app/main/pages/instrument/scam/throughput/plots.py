import pandas as pd

from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.palettes import Plasma256
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.decorators import data_quality
from app.main.data_quality_plots import data_quality_date_plot


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

    column = 'SalticamThroughputMeasurement'

    sql = 'select Date, SalticamFilter_Name as Name, DescriptiveName as Barcode, ' \
          ' SalticamThroughputMeasurement as Throughput' \
          '     from SalticamThroughputMeasurement ' \
          '         join Throughput using (Throughput_Id) ' \
          '         join NightInfo using (NightInfo_Id) ' \
          '         join SalticamFilter using(SalticamFilter_Id) ' \
        .format(start_date=start_date, end_date=end_date, column=column)

    df = pd.read_sql(sql, db.engine)
    file_df = pd.read_csv('scam_data.txt', delimiter="\t")

    file_df.columns = ['Barcode', 'Center', 'HMFW']

    df['Barcode_lower'] = df['Barcode'].str.lower()
    df['Barcode_lower'] = df['Barcode_lower'].str.replace(' ', '')

    file_df['Barcode_low'] = file_df['Barcode'].str.lower()
    file_df['Barcode_low'] = file_df['Barcode_low'].str.replace(' ', '')
    file_df['Barcode_low'] = file_df['Barcode_low'].str.replace('_', '')

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
               tools=[tool_list, _hover])

    sot = sorted(range(len(data_list)), key=lambda k: data_list[k])

    for indx in reversed(sot):
        d = pd.DataFrame()
        d['name'] = date_list[indx]['Name']
        d['centers'] = date_list[indx]['Center']
        d['throughput'] = date_list[indx]['Throughput']
        d['wavelength'] = date_list[indx]['Wavelength']
        d['hmfw'] = date_list[indx]['HMFW']

        d['colors'] = [Plasma256[int(indx * (len(Plasma256) - 1) / float(len(sot)))]
                      for x in range(len(d['centers']))]
        source = ColumnDataSource(d)
        p.scatter(source=source, y='throughput', x='centers', color=d['colors'][0], fill_alpha=0.2, size=10, legend=data_list[indx])
        p.line(source=source, y='throughput', x='centers', color=d['colors'][0], line_width=1, legend=data_list[indx])

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.3
    p.legend.inactive_fill_alpha = 0.8
    return p  # data_quality_date_plot(start_date, end_date, title, column, table,
