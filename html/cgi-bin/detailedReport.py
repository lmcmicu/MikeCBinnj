#!/usr/bin/env python

# for database access
import pg

# for cgi functionality
import cgi

# custom user library
import lunchlib


######## functions used to write the detailed and summary reports:

#detailed report:
def write_detailed_report(uname, start_month, end_month, db):
    detailed_rows = db.query('''
                       select l.lunch_date, to_char(l.amount,'9999.99')
                       from employee e inner join lunch_expenses l
                       on e.id = l.emp_id
                       where to_char(l.lunch_date,'YYYY-MM') >= '{0}'
                             and to_char(l.lunch_date,'YYYY-MM') <= '{1}'
                             and e.uname = '{2}'
                       order by l.lunch_date
                       '''.format(start_month,end_month,uname)).getresult()

    if not detailed_rows or not detailed_rows[0]:
        print "No data returned"
        return False
    else:
        # output the report as a html table
        print '<h4>Daily Expenditures</h4>'
        print '''<table cellpadding="12" border="1">
                 <tr><td><b>Date</b></td><td><b>Amount</b></td></tr>'''

        # each row gets a <tr> (table row) and each field a <td>
        for detailed_row in detailed_rows:
            print "<tr>"
            for field in detailed_row:
                print "<td>" + field + "</td>"
            print "</tr>"

        print "</table>"

        return True

#summary report:
def write_summary_report(uname, start_month, end_month, db):
    summary_rows = db.query('''
                      select to_char(l.lunch_date,'YYYY-MM'),
                             to_char(sum(l.amount),'9999.99')
                      from employee e inner join lunch_expenses l
                           on e.id = l.emp_id
                      where to_char(l.lunch_date,'YYYY-MM') >= '{0}'
                            and to_char(l.lunch_date,'YYYY-MM') <= '{1}'
                            and e.uname = '{2}'
                      group by to_char(l.lunch_date,'YYYY-MM')
                      order by to_char(l.lunch_date,'YYYY-MM')
                      '''.format(start_month,end_month,uname)).getresult()

    if not summary_rows or not summary_rows[0]:
        print "No summary data returned"
        return False
    else:
        # output the report as a html table:
        print '<h4>By Month</h4>'
        print '''<table cellpadding="12" border="1">
                 <tr><td><b>Month</b></td><td><b>Amount</b></td></tr>'''

        # each row gets a <tr> and each field a <td>
        for summary_row in summary_rows:
            print "<tr>"
            for field in summary_row:
                print "<td>" + field + "</td>"
            print "</tr>"

        print "</table>"

        return True


######## main processing starts here:

# needed for cgi
print "Content-Type: text/html"
print

# this script requires at least a username and start month:
arguments = cgi.FieldStorage()
if "uname" not in arguments or "start_month" not in arguments:
    lunchlib.write_fail("Some data not received in POST.")
else:
    uname = arguments["uname"].value
    start_month = arguments["start_month"].value

    # grab the end month if it has been supplied,
    # otherwise default to the same as the start month:
    if "end_month" not in arguments:
        end_month = start_month;
    else:
        end_month = arguments["end_month"].value

    # write javascript for going back to main menu:
    lunchlib.write_js('''
        function goToMainMenu(form) {
            form.setAttribute("action", "menu.py");
            form.submit();
        }
    ''')

    # write html header
    lunchlib.write_head_uname(uname)

    # connect to the database
    db = pg.DB(dbname=lunchlib.dbname, host=lunchlib.dbhost,
               user=lunchlib.dbuser, passwd=lunchlib.dbpasswd)

    # report header
    print "Report for user: <b>" + uname + "</b> for period: <b>" + \
        start_month + " to " + end_month +"</b><br/><br/>"

    # form to go back to main menu
    lunchlib.write_form('''
         <p><input type="button" value="Back to Menu"
             onClick="goToMainMenu(this.form)">
         <p><input type="hidden" name="uname" value="''' + uname + '''">
    ''')

    # both reports will be part of a larger overall table:
    print "<table><tr>"
    print "<td>"

    # Only run summary report if there is data in the detailed report.
    if write_detailed_report(uname, start_month, end_month, db):
        print '</td><td width="60"></td><td>'
        write_summary_report(uname, start_month, end_month, db)

    print "</td></tr></table>"

    # html footer
    lunchlib.write_tail()

    # close database connection:
    db.close()
