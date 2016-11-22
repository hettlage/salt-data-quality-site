# Storing query parameters

By default, all query parameters are lost when you navigate away from a page. So, for example, if the page lets you set a start and end date, the dates will revert back to the default dates.

You can avoid this by decorating the function for your query form with the `store_query_parameters` decorator. This decorator ensures that all specified GET, POST and PUT parameters are stored in a Flask session variable as well as in `g.stored_query_parameters`, where `g` Flask's g object. You specify the parameters to store by including their name in the `names` argument of the decorator.

Next time you load the page the stored parameters are loaded and, unless new values are passed via GET, POST or PUT parameters, they are again stored in `g.stored_query_parameters`. You may thus re-populate your form with the values of the last visit to the page.

As an example, consider a function which has a form for a start and end date and which outputs the number of days between the two dates.

The form for the dates is created in the usual way:

```python
from dateutil import parser
from flask import g, render_template
from flask_wtf import Form
from wtforms.fields import DateField, SubmitField
from wtforms.validators import DataRequired


class DateRangeForm(Form):
    start_date = DateField('Start', validators=[DataRequired()])
    end_date = DateField('End', validators=[DataRequired()])
    submit = SubmitField('Query')
```

Then the function for outputting the form and number of days might look like the following.

```python
from app.decorators import store_query_parameters


@store_query_parameters(names=('start_date', 'end_date'))
def days_between():
    form = DateRangeForm()

    # update form data from stored parameters
    stored_params = g.stored_query_parameters
    if 'start_date' in stored_params:
        form.start_date.data = parser.parse(stored_params['start_date'])
    if 'end_date' in stored_params:
        form.end_date.data = parser.parse(stored_params['end_date'])

    if form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
        days_diff = (end_date - start_date).days
    else:
        days_diff = None
    return render_template('days_between.html', form=form, days_diff=days_diff)
```

The template `days_between.html` might look as follows.

```html
{% import "bootstrap/wtf.html" as wtf %}

<!DOCTYPE html>
<html>
<head>
    <title>Day difference</title>
</head>
<body>
    {{ wtf.quick_form(form) }}

    <hr>

    <div>
        Days between these dates: {{ days_diff }}
    </div>
</body>
</html>
```
