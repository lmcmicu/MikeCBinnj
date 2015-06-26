required:
---------
python (2.7.5-5ubuntu3)
python-bcrypt (0.4-1ubuntu2)
apache2 (2.4.7-1ubuntu4.4)
postgresql (9.3+154ubuntu1)
postgresql-contrib (9.3+154ubuntu1)

installation:
------------
- create the database 'binnjLunch' on your postgres server

- in the SQL/ directory located under the main repository
directory, use the file create_schema.sql to create the
tables in the binnjLunch database (e.g. by redirecting
it to psql).

- in the PythonLib/ directory located under the main repository
directory, copy the file lunchlib.py to a desired location
(e.g. /usr/lib/python2.7/) and make sure
this location is available in your web server's PYTHONPATH.

- edit the database connection parameters in lunchlib.py
as required.

- in the html/ directory located under the main repository directory,
copy cgi-bin/, login.html, newuser.html into your http server's
main directory (e.g., /var/www/) or wherever else they will be visible
via http (e.g. in some user's public_html/ directory).

- point your browser to the login.html page. E.g. if the application
has been installed in ~mike/public_html/ this would be:
http://<host ip address>/~mike/login.html

- enjoy. Note that the database starts empty. You will have to
populate it with users through the web interface.
