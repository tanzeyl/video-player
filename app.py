from flask import Flask, render_template, request, redirect
import pymysql
from werkzeug.utils import secure_filename
import os

conn = pymysql.connect(host="db4free.net", user="tanzzeyl", passwd="#Because008", database="video_db")
cursor = conn.cursor()

uploadPath = "static/videos/"

def fetch(column):
  query = f"""SELECT DISTINCT `{ column }` FROM `videos`"""
  cursor.execute(query)
  allData = cursor.fetchall()
  data = []
  for point in allData:
    data.append(point[0])
  return data

def fetchData(videoId):
  query = f"""SELECT `location`, `comments` FROM `videos` WHERE `id` = { videoId }"""
  cursor.execute(query)
  data = cursor.fetchall()
  location = data[0][0]
  comments = data[0][1]
  comments = comments.split(",")
  return location, comments

app = Flask(__name__)
app.secret_key = "****"

@app.route("/", methods = ["GET", "POST"])
def home():
  locations = fetch("location")
  ids = fetch("id")
  return render_template("home.html", locations = locations, ids = ids, length = len(locations))

@app.route("/upload", methods = ["GET", "POST"])
def upload():
  tags = fetch("tag")
  return render_template("uploadVideo.html", tags = tags, length = len(tags))

@app.route("/uploadVideo", methods = ["GET", "POST"])
def getVideoData():
  query = """SELECT MAX(`id`) FROM `videos`"""
  cursor.execute(query)
  data = cursor.fetchall()
  videoNumber = data[0][0] + 1
  videoName = "/video" + str(videoNumber) + ".mp4"
  tag = request.form.get("tag")
  if (tag == None):
    tag = request.form.get("newTag").lower()
    os.mkdir(uploadPath + tag)
  location = uploadPath + tag + videoName
  file = request.files['video']
  file.save(location)
  query = f"""INSERT INTO `videos` (`id`, `name`, `location`, `tag`, `comments`) VALUES (NULL, '{videoName[1:-4]}', '{location}', '{tag}', '{""}')"""
  cursor.execute(query)
  conn.commit()
  return redirect("/")

@app.route("/singleVideo", methods = ["GET", "POST"])
def renderSingleVideo():
  videoId = request.form.get("id")
  location, comments = fetchData(videoId)
  return render_template("singleVideo.html", location = location, comments = comments, length = len(comments), videoId = videoId)

@app.route("/submitComment", methods = ["GET", "POST"])
def submitAComment():
  vid = request.form.get("vid")
  comment = request.form.get("comment")
  query = f"""SELECT `comments` FROM `videos` WHERE `id` = { vid }"""
  cursor.execute(query)
  data = cursor.fetchall()
  comments = data[0][0]
  comments = comments.split(", ")
  comments.append(comment)
  comment = ",".join(comments)
  query = f"""UPDATE `videos` SET `comments` = '{ comment }' WHERE `id` = { vid }"""
  cursor.execute(query)
  conn.commit()
  location, comments = fetchData(vid)
  return render_template("singleVideo.html", location = location, comments = comments, length = len(comments), videoId = vid)

@app.route("/videos", methods = ["GET", "POST"])
def allVideos():
  locations = fetch("location")
  ids = fetch("id")
  tags = fetch("tag")
  return render_template("allVideos.html", locations = locations, ids = ids, tags = tags, length = len(locations), tagL = len(tags))

@app.route("/selectedVideos", methods = ["GET", "POST"])
def getSelectedVideos():
  tag = request.form.get("tag")
  locations = []
  ids = []
  query = f"""SELECT `id`, `location` FROM `videos` WHERE `tag` = '{ tag }'"""
  cursor.execute(query)
  allData = cursor.fetchall()
  for data in allData:
    ids.append(data[0])
    locations.append(data[1])
  tags = fetch("tag")
  return render_template("allVideos.html", locations = locations, ids = ids, tags = tags, length = len(locations), tagL = len(tags))

@app.route("/about", methods = ["GET", "POST"])
def about():
  return render_template("uploadVideo.html")

if __name__ == "__main__":
    app.run(debug = True)
