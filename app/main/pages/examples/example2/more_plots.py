import numpy as np

from bokeh.embed import components
from bokeh.plotting import figure

from app.main.data_quality import data_quality


@data_quality(name='sine', caption='The sine function.')
def sine_plot(from_date, to_date, include_errors):
    x = np.linspace(-10, 10, 100)
    y = np.sin(x)
    p = figure(title='Sine', x_axis_label='x', y_axis_label='y')
    p.line(x, y)

    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)



@data_quality(name='Third Plot', caption='Yet another shiny plot.')
def plot2(from_date, to_date, include_errors):
    x = np.linspace(-10, 10, 100)
    y = np.cos(x)

    p = figure(title='Cosine', x_axis_label='x', y_axis_label='y')
    p.line(x, y)
    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)
