import pymysql

conn = pymysql.connect(host="db4free.net", user="tanzzeyl", passwd="#Because008", database="video_db")
cursor = conn.cursor()

query = """SELECT MAX(`id`) FROM `videos`"""
cursor.execute(query)
data = cursor.fetchall()
videoNumber = data[0][0]
print("/video" + str(videoNumber) + ".mp4")
