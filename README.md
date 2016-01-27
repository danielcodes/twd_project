# Tango with Django Tutorial

First tutorial I used for learning Django, check out their [site](http://www.tangowithdjango.com/book17/)

The project is called Rango. The application displays categories which are unique, and these categories contain pages.


.. picture here


To run locally,
first clone the repo down,
``` https://github.com/danielcodes/twd_project.git ```

Switch over to the no-search branch, 
``` git checkout no-search ```

From here you need to setup a virtualenv and install the dependencies,
* ``` virtualenv tango ```, then activate it with ``` source tango/bin/activate ```
* ``` pip install -r requirements.txt ```

since a database was provided from the repo, just run
``` python manage.py runserver ```
and head ``` http://localhost:8000/rango/ ``` and you should see the page :)
