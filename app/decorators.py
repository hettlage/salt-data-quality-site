import functools
import json

from flask import g, request, session

data_quality_items = dict()


def store_query_parameters(names):
    """Decorator for (re)storing query parameters in a cookie.

    If a Flask route has this decorator, it will store query parameters in a cookie, so that they are available in a
    subsequent call as default values. The following procedure is followed.

    1. POST, PUT and GET query parameters ("PPGP") are collected.
    2. The parameters stored in the user session item 'qp_<route>' ("UP") are collected.
    3. Both the PPGP and UP are checked for the list of parameters with the given names. If a parameter is defined both
       in the PPGP and the UP, the value from the PPGP is taken.
    4. The set of parameter values from the previous step is stored in the user session item qp_<route> and also as a
       dictionary g.stored_query_parameters, where g is Flask's g object.

    The user session is valid for the current browser session only.

    The intention of this decorator is to preserve a user choice such as a date range even if the user navigates away
    from a page and then back to it.

    For example, assume you have a form which asks for a date and then displays the science time for the previous days.
    With Flask-WTF you then could implement along the following lines:

    from dateutil import parser

    class DateForm(Form):
        end_date = DateField('End', validators=[DataRequired()])
        submit = SubmitField('Query')

    @stored_query_parameters(names=('end_date'))
    def science_times():
        form = DateForm()
        form.end_date.data = parser.parse(g.stored_query_parameters['end_date']
        ...

    Params:
    -------
    names: list of str
        The names of the query parameters which should be stored and restored.
    """

    def decorate(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # query parameters
            ppgp = request.values.to_dict()

            # parameters stored in the cookie
            session_item_name = 'qp_{path}'.format(path=request.path)
            session_item_value = session.get(session_item_name)
            if session_item_value:
                cp = json.loads(session_item_value)
            else:
                cp = {}

            # merge the parameters
            merged = cp.copy()
            merged.update(ppgp)

            # store the available parameters
            params = {name:merged[name] for name in names if name in merged}
            g.stored_query_parameters = params

            # make sure the parameters are remembered
            session[session_item_name] = json.dumps(params)

            r = f(*args, **kwargs)
            return r

        return wrapped

    return decorate


def data_quality(name, caption, export_name=None, **kwargs):
    """Decorator for data quality items to be displayed.

    The function to decorate must return a string with a valid HTML element. This element is wrapped in a <figure>
    element with a <figcaption> caption, whose text is passed as an argument to the decorator. The text may contain
    HTML markup.

    The name passed to the decorator can be used to retrieve the (decorated) function by means of the
    data_quality_figure method. It must be unique within a module.

    Params:
    -------
    name: str
        Name for identifying the decorated function.
    caption: str
        Text to use as caption.
    export_name: str
        Name to use as filename when this item is exported to file (without the file extension). The default is to use
        the value of the name argument.
    **kwargs: keyword arguments
        Other keyword arguments.
    """

    def decorate(func):
        _export_name = export_name if export_name else name
        _register(func, name, caption=caption, export_name=_export_name, **kwargs)

        return func
    return decorate


def _register(func, name, **kwargs):
    """Register a function under a given name.

    The name under which the function is registered must be unique within the function's module.

    Additional keyword arguments are stored as a dictionary along with the function.

    Params:
    -------
    func: function
        Function to store.
    name: str
        Name under which to store the function.
    **kwargs: keyword arguments
        Information to store along with the function.
    """

    package_name = func.__module__.rsplit('.', 1)[0]
    if package_name not in data_quality_items:
        data_quality_items[package_name] = {}
    d = data_quality_items[package_name]
    if name in d:
        raise Exception('The package {package} contains multiple functions with a data_quality decorator that '
                        'has the value "{name}" as its name argument.'.format(package=package_name,
                                                                              name=name))
    d[name] = (func, kwargs)
