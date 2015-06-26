#!/usr/bin/env python

# for common gateway interface functionality:
import cgi

# user custom library:
import lunchlib

# required by cgi:
print "Content-Type: text/html"
print

# this script must be supplied with a username:
arguments = cgi.FieldStorage()
if "uname" not in arguments:
    lunchlib.write_fail("Username not received in POST.")
else:
    uname = arguments["uname"].value

    # javascript to validate input and go forward to report generation:
    lunchlib.write_js('''
        function goToDetailedReport(form) {
            // check to see if the start month is written correctly:
            if (/^\d{4}-\d{2}$/.test(form.start_month.value)) {
                // if the format is correct, split up the string:
                bits = form.start_month.value.split('-');

                // use the parts to construct a new date object to compare to
                // the current date. Note that the constructor assumes that
                // January is the 0th month, so subtract 1.
                // Also give the "day" paramater a value of the 1st
                // of the month
                var testDate = new Date(bits[0], bits[1]-1, 1);

                // supplied month should not be in the future.
                // note that we don't care how far in the past it is.
                if (testDate > new Date()) {
                    alert("month is in the future.");
                    return;
                }
            }
            else {
                // return if the format is incorrect:
                alert("invalid start month format.");
                return;
            }

            // check to see if "end month" parameter is present.
            // If so, check its format as well. Note we don't care
            // if it is in the future.
            if (/^\s*$/.test(form.end_month.value) == false &&
                /^\d{4}-\d{2}$/.test(form.end_month.value) == false) {
                alert("invalid end month format.");
                return;
            }

            // if all is ok then call the report generation script:
            form.setAttribute("action", "detailedReport.py");
            form.submit();
        }

        // do not run the report and go back to the main menu:
        function cancel(form) {
            form.setAttribute("action", "menu.py")
            form.submit();
        }
    ''')

    # html header
    lunchlib.write_head_uname(uname)

    # input form:
    lunchlib.write_form('''
          <p>Start Month (yyyy-mm): <input type="text" name="start_month">
          <p>End Month (yyyy-mm): <input type="text" name="end_month">
             <i>(if left blank, defaults to start month)</i><br/>
          <p><input type="button" value="Submit"
                                onClick="goToDetailedReport(this.form)">
          <p><input type="button" value="Cancel"
                                onClick="cancel(this.form)">
          <p><input type="hidden" name="uname" value="''' + uname + '''">
    ''')

    # html footer
    lunchlib.write_tail()
