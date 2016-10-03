from app.main.data_quality import _register


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