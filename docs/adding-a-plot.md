# Adding a Plot

This is for adding a plot to an already existing page.   If a page is needed, speak to Christian for help with  [adding a data quality page](https://github.com/saltastro/salt-data-quality-site#adding-a-data-quality-page).  For log in details, contact Christian.

If your plot is interactive (for example because it includes a slider for choosing a cutoff level), you should refer to the section on [interactive plots](interactive-plots.md).

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
    sudo -E venv/bin/flask run -p 81 -h 0.0.0.0
    ```

    b. On a browser on your own machine, you should now be able to navigate to http://saltstatsdev.cape.saao.ac.za:81/ and see the site.
    
    c.  Navigate to the page you have created and you should be able to now see the plot added to your site.

    d.  If there is an error or the plot does not display, check the `/home/deploy/errors.log` file for details.  Once the code has been updated, reload the page to see if it will display without errors.
    
8. Once the plot works, commit the code to github. 
9. Alert Christian to restart the server so that the new plot is displayed on the live site.

# Using the test_bokeh_model.py script

For convenience, the app's root folder (`~deploy/saltstatsdev.cape.saao.ac') contains a script for testing Bokeh models (such as plots). To use this script, first activate the virtual environment (if it isn't active already),

```bash
source venv/bin/activate
```

You can then run the script as follows,

```bash
sudo -E venv/bin/python python test_bokeh_model.py path/to/your/plots/file plot_function_name [plot_function_arg1 plot_function_arg2 ...]
```

The path is that of the Python file containing your plot function, the function name is the name of your function (*not* the name attribute of its `data_quality` decorator), and the remaining arguments are passed to your function.

For example, a call to the script might be

```bash
sudo -E venv/bin/python test_bokeh.py app/main/pages/examples/example2/plots.py weather_downtime_plot 2016-06-01 2016-06-19
```
