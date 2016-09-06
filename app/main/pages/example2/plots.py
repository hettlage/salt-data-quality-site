from app.main.data_quality import data_quality


@data_quality(name='first_plot', caption='A shiny plot.')
def plot1():
    return '<div>This is plot 1.</div>/'
