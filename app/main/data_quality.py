import functools
import importlib
import os

_data_quality_items = dict()


def data_quality(name, caption, **kwargs):
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
    **kwargs: keyword arguments
        Other keyword arguments.
    """

    def decorate(func):
        @functools.wraps(func)
        def inner(*args, **kwargs2):
            return '<figure>{content}\n' \
                   '<figcaption>\n' \
                   '{caption}' \
                   '</figcaption>' \
                   '</figure>'.format(content=func(*args, **kwargs2), caption=caption)

        _register(inner, name, **kwargs)

        return inner
    return decorate


def data_quality_item(package, name):
    """Return the data quality item details for a package and name.

    The name must be the one used in the data_quality decorator of the function.

    Params:
    -------
    package: str
        Package containing the function.
    name: str
        Name used when registering the function.

    Return:
    -------
    tuple:
        The function and the dictionary of additional details, as passed to the function's decorator.

    """

    return _data_quality_items[package][name]


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
    if package_name not in _data_quality_items:
        _data_quality_items[package_name] = {}
    d = _data_quality_items[package_name]
    if name in d:
        raise Exception('The package {package} contains multiple functions with a data_quality decorator that '
                        'has the value "{name}" as its name argument.'.format(
            package=package_name,
            name=name
        ))
    d[name] = (func, kwargs)


def default_data_quality_page(package, *args, **kwargs):
    """Content for a default data quality page.

    All the modules of the given package are imported and all data quality item functions (i.e. functions with a
    data_quality decorator) are registered. Then the functions named in the content.txt file within the package
    directory are called, and their output is joined together.

    All functions named in the context.txt file must actually exist in one of the package's modules.

    For example, assume that the content.txt file has the following content,

    rss_throughput
    RSS temperature

    Then these functions must be declared somewhere in the package's modules:

    @decorate(name='rss_throughput', caption='RSS throughput over time')
    def some_func_1():
        ...

    @decorate(name='RSS temperature', caption='Temperature over time')
    def some_func_2():
        ...

    You can choose any function names, as long as the name argument of the decorator has the correct value.

    Positional and keyword arguments (other than the first one, which gives the package) are passed on to the functions.
    This implies that all the functions should have the same signature.

    For example, if you call default_data_quality_page as

    default_data_quality_page('app.main.pages.example', from_date, to_date, include_errors=True)

    then all the functions named in the content.txt file must conform to the signature

    def func(from_date, to_date, include_errors)

    Params:
    -------
    package: str
        Fully qualified name of the package to use. If you are calling this function from the packages __init__.py file,
        the variable __package__ contains this name.
    *args: positional arguments
        Positional arguments to pass to the data quality functions named in the context.txt file.
    **kwargs: keyword arguments
        Keyword arguments to pass to the data quality functions named in the context.txt file.

    Return:
    -------
    str:
        <div> element with the HTML elements returned by the functions named in the content.txt file.

    """

    # find package directory
    spec = importlib.util.find_spec(package)
    package_init = spec.origin
    if not _is_package_init(package_init):
        raise ValueError('{package_name} is not a package'.format(package_name=package))
    package_dir = os.path.dirname(package_init)

    # find all the modules
    # use a set because some may be both source and compiled
    module_extensions = ('.py', '.pyc', '.pyo')
    modules = set([package + '.' + os.path.splitext(module)[0]
                   for module in os.listdir(package_dir)
                   if module.endswith(module_extensions) and os.path.splitext(module)[0].lower() != '__init__'])

    # import everything from the modules
    for module in modules:
        importlib.import_module(module)

    # add content for each function named in context.txt
    content_file = os.path.join(package_dir, 'content.txt')
    if not os.path.isfile(content_file):
        raise IOError('The file {path} does not exist')
    html = '<div>\n'
    with open(content_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                func = data_quality_item(package, line)[0]
                html += func(*args, **kwargs) + '\n'
    html += '</div>'

    return html


def _is_package_init(path):
    """Check whether a file path refers to a __init__.py or __init__.pyc file.

    Params:
    -------
    path: str
        File path.

    Return:
    -------
    bool:
        Whether the file path refers to a pacvkage init file.
    """

    return path.lower().endswith('__init__.py') or path.lower().endswith('__init__.pyc')