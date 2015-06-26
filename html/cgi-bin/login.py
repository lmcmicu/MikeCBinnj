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

# this script must be passed a username and password:
arguments = cgi.FieldStorage()
if "uname" not in arguments or "passwd" not in arguments:
    lunchlib.write_fail("Username and password not received by POST.")
else:
    uname = arguments["uname"].value
    passwd = arguments["passwd"].value

    # connect to the database:
    db = pg.DB(dbname=lunchlib.dbname, host=lunchlib.dbhost,
               user=lunchlib.dbuser, passwd=lunchlib.dbpasswd)

    # check if the user exists and if so, retrieve her password:
    rows = db.query('''
                    select passwd
                    from employee
                    where uname='{0}'
                    '''.format(uname)).getresult()
    if not rows or not rows[0]:
        lunchlib.write_fail("No such user")
    else:
        # password should be in the first and only field of the
        # first and only row:
        retrievedpw = rows[0][0]

        # verify that supplied password is the same as the retrieved one:
        if not hashpw(passwd, retrievedpw) == retrievedpw:
            # if not, write out some html informing of a mismatch:
            lunchlib.write_fail("Incorrect password")
        else:
            # otherwise write out some html informing of a success
            lunchlib.write_js('''
                function goToMainMenu(form) {
                        // proceed to main menu when button is pressed:
                        form.setAttribute("action", "menu.py");
                        form.submit();
                }
            ''')
            lunchlib.write_head_uname(uname)

            lunchlib.write_form('''
                <p><input type="button" value="OK" onClick="goToMainMenu(this.form)">
                <p><input type="hidden" name="uname" value="''' + uname + '''">
            ''')

            lunchlib.write_tail()

    # close database connection:
    db.close()
