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


@data_quality(name='hrs_flats', caption='')
def hrs_flats_plot(start_date, end_date):
    """Return a <div> element with a HRS arc stability plot.

    The plot shows the HRS Flatfield Background level for obsmode High, low and medium over time

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the Flats field Background level.
    """

    def get_source(obsmode):
        logic = "   and OBSMODE='{obsmode}' " \
                "       and Proposal_Code = 'CAL_FLAT' " \
                "       and FileName like 'R%%'" \
            .format(obsmode=obsmode)
        sql = "select UTStart, BkgdMean, CONVERT(UTStart,char) AS Time " \
              "     from PipelineDataQuality_CCD " \
              "         join FileData using (FileData_Id) " \
              "         join ProposalCode using (ProposalCode_Id)  " \
              "     where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}" \
            .format(start_date=start_date, end_date=end_date, logic=logic)
        df = pd.read_sql(sql, db.engine)
        source = ColumnDataSource(df)
        return source

    low_source = get_source('LOW RESOLUTION')
    med_source = get_source('MEDIUM RESOLUTION')
    high_source = get_source('HIGH RESOLUTION')

    tool_list = "pan,reset,save,wheel_zoom, box_zoom"
    _hover = HoverTool(
        tooltips="""
                <div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Date: </span>
                        <span style="font-size: 15px;"> @Time</span>
                    </div>
                    <div>
                        <span style="font-size: 15px; font-weight: bold;">Background Level: </span>
                        <span style="font-size: 15px;"> @BkgdMean</span>
                    </div>
                </div>
                """
    )

    p = figure(title="Flatfield Background level",
               x_axis_label='Date',
               y_axis_label='BkgMean',
               x_axis_type='datetime',
               tools=[tool_list, _hover])
    p.scatter(source=low_source, x='UTStart', y='BkgdMean', color='red', fill_alpha=0.2, legend='Low', size=10)
    p.scatter(source=med_source, x='UTStart', y='BkgdMean', color='green', fill_alpha=0.2, legend='Medium', size=10)
    p.scatter(source=high_source, x='UTStart', y='BkgdMean', color='blue', fill_alpha=0.2, legend='High', size=10)

    p.xaxis[0].formatter = date_formatter
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.3
    p.legend.inactive_fill_alpha = 0.8

    return p