#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import mysql.connector
import hashlib
config = {
  'user': 'root',
  'password': 'scorpion',
  'host': 'localhost',
  'database': 'blog',
  'raise_on_warnings': True,
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="../styles.css">
            <title>Title</title>
        </head>
        <body>""")
form = cgi.FieldStorage()
username = form.getfirst("username")
initialPass = form.getfirst("password", "")
initialPass = html.escape(initialPass)
hash_object = hashlib.md5(initialPass.encode())
password = hash_object.hexdigest()


firstname = form.getfirst("first_name")
lastname = form.getfirst("last_name")
email = form.getfirst("email", "")
username = html.escape(username)
firstname = html.escape(firstname)
lastname = html.escape(lastname)
email = html.escape(email)

insertQuery = "insert into users(username, password, first_name, last_name, email) \
				values ('%s', '%s', '%s', '%s', '%s')" % (username, password, firstname, lastname, email)

# Execute the SQL command
try:
	checkUserQuery = "select * from users where username = '%s' and password = '%s'" % (username, password)
	cursor.execute(checkUserQuery)
	row = cursor.fetchone()

	if(row is not None):
		print("""<p>User: \"{}\" Already Exists</p>""".format(username))
	else:
		print("""<p>Enter Username and Password to Log in!</p>""")
		cursor.execute(insertQuery)
		connection.commit()

except Exception:
	print("""Exception!""")
# Fetch all the rows in a list of lists.
else:
	
	print("""<form method="POST" action="/cgi-bin/wall.py">
		        Username <input type="text" name="username" required placeholder="your username">
		        Password <input type="password" name="password"required placeholder="your password">
				<input type="submit" value="Log in"></br></br>
			  </form>
		    <p>Create new Account</p>
		    <form method="POST" action="/cgi-bin/registration.py">
			    <span>Enter FirstName *</span><br>
		        <input type="text" name="first_name" required placeholder="your firstname"><br>
		        <span>Enter LastName *</span><br>
		        <input type="text" name="last_name" required placeholder="your lastname"><br>
		        <span>Enter Username *</span><br>
		        <input type="text" name="username" required placeholder="your username"><br>
		        <span>Enter Password *</span><br>  
		        <input type="password" name="password" required placeholder="your password"><br>
		        <span>Enter Email </span><br>  
				<input type="text" name="email" placeholder="your email"><br>
				<input type="submit" value="Registrate">
		    </form>""")

print("""</body>
        </html>""")
cursor.close()
connection.close()