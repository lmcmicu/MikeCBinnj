#!/usr/bin/env python

# for password hashing:
from bcrypt import hashpw, gensalt

# for database access:
import pg

# for common gateway interface functionality
import cgi

# custom user library
import lunchlib

# content type must always be specified for cgi:
print "Content-Type: text/html"
print

# this script must be passed a username, password, first and last name:
arguments = cgi.FieldStorage()
if "uname" not in arguments or "passwd" not in arguments \
   or "fname" not in arguments or "lname" not in arguments:
    lunchlib.write_fail("Some data was not received by POST")
else:
    uname = arguments["uname"].value
    plainpw = arguments["passwd"].value
    fname = arguments["fname"].value
    lname = arguments["lname"].value

    # connect to the database:
    db = pg.DB(dbname=lunchlib.dbname, host=lunchlib.dbhost,
               user=lunchlib.dbuser, passwd=lunchlib.dbpasswd)

    # check if username already exists
    rows = db.query('''
                    select 1
                    from employee
                    where uname='{0}'
                    '''.format(uname)).getresult()
    if rows:
        lunchlib.write_fail("A user with that username already exists!")
    else:
        # encrypt the password:
        hashedpw = hashpw(plainpw, gensalt())

        # store new record for user into the employee table
        updValues = {'uname':uname, 'passwd':hashedpw, 'fname':fname,
                     'lname':lname}
        if db.insert("employee", updValues) == None:
            lunchlib.write_fail("Problem inserting new user to database")
        else:
            lunchlib.write_succeed("User created successfully!")


    # close the database connection:
    db.close()

