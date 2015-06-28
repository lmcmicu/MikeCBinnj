#!/usr/bin/env python

# for database access:
import pg

# for common gateway interface access:
import cgi

# custom user library:
import lunchlib

# necessary for cgi:
print "Content-Type: text/html"
print

# this script must be passed a username, lunch date, and lunch amount:
arguments = cgi.FieldStorage()
if "uname" not in arguments or "ldate" not in arguments \
   or "amount" not in arguments:
    lunchlib.write_fail("Some data not received in POST.")
else:
    uname = arguments["uname"].value
    ldate = arguments["ldate"].value
    amount = arguments["amount"].value

    # html that will eventually be written to the page:
    status_message = ""

    try:
        # connect to the database:
        db = pg.DB(dbname=lunchlib.dbname, host=lunchlib.dbhost,
                   user=lunchlib.dbuser, passwd=lunchlib.dbpasswd)

        # retrieve the id corresponding to this username:
        rows = db.query('''
                        select id
                        from employee
                        where uname='{0}'
                       '''.format(uname)).getresult()

        if not rows or not rows[0]:
            lunchlib.write_fail("No such user")
        else:
            emp_id = rows[0][0]

            # check to see if an entry for this user on the date requested
            # already exists:
            rows = db.query('''
                            select 1
                            from lunch_expenses
                            where emp_id='{0}'
                                  and lunch_date='{1}'
                            '''.format(emp_id,ldate)).getresult()

            # if it does, then delete it first:
            if rows:
                updValues = {'emp_id':emp_id, 'lunch_date':ldate}
                if db.delete("lunch_expenses", updValues) == 0:
                    status_message = status_message + \
                                     "problem deleting exising row in database"
                else:
                    status_message = status_message + "Previous entry for " + \
                                     ldate + " overwritten.<br/>"
            # end of if rows block

            # now insert the new entry to the database:
            updValues = {'emp_id':emp_id, 'lunch_date':ldate, 'amount':amount}

            if db.insert("lunch_expenses", updValues) == None:
                status_message = status_message + \
                                 "Problem inserting row to database"
            else:
                status_message = status_message + "New entry for " + \
                                 ldate + " inserted successfully!"

            # write out the html page:
            lunchlib.write_js('''
                function goToMainMenu(form) {
                    // go back to main menu:
                    form.setAttribute("action", "menu.py");
                    form.submit();
                }
            ''')

            # html header
            lunchlib.write_head_uname(uname);

            # information message
            print status_message

            # form to go back to main menu
            lunchlib.write_form('''
                <p><input type="button" value="OK" onClick="goToMainMenu(this.form)">
                <p><input type="hidden" name="uname" value="''' + uname + '''">
            ''');

            # html footer
            lunchlib.write_tail();

        # close db connection
        db.close()

    except pg.InternalError:
        lunchlib.write_fail("Could not connect to database")
