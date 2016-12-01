# SALT Data Quality Site

A website for displaying data quality measurements done for the Southern African Large Telescope (SALT).

## If you have no time...

If you are pressed for time, you should have a look at the section on [what to do if you have no time](docs/no-time.md).

## If you are an astronomer adding a plot to the site...

In most cases, you just need to add a [Bokeh](http://bokeh.pydata.org/) plot to an already existing page. This is covered by the section on [adding a plot](docs/adding-a-plot.md).

The section on [potential pitfalls](docs/potential-pitfalls.md) might save you from some head-scratching.

If you need a new page for your plot(s), you should refer to the section on [adding a database quality page](docs/adding-a-data-quality-page.md). In case your page contains a form for query parameters (such as a start and date) you should also have a look at the section on [storing query parameters](docs/storing-query-parameters.md).

Fancy plots allowing user interaction may require a slightly different approach and are covered in the section on [interactive plots](docs/interactive-plots.md).

It is always a good idea to test, and the above-mentioned sections include instructions on how you can test your plots. But you might also have a look at the section on [testing](docs/testing.md), in particular as the script described in that section allows you to check [PEP-8](https://www.python.org/dev/peps/pep-0008/) compliance.

## Table of contents

* [Installation](docs/installation.md)
* [Environment variables](docs/environment-variables.md)
* [Logging](docs/logging.md)
* [Authentication](docs/authentication.md)
* [Flask templates](docs/templates.md)
* [Static files](docs/static-files.md)
* [Database access](docs/database-access.md)
* [Storing query parameters](docs/storing-query-parameters.md)
* [Potential pitfalls](docs/potential-pitfalls.md)
* [Adding a data quality page](docs/adding-a-data-quality-page.md)
* [Adding a plot](docs/adding-a-plot.md)
* [Interactive plots](docs/interactive-plots.md)
* [Testing](docs/testing.md)






