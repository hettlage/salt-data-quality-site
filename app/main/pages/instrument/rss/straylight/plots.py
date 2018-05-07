import pandas as pd

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
colors = ['red', 'magenta', 'blue', 'orange', 'green', 'purple']
legends_name = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6']
y_name = ['mean_z1', 'mean_z2', 'mean_z3', 'mean_z4', 'mean_z5', 'mean_z6']


# One plot for zero articulation setting closed dome test
@data_quality(name='rss_straylight_zero', caption='')
def rss_straylight_zero_plot(start_date, end_date):
    return _rss_straylight_plot(0.0, start_date, end_date)


# One plot for ninety articulation setting closed dome test
@data_quality(name='rss_straylight_ninety', caption='')
def rss_straylight_ninety_plot(start_date, end_date):
    return _rss_straylight_plot(90.25, start_date, end_date)


def _rss_straylight_plot(articulation, start_date, end_date):
    """Return a <div> element with a RSS Straylight plot.

    The plots show the average counts in six detector regions of RSS taken
    from standard closed dome straylight tests (one plot for articulation=0, one for articulation=90.25)
    To measure stray light on RSS, we split up the product RSS frame into 6 regions:
     ___________
    |   |   |   |
    | 1 | 3 | 5 |
    |___|___|___|
    |   |   |   |
    | 2 | 4 | 6 |
    |___|___|___|

    The plot is made for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    articulation: degrees (float - %.2f)
        RSS camera articulation angle; either 0 or 90.25
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the plot.
    """

    # title with articulation angle to 2 decimal points
    title = "RSS Straylight @ {0:.2f} deg" .format(articulation)
    y_axis_label = 'Average Counts'

    # creates your query
    table = 'RssStrayLight'
    # query only selects rows with camang that are specified by articulation
    sql = "select UTStart,mean_z1,mean_z2,mean_z3,mean_z4,mean_z5,mean_z6 from RssStrayLight" \
          "       join FileData using (FileData_Id)" \
          "       join FitsHeaderRss using (FileData_Id)" \
          "       join FitsHeaderImage using (FileData_Id)" \
          "       where UTStart > '{start_date}' and UTStart <'{end_date}' and CAMANG='{camang}'"\
        .format(start_date=start_date, end_date=end_date, camang=articulation)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    p = figure(title=title,
               x_axis_label='UTStart',
               y_axis_label=y_axis_label,
               x_axis_type='datetime')
    # creating line and circle sepearately; fill_alpha gives a bit of transparency to the circles
    # legends are easily added with legend=...
    for x in range(6):
        p.line(x='UTStart', y=y_name[x], color=colors[x], source=source, legend=legends_name[x])
        p.circle(x='UTStart', y=y_name[x], color=colors[x], fill_alpha=0.2, size=10, source=source, legend=legends_name[x])

    p.xaxis[0].formatter = date_formatter
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"


    return p
