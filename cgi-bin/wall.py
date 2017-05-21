#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import mysql.connector
import hashlib
import os
import http.cookies
import sys
from random import randint
import cgitb
cgitb.enable(display=1, logdir="/log.txt")

config = {
  'user': 'root',
  'password': 'scorpion',
  'host': 'localhost',
  'database': 'blog_p',
  'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))

form = cgi.FieldStorage()
username = form.getfirst("username", "")

initialPass = form.getfirst("password", "")
initialPass = html.escape(initialPass)
hash_object = hashlib.md5(initialPass.encode())
password = hash_object.hexdigest()

firstname = form.getfirst("first_name", "")
lastname = form.getfirst("last_name", "")
email = form.getfirst("email", "")

action = form.getfirst("action", "login")
title = form.getfirst("title", "")
content = form.getfirst("content", "")
user_id = form.getfirst("user_id", "-1")
post_id = form.getfirst("post_id", "-1")
logout = form.getfirst("logout", "-1")



username = html.escape(username)
action = html.escape(action)
title = html.escape(title)
content = html.escape(content)
user_id = html.escape(user_id)
post_id = html.escape(post_id)
firstname = html.escape(firstname)
lastname = html.escape(lastname)
email = html.escape(email)
logout = html.escape(logout)

def printer():
	print("Content-type: text/html\n")



def printHeader():

	print("Content-type: text/html\n")

	print("""<!DOCTYPE HTML>
	<html>
	<head>
	<meta charset="utf-8">
	    <link rel="stylesheet" href="/styles.css">
	  <title>Blog</title>
	</head>
	<body>""")

def printLoginForm():
	print("""<div>
		        <form method="POST" action="/cgi-bin/wall.py">
		            Username <input type="text" name="username" required placeholder="your username">
		            Password <input type="password" name="password" required placeholder="your password">
		    		<input class="button" type="submit" value="Log in"></br></br>
		    	  </form>
		        <p>Create new Account</p>
		    </div>
		    <div>
		        <form method="POST" action="/cgi-bin/wall.py">
		        	<span class="field_name">Enter FirstName </span><span class="star">*</span><br>
		            <input type="text" name="first_name" required placeholder="your firstname"><br>
		            <span class="field_name">Enter LastName </span><span class="star">*</span><br>
		            <input type="text" name="last_name" required placeholder="your lastname"><br>
		            <span class="field_name">Enter Username </span><span class="star">*</span><br>
		            <input type="text" name="username" required placeholder="your username"><br>
		            <span class="field_name">Enter Password </span><span class="star">*</span><br>  
		            <input type="password" name="password" required placeholder="your password"><br>
		            <span class="field_name">Enter Email </span><br>  
		    		<input type="text" name="email" placeholder="your email"><br>
		            <input type="hidden" name="action" value="registration">
		    		<input class="button" type="submit" value="Registrate">
		        </form>
		    </div>""")
def printPosts(userID):

	printHeader()

	if(username != ""):

		print("""<h1>User: {}</h1>""".format(username))

	else:
		getUsernameQuery = "select username from users where user_id = '%d'" % int(user_id)
		cursor.execute(getUsernameQuery)

		row = cursor.fetchone()
		print("""<h1>User: {}</h1>""".format(row[0]))

	print("""<form method="GET" action="/cgi-bin/wall.py">
				<p class="logout"><input class="button" type="submit" name="logout" value="Log Out"></p>
				<input type="hidden" name="action" value="login">


			</form><br><br>""")
	getQuery = """select * from posts inner join users on users.user_id = posts.user_id
						 order by posts.creation_date desc"""
	try:
		cursor.execute(getQuery)
	except Exception:
		print("""Exception!""")
	else:
		print("""<form method="POST" action="/cgi-bin/post.py">
						<input type="hidden" name="user_id" value="{}">
						<p class="button-create"><input class="button" type="submit" name="new_post" value="Create new post"></p>

			</form>""".format(userID))
		print("""<hr>""")

		rows = cursor.fetchall()
		if (rows is not None):
			for row in rows:
				print("""<p class="published">Publisher: {} | published date: {}</p>""".format(row[8], row[3]))
				print("""<p>Title: {}</p>
						 <p>Content: {}</p>""".format(row[1], row[2]))
				
				if((row[6] == username and row[7] == password)  or (row[5] == int(user_id))):
					print("""<form method="POST" action="/cgi-bin/post.py">
								<input type="hidden" name="post_id" value="{}">
								<input type="hidden" name="user_id" value="{}">
								<input type="hidden" name="title" value="{}">
								<input type="hidden" name="content" value="{}">
								<input type="hidden" name="action" value="update">
								<input class="button-edit" type="submit" name="edit" value="Edit">
					</form>""".format(row[0], row[5], row[1], row[2]))
					print("""<form method="POST" action="/cgi-bin/wall.py">
								<input type="hidden" name="post_id" value="{}">
								<input type="hidden" name="user_id" value="{}">
								<input type="hidden" name="title" value="{}">
								<input type="hidden" name="content" value="{}">
								<input type="hidden" name="action" value="delete">
								<input class="button-delete" type="submit" name="delete" value="Delete">
					</form>""".format(row[0], row[5], row[1], row[2]))

				print("""<hr>""")

cookie_user = cookie.get("cookie_user")

is_any_cookie = False

if cookie_user is not None:

	if(logout == "Log Out"):
		updateSessionQuery = "update users set session_id = 0 WHERE session_id='%d'" % (int(cookie_user.value))
		try:
			cursor.execute(updateSessionQuery)
			connection.commit()
		except Exception:
			print("""Exception!""")
		# Fetch all the rows in a list of lists.
		else:
			is_any_cookie = False
			
			print ("Set-Cookie: cookie_user=deleted")


	elif (str(cookie_user.value).isdigit()):

		getUserID = "select * from users where session_id = '%d'" % (int(cookie_user.value))
		try:
			cursor.execute(getUserID)

		except Exception:
			print("""Exception!""")
		else:
			row = cursor.fetchone()
			user_id = row[0]
			is_any_cookie = True

				

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
elif(is_any_cookie):

	printPosts(user_id)
	print("""<p class="warning">User: \"{}\" Already Exists</p>""".format(logout))


elif (action == "registration"):
	

	# Execute the SQL command
	try:
		checkUserQuery = "select * from users where username = '%s' and password = '%s'" % (username, password)
		cursor.execute(checkUserQuery)
		
	except Exception:
		print("""Exception!""")
	# Fetch all the rows in a list of lists.
	else:
		row = cursor.fetchone()
		rand_id = randint(1, 10000000)

		if(row is not None):
			printHeader()
			print("""<p class="warning">User: \"{}\" Already Exists</p>""".format(username))
			printLoginForm()
		else:
			cookie_user = cookie.get("cookie_user")
			if cookie_user is None:
			    print("Set-cookie: cookie_user={}".format(rand_id))

			insertQuery = "insert into users(username, password, first_name, last_name, email, session_id) \
					values ('%s', '%s', '%s', '%s', '%s', '%d')" % (username, password, firstname, lastname, email, rand_id)
			try:
				cursor.execute(insertQuery)
				connection.commit()
			except Exception:
				print("""Exception!""")
			else:
				getUserID = "select * from users where username = '%s' and password = '%s'" % (username, password)
				try:
					cursor.execute(getUserID)

				except Exception:
					print("""Exception!""")
				else:
					row = cursor.fetchone()
					user_id = row[0]
				 #   print("Set-cookie: user_id_cookie=muha")
					printPosts(user_id)

			

elif (action == "login"):

	checkUserQuery = "select * from users where username = '%s' and password = '%s'" % (username, password)

	try:
		cursor.execute(checkUserQuery)

	except Exception:
		print("""Exception!""")
	# Fetch all the rows in a list of lists.
	else:
		row = cursor.fetchone()
		rand_id = randint(1, 10000000)

		if(row is not None):
			updateSessionQuery = "update users set session_id = '%d' WHERE user_id='%d'" % (rand_id, row[0])
			try:
				cursor.execute(updateSessionQuery)
				connection.commit()
			except Exception:
				print("""Exception!""")
			# Fetch all the rows in a list of lists.
			else:
				print("Set-cookie: cookie_user={}".format(rand_id))

			printPosts(row[0])

		else:
			

			printHeader()
			if(username != ""):
				print("""<p class="warning">Incorrect Username or Password!</p>""")
			printLoginForm()



cursor.close()
connection.close()