from flask import Flask, render_template, request, send_from_directory
import os
import requests

app = Flask(__name__)

SONG_FOLDER = os.path.join("static", "songs")

# 🔑 Replace with your real API key
YOUTUBE_API_KEY = "AIzaSyBq_on5XnyoQWUDZgLu-kJSHwQfkXQ4Lss"


@app.route("/")
def index():
    try:
        songs = os.listdir(SONG_FOLDER)
        songs = [s for s in songs if s.endswith(".mp3")]
    except:
        songs = []

    return render_template("index.html", songs=songs, videos=None)


@app.route("/songs/<path:filename>")
def get_song(filename):
    return send_from_directory(SONG_FOLDER, filename)


# 🔥 UPDATED SEARCH ROUTE (BEST VERSION)
@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]

    # 🎯 Better YouTube targeting
    yt_query = query + " Jubin Garg Assamese song"

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={yt_query}&key={YOUTUBE_API_KEY}&maxResults=5&type=video"

    videos = []
    filtered_songs = []

    # 🎬 YouTube search
    try:
        response = requests.get(url).json()

        if "items" in response:
            for item in response["items"]:
                videos.append({
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
                })

    except Exception as e:
        print("YT ERROR:", e)

    # 🎵 Local song search (FILTERED)
    try:
        songs = os.listdir(SONG_FOLDER)
        songs = [s for s in songs if s.endswith(".mp3")]

        filtered_songs = [
            s for s in songs if query.lower() in s.lower()
        ]

    except Exception as e:
        print("LOCAL ERROR:", e)
        songs = []
        filtered_songs = []

    return render_template(
        "index.html",
        songs=filtered_songs if query else songs,
        videos=videos
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
