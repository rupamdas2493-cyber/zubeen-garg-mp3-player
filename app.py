from flask import Flask, render_template, request
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# 🔐 Use environment variable (IMPORTANT for production)
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

videos_cache = []  # store results temporarily


@app.route("/")
def home():
    return render_template("index.html", videos=[], selected_video=None)


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")

    global videos_cache
    videos_cache = []

    try:
        request_api = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=8
        )
        response = request_api.execute()

        for item in response.get("items", []):
            videos_cache.append({
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            })

    except Exception as e:
        print("YouTube API Error:", e)

    return render_template("index.html", videos=videos_cache, selected_video=None)


@app.route("/play/<video_id>")
def play(video_id):
    return render_template("index.html", videos=videos_cache, selected_video=video_id)


if __name__ == "__main__":
    app.run()
