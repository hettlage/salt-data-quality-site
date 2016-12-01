# If you have no time...

While the SALT data quality site framework tries to make adding plots as simple as possible, getting a plot up-and-running on the server can have its intricacies. But there are two alternative options.

## If you have absolutely no time

In case you have no time to create a plot, you should speak to Nhlavutelo and Christian about your needs, and they'll create the plot for you.

## If you have a bit of time

In case you have the time to create a plot, you can come up with your (static) plot on your own machine. You don't need a web server for this, and brief instructions are given in the next section.

Once finished, you should send your shiny new plot file to Nhlavutelo and Christian.

## Creating a plot with Bokeh

Please make sure you are using Python 3 before you start creating your plot. Bokeh might require the latest version, 3.5 at the time of writing. An easy way to get Python 3 with all the necessary libraries is to install [Anaconda](http://continuum.io/anaconda).

If you are using Anaconda, you can install Bokeh by means of its conda command.

```bash
conda install bokeh
```

Otherwise you can use pip (preferably in a virtual environment).

```bash
pip install numpy
pip install bokeh
```

To test the Bokeh installation, create and run a Python file with the following content.

```python
import math
import numpy as np

from bokeh.plotting import figure, output_file, show


output_file('output.html')

x = np.linspace(0, 2 * math.pi)
y = np.sin(x)

p = figure(title='Sine')
p.line(x, y)

show(p)
```

In case you are running your code in a Jupyter notebook, you should use the function `output_notebook` instead of `output_file`.

A good introduction to Bokeh is provided by the [user guide](http://bokeh.pydata.org/en/latest/docs/user_guide.html) on the Bokeh website.