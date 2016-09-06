import functools
import importlib
import os

data_quality_items = dict()


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
        _register(func, name, **kwargs)

        @functools.wraps(func)
        def inner(*args, **kwargs2):
            return '<figure>{content}\n' \
                   '<figcaption>\n' \
                   '{caption}' \
                   '</figcaption>' \
                   '</figure>'.format(content=func(*args, **kwargs2), caption=caption)

        return inner
    return decorate


def data_quality_item(module, name):
    """Return the data quality item details for a module and name.

    The name must be the one used in the data_quality decorator of the function.

    Params:
    -------
    module: str
        Module containing the function.
    name: str
        Name used when registering the function.

    Return:
    -------
    tuple:
        The function and the dictionary of additional details, as passed to the function's decorator.

    """

    return data_quality_items[module][name]


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

    if func.__module__ not in data_quality_items:
        data_quality_items[func.__module__] = {}
    d = data_quality_items[func.__module__]
    if func.__name__ in d:
        raise Exception('The module {module} contains multiple functions with a data_quality decorator that '
                        'has the value "{name}" as its name argument.'.format(
            module=func.__module__,
            name=name
        ))
    d[name] = (func, kwargs)


def default_data_quality_page(package_name):
    # find package directory
    spec = importlib.util.find_spec(package_name)
    package_init = spec.origin
    if not _is_package_init(package_init):
        raise ValueError('{package_name} is not a package'.format(package_name=package_name))
    package_dir = os.path.dirname(package_init)

    # find all the modules
    # use a set because some may be both source and compiled
    module_extensions = ('.py', '.pyc', '.pyo')
    modules = set([package_name + '.' + os.path.splitext(module)[0]
                   for module in os.listdir(package_dir)
                   if module.endswith(module_extensions) and os.path.splitext(module)[0].lower() != '__init__'])

    # import everything from the modules
    for module in modules:
        importlib.import_module(module)


def _is_package_init(path):
    """Check whether a file path refers to a __init__.py or __init__.pyc file.

    Params:
    -------
    path: str
        File path.

    Returns:
    --------
    bool:
        Whether the file path refers to a pacvkage init file.
    """

    return path.lower().endswith('__init__.py') or path.lower().endswith('__init__.pyc')