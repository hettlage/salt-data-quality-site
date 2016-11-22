# Potential pitfalls

* If you are accessing the database using Pandas' `read_sql` function, you must use '%%' instead of '%' in your SQL query strings.
* If you are using a DatetimeTickFormatter in Bokeh, you *must* define a format for all possible timescales, as otherwise your plot might not be displayed. An easy way for achieving this is to use Bokeh's DEFAULT_DATETIME_FORMATS function. For example,

```python
from bokeh.models.formatters import DatetimeTickFormatter, DEFAULT_DATETIME_FORMATS

date_formats = DEFAULT_DATETIME_FORMATS()
date_formats['hours'] = ['%e %b %Y']
date_formats['days'] = ['%e %b %Y']
date_formats['months'] = ['%e %b %Y']
date_formats['years'] = ['%e %b %Y']
date_formatter = DatetimeTickFormatter(formats=date_formats)
```
