from app.main.data_quality import data_quality


@data_quality(name='Second Plot', caption='Another shiny plot.')
def plot1(from_date, to_date, include_errors):
    return '<div>This is plot 2 (from: {from_date}, to: {to_date}, include errors: {include_errors})</div>' \
        .format(from_date=from_date, to_date=to_date, include_errors=include_errors)


@data_quality(name='Third Plot', caption='Yet another shiny plot.')
def plot2(from_date, to_date, include_errors):
    return '<div>This is plot 2 (from: {from_date}, to: {to_date}, include errors: {include_errors})</div>' \
        .format(from_date=from_date, to_date=to_date, include_errors=include_errors)