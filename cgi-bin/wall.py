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
            <title>Title</title>
            <link rel="stylesheet" href="../styles.css">

        </head>
        <body>""")

form = cgi.FieldStorage()
username = form.getfirst("username", "")

initialPass = form.getfirst("password", "")
initialPass = html.escape(initialPass)
hash_object = hashlib.md5(initialPass.encode())
password = hash_object.hexdigest()

action = form.getfirst("action", "wall")
title = form.getfirst("title", "")
content = form.getfirst("content", "")
user_id = form.getfirst("user_id", "-1")
post_id = form.getfirst("post_id", "-1")


username = html.escape(username)
action = html.escape(action)
title = html.escape(title)
content = html.escape(content)
user_id = html.escape(user_id)
post_id = html.escape(post_id)


if(username != ""):
	print("""<h1>User: {}</h1>""".format(username))
else:
	getUsernameQuery = "select username from users where user_id = '%d'" % int(user_id)
	cursor.execute(getUsernameQuery)

	row = cursor.fetchone()
	print("""<h1>User: {}</h1>""".format(row[0]))

print("""<form method="GET" action="../index.html">
			<input type="submit" name="new_post" value="Log Out">
		</form><br><br>""")

def printPosts(userID):
	getQuery = """select * from posts inner join users on users.user_id = posts.user_id
						 order by posts.creation_date desc"""
	try:
		cursor.execute(getQuery)
	except Exception:
		print("""Exception!""")
	else:
		
		print("""<form method="POST" action="/cgi-bin/post.py">
						<input type="hidden" name="user_id" value="{}">
						<input type="submit" name="new_post" value="Create new post">

			</form>""".format(userID))
		print("""<hr>""")

		rows = cursor.fetchall()
		for row in rows:
			print("""<p>Publisher: {} | published date: {}</p>""".format(row[8], row[3]))
			print("""<p>Title: {}</p>
					 <p>Content: {}</p>""".format(row[1], row[2]))
			
			if((row[6] == username and row[7] == password)  or (row[5] == int(user_id))):
				print("""<form method="POST" action="/cgi-bin/post.py">
							<input type="hidden" name="post_id" value="{}">
							<input type="hidden" name="user_id" value="{}">
							<input type="hidden" name="title" value="{}">
							<input type="hidden" name="content" value="{}">
							<input type="hidden" name="action" value="update">
							<input type="submit" name="edit" value="Edit">
				</form>""".format(row[0], row[5], row[1], row[2]))
				print("""<form method="POST" action="/cgi-bin/wall.py">
							<input type="hidden" name="post_id" value="{}">
							<input type="hidden" name="user_id" value="{}">
							<input type="hidden" name="title" value="{}">
							<input type="hidden" name="content" value="{}">
							<input type="hidden" name="action" value="delete">
							<input type="submit" name="delete" value="Delete">
				</form>""".format(row[0], row[5], row[1], row[2]))

			print("""<hr>""")

if (action == "create"):	

	insertQuery = "insert into posts(title, content, user_id) \
				values ('%s', '%s', '%d')" % (title, content, int(user_id))
	try:
		cursor.execute(insertQuery)
		connection.commit()

	except Exception:
		print("""Exception!""")
	else:
		printPosts(user_id)
elif (action == "update"):
	updateQuery = "update posts set title = '%s', content = '%s' where post_id = '%d'" % (title, content, int(post_id))

	try:
		cursor.execute(updateQuery)
		connection.commit()
	except Exception:
		print("""Exception!""")
	else:
		printPosts(user_id)
elif (action == "delete"):
	deleteQuery = "delete from posts where post_id = '%d'" % (int(post_id))
	try:
		cursor.execute(deleteQuery)
		connection.commit()
	except Exception:
		print("""Exception!""")
	else:
		printPosts(user_id)

else:
	checkUserQuery = "select * from users where username = '%s' and password = '%s'" % (username, password)
			

	# Execute the SQL command
	try:
		cursor.execute(checkUserQuery)

	except Exception:
		print("""Exception!""")
	# Fetch all the rows in a list of lists.
	else:
		row = cursor.fetchone()
		if(row is not None):
			printPosts(row[0])

		else:
			print("""<p>Incorrect Username or Password!</p>""")
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