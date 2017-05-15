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


getUsernameQuery = "select username from users where user_id = '%d'" % int(user_id)
cursor.execute(getUsernameQuery)
row = cursor.fetchone()
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