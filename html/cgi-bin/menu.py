#!/usr/bin/env python

# for common gateway interface functionality:
import cgi

# custom user library:
import lunchlib

# cgi requires this:
print "Content-Type: text/html"
print

# this script must be supplied with a username:
arguments = cgi.FieldStorage()
if "uname" not in arguments:
    lunchlib.write_fail("Username not received in POST.")
else:
    uname = arguments["uname"].value

    # write out the menu options in html:
    lunchlib.write_js('''
        function enterLunchExp(form) {
            // go to lunch expense entry form:
            form.setAttribute("action", "lunchForm.py");
            form.submit();
        }

        function detailedReport(form) {
            // go to lunch expense reporting form:
            form.setAttribute("action", "detailedReportForm.py");
            form.submit();
        }

        function logout(form) {
            // go back to the login page.
            // do not pass any form data since the user has logged out.
            location="../login.html"
        }
    ''')

    lunchlib.write_head_uname(uname)

    print "<h3>Main Menu</h3>"

    lunchlib.write_form('''
        <p><input type="button" value="Add to lunch expenditures"
                onClick="enterLunchExp(this.form)">
        <p><input type="button" value="List of monthly lunch expenditures"
                onClick="detailedReport(this.form)">
        <p><input type="button" value="Logout"
                onClick="logout(this.form)">
        <p><input type="hidden" name="uname" value="''' + uname + '''">
    ''')

    lunchlib.write_tail()
