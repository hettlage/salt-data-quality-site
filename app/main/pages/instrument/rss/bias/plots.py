from app.decorators import data_quality
from app.main.data_quality_plots import data_quality_date_plot


@data_quality(name='rss_bias', caption='Mean RSS Bias Background levels')
def rss_bias_plot(start_date, end_date):
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
    title = "RSS Bias Levels"
    column = 'BkgdMean'
    table = 'PipelineDataQuality_CCD'
    logic = " and FileName like 'P%%' and Target_Name='BIAS'"
    y_axis_label = 'Bias Background Mean (e)'
    return data_quality_date_plot(start_date, end_date, title, column, table, logic=logic, y_axis_label=y_axis_label)
