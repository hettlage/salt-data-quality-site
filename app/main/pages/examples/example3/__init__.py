from bokeh.embed import autoload_server


def title():
    return 'Interactive Plot'


def content():
    script1 = autoload_server(model=None, app_path='/sine', url='http://localhost:5100')
    script2 = autoload_server(model=None, app_path='/cosine', url='http://localhost:5100')
    return '<div>' + script1 + '</div>\n<div>' + script2 + '</div>'
