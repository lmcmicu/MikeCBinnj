#!/usr/bin/env python

# for common gateway interface functionality:
import cgi

# custom user library:
import lunchlib

# cgi requires this:
print "Content-Type: text/html"
print

# script must be supplied with username:
arguments = cgi.FieldStorage()
if "uname" not in arguments:
    lunchlib.write_fail("Username not received in POST.")
else:
    uname = arguments["uname"].value

    # write out html code for lunch entry form:
    lunchlib.write_js('''
        function insertLunch(form) {
            // check first to see if date is in desired format:
            dateRegexp = /^\d{4}-\d{2}-\d{2}$/.test(form.ldate.value)
            if (!dateRegexp) {
               alert("bad date format.");
               return;
            }

            // extract parts of the date
            bits = form.ldate.value.split('-');
            var year = bits[0];
            var month = bits[1];
            var day = bits[2];

            // create a new date object. note that the Date constructor
            // assumes January is the 0th month, so we must subtract 1
            // from our month value before calling the constructor:
            var testDate = new Date(year, month - 1, day);

            // make sure that the supplied date is not in the future:
            if (testDate > new Date()) {
                alert("date in the future.");
                return;
            }
  
            // if date is in the right format, make sure it is valid:
            if (year < 1 || month > 12 || month < 1 || day < 1) {
               alert("invalid date.");
               return;
            }
            else if (month == 1 || month == 3 || month == 5 ||
                month == 7 || month == 8 || month == 10 ||
                month == 12) {
                // some months have 31 days:
                if (day > 31) {
                   alert("invalid date.");
                   return;
                }
            }
            else if (month == 4 || month == 6 || month == 9 ||
                     month == 11) {
                // some months have 30 days:
                if (day > 30) {
                   alert("invalid date.");
                   return;
                }
            }
            else if (month == 2) {
                // February may have 28 or 29 days depending on the year:
                if ((year % 4) == 0 &&
                    ((year % 100) != 0 || (year % 400) == 0)) {
                   if (day > 29) {
                       alert("invalid date.");
                       return;
                   }
                }
                else {
                   if (day > 28) {
                       alert("invalid date.");
                       return;
                   }
                }
            }

            // now validate the amount. No one is allowed to spend more
            // than 9999.99 dollars on lunch!
            // note also that you can't input more than two decimal places
            if (/^\d{1,4}(\.\d{0,2}){0,1}$/.test(form.amount.value)
                == false) {
                alert("invalid amount.");
                return;
            }

            // if we get to here then we can call the code to insert the
            // lunch expense in the database:
            form.setAttribute("action", "insertLunch.py");
            form.submit();

        }

        // do not enter a lunch expense and go back to the main menu:
        function cancel(form) {
            form.setAttribute("action", "menu.py")
            form.submit();
        }
    ''')

    # write html header:
    lunchlib.write_head_uname(uname)

    print "<h3>Enter a lunch expense for a day</h3>"

    lunchlib.write_form('''
          <p>Date (yyyy-mm-dd): <input type="text" name="ldate"><br/>
          <p>Amount Spent: <input type="text" name="amount"><br/>
             (format: dollars[.cents], do not type "$", max.: 9999.99)
          <p><input type="button" value="Submit"
                                onClick="insertLunch(this.form)">
          <p><input type="button" value="Cancel"
                                onClick="cancel(this.form)">
          <p><input type="hidden" name="uname" value="''' + uname + '''">
    ''')

    # html footer
    lunchlib.write_tail()
