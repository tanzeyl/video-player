import pymysql

conn = pymysql.connect(host="db4free.net", user="tanzzeyl", passwd="#Because008", database="video_db")
cursor = conn.cursor()

tag = "nature"
locations = []
ids = []
query = f"""SELECT `id`, `location` FROM `videos` WHERE `tag` = '{ tag }'"""
cursor.execute(query)
allData = cursor.fetchall()
for data in allData:
  ids.append(data[0])
  locations.append(data[1])
print(ids)
print(locations)
