import requests
import sqlite3
import os


# -----------------------------
# ADD YOUR API KEY HERE
# -----------------------------

import os

API_KEY = os.getenv("YOUTUBE_API_KEY")


# -----------------------------
# PATHS
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "youtube.db")


# -----------------------------
# GET VIDEO DETAILS FROM YOUTUBE
# -----------------------------

def get_video_details(video_id):

    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,statistics",
        "id": video_id,
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()


    if "items" not in data or len(data["items"]) == 0:
        print(f"Video not found: {video_id}")
        return None


    item = data["items"][0]


    return {
        "video_id": video_id,
        "title": item["snippet"]["title"],
        "channel": item["snippet"]["channelTitle"],
        "published": item["snippet"]["publishedAt"],
        "views": int(item["statistics"].get("viewCount", 0)),
        "likes": int(item["statistics"].get("likeCount", 0)),
        "comments": int(item["statistics"].get("commentCount", 0))
    }



# -----------------------------
# GET VIDEOS FROM DATABASE
# -----------------------------

def get_database_videos():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT video_id, video_name
        FROM videos
    """)


    videos = cursor.fetchall()


    conn.close()


    return videos



# -----------------------------
# SAVE VIEW HISTORY
# -----------------------------

def save_history(data, video_name):

    from datetime import datetime

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # Get previous views

    cursor.execute("""
        SELECT views
        FROM view_history
        WHERE video_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """,
    (data["video_id"],))


    previous = cursor.fetchone()


    if previous:
        view_gain = data["views"] - previous[0]
    else:
        view_gain = 0



    cursor.execute("""
        INSERT INTO view_history
        (
            video_id,
            video_name,
            timestamp,
            views,
            view_gain,
            likes,
            comments
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        data["video_id"],
        video_name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data["views"],
        view_gain,
        data["likes"],
        data["comments"]
    ))


    conn.commit()

    conn.close()


    print(f"View Gain: {view_gain}")



# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":


    videos = get_database_videos()


    print(f"\nFound {len(videos)} videos in database.\n")


    for video_id, video_name in videos:


        print(f"Checking: {video_name}")


        details = get_video_details(video_id)


        if details:

            print(details)


            save_history(details, video_name)


            print("✅ Saved to database")

            print("-----------------------")