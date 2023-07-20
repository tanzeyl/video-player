from flask import Flask, render_template, request, redirect
import pymysql
from werkzeug.utils import secure_filename
import os

conn = pymysql.connect(host="db4free.net", user="tanzzeyl", passwd="#Because008", database="video_db")
cursor = conn.cursor()

uploadPath = "static/videos/"

app = Flask(__name__)
app.secret_key = "****"

@app.route("/", methods = ["GET", "POST"])
def home():
  query = """SELECT `location` FROM `videos`"""
  cursor.execute(query)
  allVideoData = cursor.fetchall()
  locations = []
  for data in allVideoData:
    for location in data:
      locations.append(location)
  return render_template("home.html", locations = locations, length = len(locations))

@app.route("/upload", methods = ["GET", "POST"])
def upload():
  query = """SELECT DISTINCT `tag` FROM `videos`"""
  cursor.execute(query)
  allTags = cursor.fetchall()
  tags = []
  for data in allTags:
    for tag in data:
      tags.append(tag)
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

@app.route("/videos", methods = ["GET", "POST"])
def allVideos():
  return render_template("allVideos.html")

@app.route("/about", methods = ["GET", "POST"])
def about():
  return render_template("uploadVideo.html")

if __name__ == "__main__":
    app.run(debug = True)
