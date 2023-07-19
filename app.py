from flask import Flask, render_template, send_file, request, session
import pymysql

conn = pymysql.connect(host="db4free.net", user="tanzzeyl", passwd="#Because008", database="video_db")
cursor = conn.cursor()

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
    return render_template("uploadVideo.html")

if __name__ == "__main__":
    app.run(debug = True)
