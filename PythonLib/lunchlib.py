# database connection parameters:
dbname = 'binnjLunch'
dbhost = 'localhost'
dbuser = 'postgres'
dbpasswd = 'postgres'

# html header
def write_head():
    print '''
    <html>
    <head><title>Lunch Manager</title></head>
    <body>
    <h2>Lunch Manager</h2>
    '''

# html header including username:
def write_head_uname(uname):
    print '''
    <html>
    <head><title>Lunch Manager</title></head>
    <body>
    <h2>Lunch Manager</h2>
    <h3>Logged in as ''' + uname + "</h3>"

# html footer
def write_tail():
    print '''
    </body>
    </html>
    '''

# "Try again" button
def write_fail_button():
    print '''
    <form method="post" action="../login.html">
    	<p><input type="submit" value="Try again">
    </form>
    '''

# OK button
def write_succeed_button():
    print '''
    <form method="post" action="../login.html">
    	<p><input type="submit" value="OK">
    </form>
    '''

# back to main menu button
def write_menu_button():
    print '''
    <form method="post" action="menu.py">
    	<p><input type="submit" value="Back to menu">
    </form>
    '''

def write_fail_menu(message):
    write_head()
    print message
    write_menu_button()
    write_tail()

def write_fail(message):
    write_head()
    print message
    write_fail_button()
    write_tail()

def write_succeed(message):
    write_head()
    print message
    write_succeed_button()
    write_tail()

# to write a block of javascript
def write_js(text):
    print '''
    <script type="text/javascript" language="JavaScript">
    '''
    print text
    print "</script>"

# to write a form:
def write_form(text):
    print '''
    <form method="post">
    '''
    print text
    print "</form>"
