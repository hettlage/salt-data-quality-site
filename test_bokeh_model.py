import argparse
import importlib
import inspect
import os
import sys
import traceback

from bokeh.plotting import output_file, show
from fabulous.color import bold, red

from app import create_app


def error(msg, stacktrace=None):
    """Print an error message and exit.

    Params:
    -------
    msg: str
        Error message.
    stacktrace: str
        Stacktrace.
    """

    if stacktrace:
        print(stacktrace)
    print(bold(red(msg)))
    sys.exit(1)

# get command line arguments
parser = argparse.ArgumentParser(description='Test a Bokeh model.')
parser.add_argument('module_file',
                    type=str,
                    help='Python file containing the Bokeh model')
parser.add_argument('model_function',
                    type=str,
                    help='Function returning the Bokeh model')
parser.add_argument('func_args',
                    type=str,
                    nargs='*',
                    help='Arguments to pass to the model function')

args = parser.parse_args()

# directory in which this script is located
# note: this must not be app or a subdirectory thereof
this_file = os.path.realpath(__file__)
base_dir = os.path.abspath(os.path.join(this_file, os.path.pardir))

# ensure the given module file isd a Python file
module_file = os.path.abspath(args.module_file)
if not module_file.lower().endswith('.py'):
    error('The module filename must end with ".py".')

# find the path of the module file relative to the base directory of the project
module_path = os.path.relpath(module_file, os.path.commonprefix([module_file, this_file]))

# convert the path into a module name (remove ".py" and replace separators with dots)
module = module_path[:-3].replace(os.path.sep, '.')

# import the module and find the requested function to test
try:
    imported_module = importlib.import_module(module, __package__)
except:
    error('The module {module} couldn\'t be imported. Does the model exist?'.format(module=module))
functions = [member for member in inspect.getmembers(imported_module) if member[0] == args.model_function]
if len(functions) == 0:
    error('There is no function "{func}" defined in {module}'.format(func=args.model_function, module=module))
if len(functions) > 1:
    error('The name "{func}" is ambiguous in the module {module}.'.format(func=args.model_function, module=module))

# set up Flask app context
# if we don't do this SQLAlchemy will fail
app = create_app(os.getenv('FLASK_CONFIG') or 'development')
app_context = app.app_context()
app_context.push()

# get the Bokeh model
func = functions[0][1]
try:
    model = func(*args.func_args)
except:
    error('The call to function "{func}" failed.'.format(func=args.model_function),
          traceback.format_exc(1))

# output the model
output_file('/tmp/bokeh_test.html')
try:
    show(model)
except:
    error('The Bokeh model couldn\'t be output. (Is your function returning a Bokeh model?)',
          traceback.format_exc())

# clean up
app_context.pop()
