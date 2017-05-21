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
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
config = {
  'user': 'root',
  'password': 'scorpion',
  'host': 'localhost',
  'database': 'blog',
  'raise_on_warnings': True,
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

form = cgi.FieldStorage()


action = form.getfirst("action", "create")
title = form.getfirst("title", "")
content = form.getfirst("content", "")
user_id = form.getfirst("user_id", "")
post_id = form.getfirst("post_id", "-1")

action = html.escape(action)
title = html.escape(title)
content = html.escape(content)
user_id = html.escape(user_id)
post_id = html.escape(post_id)

cookie_user = cookie.get("cookie_user")
if cookie_user is not None:
  getUserID = "select * from users where session_id = '%d'" % (int(cookie_user.value))
  try:
    cursor.execute(getUserID)

  except Exception:
    print("""Exception!""")
  else:
    row = cursor.fetchone()
    user_id = row[0]
getUsernameQuery = "select username from users where user_id = '%d'" % int(user_id)
cursor.execute(getUsernameQuery)
row = cursor.fetchone()


print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="../styles.css">
            <title>Title</title>
        </head>
        <body>""")

print("""<h1>User: {}</h1>""".format(row[0]))

print("""<div class="post"><form method="POST" action="/cgi-bin/wall.py">
			<label for="title">Title</label><br>
			<input type="text" name="title" placeholder="Enter the title" value="{}" required><br>
			<label for="content">Content</label><br>
			<textarea name="content" rows="20" cols="40" placeholder="Enter the blog entry" required>{}</textarea><br>
			<input type="hidden" name="action" value="{}">
			<input type="hidden" name="user_id" value="{}">
			<input type="hidden" name="post_id" value="{}">
			<input class="button" type="submit" name="new_post" value="POST">

		</form></div>""".format(title, content, action, user_id, post_id))

cursor.close()
connection.close()