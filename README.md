# SALT Data Quality Site

A website for displaying data quality measurements done for the Southern African Large Telescope (SALT).

## Installation

### On your machine for development

Download the content of the repository as a zip file and extract the file into a directory of your choice. Don't clone the repository, unless you are actually planning to update the start setup rather than to create a new Flask site.

You should then put the new directory (let's call it `/path/to/site`) under version control.

```bash
cd /path/to/site
git init
```

Make sure you've installed [Java](http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html) (required for building bundles of static files with Flask-Assets) and Python 3. Create a virtual environment

```bash
python3 -m venv venv
```

and then install the required Python libraries,

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Open the file `environment.yml` and replace the environment name with a more suitable one. Save the file and create the environment by executing

```bash
conda env create -f environment.yml
```

Define the required environment variables, as set out in the section *Environment variables* below. (If you are using an IDE, you might define these in your running configuration.)

You can then run the following commands for launching the (development) server or running the tests.

| Command | Purpose |
| --- | --- |
| `python manage.py runserver` | Launch the server |
| `./run_tests.sh` | Run the tests |

You might have to make the script `./run_tests.sh` executable,

```bash
chmod u+x run_tests.sh
```

### On a remote server

**Important:** When the site is deployed, a file `.env` is created, which contains settings which must be kept secret. **Ensure that this file is not put under version control.**

Ubuntu 14.04 or higher must be running on the remote server, and standard commands like`ssh` must be installed. The server should not be used for anything other than running the deployed website.

Create a user `deploy` for deploying the site, and give that user sudo permissions:

```bash
adduser deploy
gpasswd -a deploy sudo
```

You may choose another username for this user, but then you have to set the `<PREFIX>_SERVER_USERNAME` environment variable accordingly. See the section on environment variables for an explanation of the prefix.

Make sure wget is installed on the server.

Login as the deploy user.

Unless your repository has public access, you should also generate an SSL key for the deploy user. Check whether there is a file `~/.ssh/id_rsa.pub` already. If there isn't, create a new public key by running

```bash
ssh-keygen
```

If you don't choose the default file location, you'll have to modify the following instructions accordingly.

Once you have the key generated, find out whether the ssh agent is running.

```bash
ps -e | grep [s]sh-agent
```

If agent isn't running, start it with

```bash
ssh-agent /bin/bash
```

Load your new key into the ssh agent:

```bash
ssh-add ~/.ssh/id_rsa
```

You can now view your public key by means of

```bash
cat ~/.ssh/id_rsa.pub
```

Refer to to the instructions for your repository host like Github or Bitbucket as to how add your key top the host.

Once all the these prerequisites are in place you may deploy the site by running

```bash
fab setup
```

Supervisor, which is used for running the Nginx server, logs both the standard output and the standard error to log files in the folder `/var/log/supervisor`. You should check these log files if the server doesn't start.

For subsequent updates you may just run

```bash
fab deploy
```

If you get an internal server error after updating, there might still be a uWSGI process bound to the requested port. Also, it seems that sometimes changes aren't picked up after deployment, even though Supervisor is restarted. 

In these cases rebooting the server should help. You can easily force the reboot by executing
 
 ```bash
 fab reboot
 ```

## Environment variables

The configuration file makes use of various environment variables. All of these must have a common prefix which is defined in the root level file `env_var_prefix`. This file must have a single line with a text string, which is taken as the prefix. Leading and trailing white space as well as trailing underscores are ignored. An underscore is affixed to the prefix.

Most of the environment variables must be defined for various configurations, which are distinguished by different infixes for the variable name:

| Configuration name | Infix |
| --- | --- |
| development | `DEV_` |
| testing | `TEST_` |
| production | no prefix |

The script `run_tests.sh` uses the testing configuration. If you launch the server with the `manage.py` script, the development configuration is used. Code deployed to a remote server uses the production configuration.

For example, if the content of the file `env_var_prefix` is `MY_APP` an environment variable name for the development configuration could be `MY_APP_DEV_DATABASE_URI`.

The following variables are required for all modes:

| Environment variable | Description | Required | Default | Example |
| --- | --- | --- | --- | --- | --- |
| `DATABASE_URI` | URI for the database access | Yes | n/a | `mysql://user:password@your.server.ip/database` |
| `LOGGING_FILE_BASE_PATH` | Base path for the error log(s) | Yes | n/a | `/var/log/my-app/errors.log` |
| `LOGGING_FILE_LOGGING_LEVEL` | Level of logging for logging to a file | No | `ERROR` | `ERROR` |
| `LOGGING_FILE_MAX_BYTES` | Maximum number of bytes before which the log file is rolled over | No | 5242880 | 1048576 |
| `LOGGING_FILE_BACKUP_COUNT` | Number of backed up log files kept | No | 10 | 5 |
| `LOGGING_MAIL_FROM_ADDRESS` | Email address to use as from address in log emails | No | `no-reply@saaoo.ac.za` | `no-reply@saaoo.ac.za` |
| `LOGGING_MAIL_LOGGING_LEVEL` | Level of logging for logging to an email | No | `Error` | `ERROR` |
| `LOGGING_MAIL_SUBJECT` | Subject for the log emails | No | `Error Logged` | `Error on Website` |
| `LOGGING_MAIL_TO_ADDRESSES` | Comma separated list of email addresses to which error log emails are sent | No | None | `John  Doe <j.doe@wherever.org>, Mary Miller <mary@whatever.org>` |
| `SECRET_KEY` | Key for password seeding | Yes | n/a | `s89ywnke56` |
| `SSL_ENABLED` | Whether SSL should be disabled | No | 0 | 0 |

The following variable have no infix (but the prefix!) and are required only if you run the commands for setting up a remote server or deploying the site.

| Environment variable | Description | Required | Default | Example |
| --- | --- |
| DEPLOY_GIT_REPOSITORY | Git repository used for deploying the site | Yes | n/a | `git@bitbucket.org:your/repository.git` |
| DEPLOY_HOST | Address of the deployment server | Yes | n/a | `my-app.org.za` |
| DEPLOY_DOMAIN_NAME | Domain name for the website | No | Value of `DEPLOY_HOST` | `my-app.org.za` |
| DEPLOY_USER | User for the deployment server | No | `deploy` | `deploy` |
| DEPLOY_USER_GROUP | Unix group for the deploy user | No | Value of `DEPLOY_USER` | `deploy` |
| DEPLOY_APP_DIR_NAME | Directory name for the deployed code | Yes | n/a | `my_app` |
| DEPLOY_WEB_USER | User for running the Tornado server | No | `www-data` | `www-data` |
| DEPLOY_WEB_USER_GROUP | Unix group of the user running the Tornado server | No | `www-data` | `www-data` |
| DEPLOY_BOKEH_SERVER_PORT | No | 5100 | 5100 |

## Adding your own environment variables

If you want to add your own environment variables for the various configuration names, you should modify the `_settings` method in `config.py`. You can get the value of your variable with the `_environment_variable` method, and you have to include this in the returned dictionary.

For example, assume you want to use an LDAP server for authentication and want to set this in an environment variable `LDAP_SERVER` (with the different prefixes for the various configurations). Then you could modify the `_settings` method as follows.

```python
def _settings(config_name)
    ...
    # LDAP server for user authentication
    ldap_server = Config._environment_variable('LDAP_SERVER', config_name)
    ...
    return dict(
        ...
        ldap_server=ldap_server,
        ...
    )
```

You can then access the variable value as `settings['ldap_server']` in the `init_app` method of `config.py`.

## Logging

The app logs errors etc. to file and optionally can send an email whenever a message is logged. Different logging levels can be set for both by means of the respective environment variables. The available levels are those defined in the `logging` module, i.e. `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG` and `NOTSET`.

The log files are automatically rolled over when their size reaches the value specified by the environment variable  `LOGGING_FILE_MAX_BYTES`. The number of backed up copies kept is set by the environment variable `LOGGING_FILE_BACKUP_COUNT`. If `LOGGING_FILE_MAX_BYTES` or `LOGGING_FILE_BACKUP_COUNT` is 0, the log file is never rolled over. See the documentation for `logging.handlers.RotatingFileHandler` for more details.

The logging handler are attached to the app. So in order to access them, you have to use code like the following.

```python
from flask import current_app

current_app.logger.error('This is an error.')
current_app.logger.warning('This is a warning.')
```

## Authentication

Currently no authentication is used, but Flask-Login is included. Modify the content of the `app.auth` package to enable authentication.

## Templates

The Jinja2 templates are located in the folder `app/templates`.

## Static files

Static files should be put in the directory `app/static` (which is Flask's default). Static files have two problems:

1. They should be bundled together, to avoid unnecessarily many HTTP requests.
2. More importantly, they are cached by browsers, and you must ensure that an updated version will actually be loaded by the browser.

This framework addresses both issues by using the Flask-Assets library, which creates bundles and attaches a GET parameter based on the bundles hash. To make use of this, you first have to define your bundles in the root-level file `webassets.yaml`. Here is an example:

```yaml
js-all:
    filters: rjsmin
    output: cache/all.%(version)s.js
    contents:
        - js/a.js
        - js/b.js
        - js/c/d.js

css-all:
    filters: yui_css
    output: cache/all.%(version)s.css
    contents:
        - css/main/a.css
        - css/main/b.css
```

Note the dashes before the file paths - these are indeed required! Also note the '%(version)s' - this is a placeholder to be replaced with the first characters of the bundle's hash.

Then you can include any of the defined bundles in a Jinja2 template by using the `assets` tag. For example,

```
{% block scripts %}
{{ super() }}
{% assets 'js-all' %}
<script src="{{ ASSET_URL }}"></script>
{% endassets %}
{% endblock %}
```

The generated bundles are put in the directory `app/static/cache`. When running the server in test or development mode, the original, individual files rather than the bundles will be included.

The deploy script automatically generates the bundles on the production server, rather than relying on them being created on the fly when a page is requested. This implies that you *don't* have to give the web user write access to the bundle directory. That user still needs write access to the directory `app/static/.webassets_cache`, though, and the deploy script takes care of that.

Some care must be taken when it comes to unit tests. If the Flask-Assets environment is defined as a global variable, running more than one unit test may result in multiple registration of the same bundle, which results in an error of the form

```
webassets.env.RegisterError: Another bundle is already registered as ...
```

This site circumvents the issue by removing all existing bundles before attempting to load bundles in the app's `__init__.py` file.

## Potential pitfalls

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

## Database access

The framework includes Flask-SQLAlchemy and makes an SQLAlchemy instance available as a variable `db` in the `app` package. You can, for example, use this to create a Pandas dataframe from an SQL query:

```python
# Pandas doesn't ship with this framework, but you can install it with
# pip install pandas
import pandas as pd

from app import db

sql = 'SELECT * FROM SomeTable'
df = pd.read_sql(sql, db.engine)
```

When using Pandas' `read_sql` function you should bear in mind that the MySQL wildcard % has to be escaped by another %, as the query is parsed as a Python format string.

## Adding a data quality page

In order to add a data quality page you have to take the following steps.

1. Create a directory in `/app/main/pages/`. It is perfectly fine to have subdirectories; so for example you could create `/app/main/pages/a/b/` instead of just `/app/main/pages/a/`.
2. In the directory create a file `__init__.py` which defines a function `title` returning the page title and a function `content` returning string with an HTML element containing the page content.

And that's it. Assuming your new directory is `/app/main/pages/a/b/` you can now access the new page at the URL `/data-quality/a/b` (or `/data-quality/a/b/` - trailing slashes are ignored).

### Example: Hello World

Let's create a Hello World page which is accessible at `/data-quality/hello/world`. To this end first create the directory for the page:

```bash
mkdir app/main/pages/hello
mkdir app/main/pages/hello/world
```

In the new directory create a file `__init__.py` with the following content.

```python
def title():
    return 'Hello World'
    
def content():
    return '<div>This is a Hello World page.</div>'
```

You can now view the page by pointing your browser at `/data-quality/hello/world`.

### Data quality content and the `data_quality` decorator

Your page presumably will contain plots, tables etc. Each of these items should be generated by a dedicated function defined in a module within your page's package.

Also, all of these functions should be decorated with the `data_quality` decorator, as shown in the following example.

```python
from app.main.data_quality import data_quality

@data_quality(name='throughput_plot`, caption='Plot of the RSS throughput.', export_name='throughput_plot')
def throughput():
    return '<div>...</div>'
```

The decorator stores the function under the name given by its `name` argument, along with all the arguments (apart from the name) passed to the decorator. You can access these using the `data_quality_item` function (also in the package `app.main.data_quality`), which expects the name (as used in the function's decorator) and package as its arguments.

Within a package the value for the name argument of the `data_quality` decorator must be unique.

The function should return a Bokeh model (such as a plot) or a string containing a valid HTML element.

It is up to you what to with the return value, but it is a good idea to use the `data_quality_item_html` function in the module `app.main.data_quality` to generate it into HTNML for a data quality page. Note that this function automatically creates the relevant HTML for Bokeh models.

### Default data quality pages

If all you need is a page with plots (or tables etc.) stacked one over another, and if this page should contain a form for querying a date range, you can use the `default_data_quality_content_for_date_range` function from the `app.main.data_quality` package to generate the content.

To do so, some requirements must be met.

* All the functions for generating a data quality item (such as a plot) must be decorated with the `data_quality` decorator.
* All of these functions must have the same signature, i.e. accept the same arguments. Most notably, they must accept a `start_date` and `end_date` argument. String values should be accepted for all the function arguments, at least if the function is returning a Bokeh model and you are planning to use the `test_bokeh_model.py` script (see below).
* All these functions must be defined in modules in the page's package.
* All these functions must return a Bokeh model (such as a plot) or a string containing a valid HTML element.
* The data quality items to display must be listed in a file `content.txt`in the page's package. Each line in this file must contain the name for the function generating the item, as passed to the name argument of the `data_quality` decorator.

You have to call the `default_data_quality_content_for_date_range` function with the pages package (as a string), a default start date, a default end date, and any additional arguments to call the data quality item functions with.

### Using Bokeh

While ultimately it is up to you how to create a plot or table, the site is including Bokeh, and it is a good idea to use it. You can just return the created  Bokeh model; there is no need to convert it into HTML. Here is a simple example:

```python
import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.main.data_quality import data_quality


@data_quality(name='weather_downtime', caption='Weather downtime for May 2016.')
def weather_downtime_plot():
    sql = 'SELECT Date, TimeLostToWeather FROM NightInfo' \
          '       WHERE Date >= \'2016-05-01\' AND Date <= \'2016-05-31\' AND TimeLostToProblems IS NOT NULL'
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    date_formatter = DatetimeTickFormatter(formats=dict(hours=['%e %b %Y'],
                                                        days=['%e %b %Y'],
                                                        months=['%e %b %Y'],
                                                        years=['%e %b %Y']))

    p = figure(title='Weather Downtime',
               x_axis_label='Date',
               y_axis_label='Downtime (seconds)',
               x_axis_type='datetime')
    p.scatter(source=source, x='Date', y='TimeLostToWeather')

    p.xaxis[0].formatter = date_formatter

    return p
```

Bokeh uses a fairly high z-index (100) for its html elements, which may cause itv to hide other (dynamic) elements like a datepicker. You then have to increase the latter's z-index. In case of a jQuery datepicker you would assigning `position: relative` and `z-index: 1000` to an ancestor of the input field using the datepicker. You may of course choose a value other than 1000, as long as it's higher than the z-index used by Bokeh.

If you require an interactive plot you should refer to the section below. 

### Example: a default data quality page

Let's create a default data quality page `/data-quality/general/downtime` with a weather and engineering downtime plot. Both plots are for a date range supplied by the user.

The first step is to create the necessary directory.

```bash
mkdir app/main/pages/general
mkdir app/main/pages/general/downtime
```

In the new directory create a file `__init__.py` with the following content.

```python
import datetime

from app.main.data_quality import default_data_quality_content_for_date_range


def title():
    return 'Telescope Downtime'


def content():
    return default_data_quality_content_for_date_range(__package__,
                                                       datetime.date.today() - datetime.timedelta(days=7),
                                                       datetime.date.today())
```

Add a file `plots.py` for the plot functions, with the following content.

```python
import pandas as pd

from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource

from app import db
from app.main.data_quality import data_quality


@data_quality(name='weather_downtime', caption='Weather downtime.')
def weather_downtime_plot(start_date, end_date):
    """Return a <div> element with a weather downtime plot.

    The plot shows the downtime for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the weather downtime plot.
    """

    return _downtime_plot('TimeLostToWeather', 'Weather Downtime', start_date, end_date)


@data_quality(name='technical_downtime', caption='Downtime due to technical problems.')
def technical_downtime_plot(start_date, end_date):
    """Return a <div> element with a plot displaying the downtime due to technical problems.

    The plot shows the downtime for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    str:
        A <div> element with the weather downtime plot.
    """

    return _downtime_plot('TimeLostToProblems', 'Downtime due to Technical Problems', start_date, end_date)


def _downtime_plot(downtime_column, title, start_date, end_date):
    """Return a <div> element with a downtime plot.

    The plot shows the downtime for the period between start_date (inclusive) and end_date (exclusive).

    Params:
    -------
    downtime_column: str
        Name of the column in the NightInfo table whose data shall be used.
    title: str
        Plot title.
    start_date: date
        Earliest date to include in the plot.
    end_date: date
        Earliest date not to include in the plot.

    Return:
    -------
    bokeh.model.Model:
        The downtime plot.
    """

    sql = 'SELECT Date, {downtime_column} FROM NightInfo' \
          '       WHERE Date >= \'{start_date}\' AND Date < \'{end_date}\' AND {downtime_column} IS NOT NULL' \
        .format(start_date=start_date, end_date=end_date, downtime_column=downtime_column)
    df = pd.read_sql(sql, db.engine)
    source = ColumnDataSource(df)

    date_formatter = DatetimeTickFormatter(formats=dict(hours=['%e %b %Y'],
                                                        days=['%e %b %Y'],
                                                        months=['%e %b %Y'],
                                                        years=['%e %b %Y']))

    p = figure(title=title,
               x_axis_label='Date',
               y_axis_label='Downtime (seconds)',
               x_axis_type='datetime')
    p.scatter(source=source, x='Date', y='{downtime_column}'.format(downtime_column=downtime_column))

    p.xaxis[0].formatter = date_formatter

    script, div = components(p)

    return '<div>{script}{div}</div>'.format(script=script, div=div)
```
 
Finally, create a file `content.txt` with the following content.
 
```
weather_downtime
technical_downtime
```

Your new page is now accessible at `/data-quality/general/downtime`.

## Adding a Plot

This is for adding a plot to an already existing page.   If a page is needed, see [adding a data quality page](https://github.com/saltastro/salt-data-quality-site#adding-a-data-quality-page) or contact Christian.  For log in details, contact Christian.    

1. Log into the development machine as user deploy. For testing you'll need an X11 connection, so use the `-X` flag with `ssh`.
2. Move into the directory for the page you want to add a plot to

    ```cd saltstatsdev.cape.saao.ac.za/app/main/pages/instrument/rss```
3. Check out a new branch to develop on

    ```git checkout -b rss_bias``
4. Make sure that your current branch is up to date.

    ```git pull origin master```
5. In a Python file (`plots.py`, say) in this directory add a function returning your plot. Make sure to annotate your function with a `data_quality` decorator, as described above.
6. Use the script `test_bokeh_model` in the root folder for testing your plot (see below).
7. Add the name of the plot (as used in the `name` argument of the `data_quality` decorator) to the `content.txt` file.
8. Deploy a test server and test the plot.

    a. In a new terminal, log in and move into the project directory and start up the server

        ```
        cd saltstatsdev.cape.saao.ac.za
        source venv/bin/activate
        python manage.py runserver -p 81 -h 0.0.0.0
        ```
    b. On a browser on your own machine, you should now be able to navigate to http://saltstatsdev.cape.saao.ac.za:81/ and see the site.
    
    c.  Navigate to the page you have created and you should be able to now see the plot added
to your site.

    d.  If there is an error or the plot does not display, check the `/home/deploy/errors.log` file for details.  Once the code has been updated, reload the page to see if it will display without errors.   
8. Once the plot works, commit the code to github. 
9. Alert Christian to restart the server so that the new plot is displayed on the live site. 

### Using the test_bokeh_model.py script

For convenience, the app's root folder (`~deploy/saltstatsdev.cape.saao.ac') contains a script for testing Bokeh models (such as plots). To use this script, first activate the virtual environment (if it isn't active already),

```bash
source venv/bin/activate
```

You can then run the script as follows,

```bash
python test_bokeh_model.py path/to/your/plots/file plot_function_name [plot_function_arg1 plot_function_arg2 ...]
```

The path is that of the Python file containing your plot function, the function name is the name of your function (*not* the name attribute of its `data_quality` decorator), and the remaining arguments are passed to your function.

For example, a call to the script might be

```bash
python test_bokeh.py app/main/pages/examples/example2/plots.py weather_downtime_plot 2016-06-01 2016-06-19
```

### Interactive plots

Bokeh supports interactivity by adding JavaScript to your plot or by hosting your plot on a Bokeh server. You can use both on the data quality site.

In order to add JavaScript to your plot, you may define a callback with CustomJS and pass this callback to a widget constructor. See [http://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html](http://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html) for examples.

While adding JavaScript in this way is straightforward, it is limited. For example, you cannot perform a new database query. Also, it is arguably much easier to define your callbacks in Python, enjoying full IDE support, rather than to have write a string containing JavaScript code.

These shortcomings fall away if you use a Bokeh server for hosting your plot, as then you you can add (Python) callbacks to your widgets which can update your plot's source data. An example of this is shown below.

**Plots served by the Bokeh server are not password-protected.**

You need to put the file with your plot in the folder `bokeh_server`. All files in this folder (but not in its subfolders) is assumed to contain a plot to be hosted. So you should avoid putting helper files in this folder (although you are perfectly fine to put them in subfolders).

In order to include an interactive plot on a page, you have to use Bokeh's `autoload_server` function to get the necessary html. So a plot function might look as follows.

```python
@data_quality(name='interactive_downtime_plot', caption='Telescope downtime.')
def content():
    up = urlparse(request.url)
    scheme = up.scheme
    host = up.netloc
    port = up.port
    if port:
        host = host[:-(len(str(port)) + 1)]
    bokeh_server_url = '{scheme}://{host}:5100'.format(scheme=scheme, host=host)
    script = autoload_server(model=None, app_path='/telescope_downtime', url=bokeh_server_url)
    return '<div>' + script + '</div>'
```

The plot for this would have to be defined in a file `bokeh_server/telescope_downtime.py`. Note the port number 5100; this is not the default port (5006) of a Bokeh server.

### Example: an interactive plot with a two-dimensional Gaussian distribution

Assume you want to display a two-dimensional Gaussian distribution centred on the the origin and let the user choose a standard deviation as well as a cutoff value for the distance from the origin. When the user changes the standard deviation, the current set of random points is replaced with a new points. Points beyond the cutoff should have a lower opacity.

Then you could create a file `bokeh_server/gaussian.py with the following Python code.

```python
import math
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Range1d
from bokeh.models.widgets import Slider
from bokeh.plotting import ColumnDataSource, Figure

# --------------------------------------------------------
#
# An interactive plot showing normally distributed points.
#
# --------------------------------------------------------

# number of points shown in the plot
NUM_POINTS = 100

standard_deviation_slider = Slider(title='standard deviation', value=2, start=0, end=4)
cutoff_slider = Slider(title='maximum radius', value=4, start=0, end=8)

source = ColumnDataSource()


def update_source_data(new_points):
    """Update the source data.

    If new_points is True, random points will be generated. A normal distribution is used, and its standard deviation
    is the value of the standard deviation slider.

    The opacity of the points is chosen according to whether their distance from the origin is greater than the value
    of the cutoff slider.

    Params:
    -------
    new_points: bool
        Whether to generate new points.
    """

    standard_deviation = standard_deviation_slider.value
    cutoff = cutoff_slider.value

    # generate new points if requested

    if new_points:
        if standard_deviation > 0:
            x = np.random.normal(0, standard_deviation, NUM_POINTS)
            y = np.random.normal(0, standard_deviation, NUM_POINTS)
        else:
            x = np.zeros(NUM_POINTS)
            y = np.zeros(NUM_POINTS)
        source.data['x'] = x
        source.data['y'] = y

    # update the opacity

    def radius(u, v):
        """The distance from the origin."""

        return math.sqrt(u ** 2 + v ** 2)

    x = source.data['x']
    y = source.data['y']
    alpha = [1 if radius(x[i], y[i]) <= cutoff else 0.1 for i in range(NUM_POINTS)]

    source.data['alpha'] = alpha


# initialize the plot data
update_source_data(True)

# make the plot responsive to slider changes
standard_deviation_slider.on_change('value', lambda attr, old_value, new_value: update_source_data(True))
cutoff_slider.on_change('value', lambda attr, old_value, new_value: update_source_data(False))

# create the figure

p = Figure(title='Normal Distribution')

p.scatter(source=source, x='x', y='y', color='green', alpha='alpha', radius=0.1)

p.x_range = Range1d(start=-8, end=8)
p.y_range = Range1d(start=-8, end=8)

content = column(standard_deviation_slider, cutoff_slider, p)

# register the figure

curdoc().add_root(content)
curdoc().title = 'Normal Distribution'
```

In the plots file of the page where the plot is to be shown you could add the following function.

```python
from urllib.parse import urlparse

from bokeh.embed import autoload_server
from flask import request


@main.route('/gaussian')
def gaussian():
    up = urlparse(request.url)
    scheme = up.scheme
    host = up.netloc
    port = up.port
    if port:
        host = host[:-(len(str(port)) + 1)]
    bokeh_server_url = '{scheme}://{host}:5100'.format(scheme=scheme, host=host)
    script = autoload_server(model=None, app_path='/gaussian', url=bokeh_server_url)
    return '<div>' + script + '</div>'
@data_quality(name='gaussian_2d_plot', caption='Two-dimensional Gaussian distribution.')
def content():
    up = urlparse(request.url)
    scheme = up.scheme
    host = up.netloc
    port = up.port
    if port:
        host = host[:-(len(str(port)) + 1)]
    bokeh_server_url = '{scheme}://{host}:5100'.format(scheme=scheme, host=host)
    script = autoload_server(model=None, app_path='/gaussian', url=bokeh_server_url)
    return '<div>' + script + '</div>'
```

### Testing interactive Bokeh plots

In order to test an interactive plot (in a filer `bokeh_serve/gaussian.py`, say), go to the `bokeh_server` folder and start a Bokeh server with the plot file.

```bash
source venv/bin/activate
cd bokeh_server
bokeh serve gaussian.py
```

You can then view the plot by pointing a browser at `http://localhost:5006/gaussian`.

## Testing

Unit tests, Behave tests and PEP8 tests are supported.

### Unit tests

You should add all your unit tests to the folder `tests/unittests`. For convenience a base test case class `tests.unittests.base.BaseTestCase` is provided, which sets up and tears down the Flask environment. This class also creates a test client, which can be accessed as `self.client`. This test client is using cookies.

In addition, the `test.unittests.base` module offers a class `NoAuthBaseTestCase`, which extends the `BaseTestCase` class and disables authentication, meaning that `login_required` decorators for routes are ignored.

A unit test using the `NoAuthBaseTestClass` might look as follows.

```python
from tests.unittests.base import NoAuthBaseTestCase


class NoAuthBasicsTestCase(NoAuthBaseTestCase):
    def test_homepage_exists(self):
        response = self.client.get('/')
        self.assertTrue(response.status_code == 200)
```

### Behave tests

[Behave](https://pythonhosted.org/behave/index.html) feature files should be put in the folder `tests/features`, and the corresponding step implementation files in `tests/features/steps`.

The context variable passed to the step implementations provides access to the Flask app and a test client (which are set up in the `environment.py` module). The test client is using cookies. The following example illustrates how the test client can  be used.

```python
from behave import *

use_step_matcher("re")


@when('I access the homepage')
def step_impl(context):
    context.response = context.client.get('/')


@then('I get a page with no error')
def step_impl(context):
    assert context.response.status_code == 200
```

### PEP8 tests

The testing script mentioned in the next subsection includes PEP8 checking.

### Running the tests 

The Bash script `run_tests.sh` allows you to run your tests. In addition it uses the `pycodestyle` module to check compliance with PEP8. Regarding the latter a maximum line length of 120 is assumed and module level imports aren't forced to be at the top of a file.

If you want to enforce that git commits can only be pushed if all tests are passed, you may use a git hook. If there is a pre-push hook already, modify it to include the content of the `run_tests.sh` script. Otherwise just copy the script and ensure the hook is executable:

```bash
cp run_tests.sh .git/hooks/pre-push
chmod u+x .git/hooks/pre-push
```




