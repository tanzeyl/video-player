import pymysql

conn = pymysql.connect(host="db4free.net", user="tanzzeyl", passwd="#Because008", database="video_db")
cursor = conn.cursor()

videoId = 1
query = f"""SELECT `location`, `comments` FROM `videos` WHERE `id` = { videoId }"""
cursor.execute(query)
data = cursor.fetchall()
location = data[0][0]
comments = data[0][1]
comments = comments.split(",")
print(location)
print(comments)
