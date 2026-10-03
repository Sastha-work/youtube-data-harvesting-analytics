from googleapiclient.discovery import build
import pymongo


# -----------------------------
# YouTube API Connection
# -----------------------------

def api_connect():

    api_key = "AIzaSyCHXyttWAFgsWkTfq8rzJiX9txKIa-L_2Q"

    youtube = build(
        "youtube",
        "v3",
        developerKey=api_key
    )

    return youtube


youtube = api_connect()


# -----------------------------
# MongoDB Connection
# -----------------------------

client = pymongo.MongoClient(
    "mongodb://localhost:27017"
)

db = client["youtube_data"]


# -----------------------------
# Get Channel Information
# -----------------------------

def get_channel_info(channel_id):

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )

    response = request.execute()

    data = {}

    for i in response["items"]:

        data = {
            "channel_name": i["snippet"]["title"],
            "channel_id": i["id"],
            "subscribers": i["statistics"]["subscriberCount"],
            "views": i["statistics"]["viewCount"],
            "total_videos": i["statistics"]["videoCount"],
            "description": i["snippet"]["description"],
            "playlist_id":
                i["contentDetails"]["relatedPlaylists"]["uploads"],
            "channel_profile":i['snippet']['thumbnails']['high']['url']
        }

    return data


# -----------------------------
# Get Video IDs
# -----------------------------

def get_video_id(channel_id):

    video_ids = []

    response = youtube.channels().list(
        id=channel_id,
        part="contentDetails"
    ).execute()

    playlist_id = (
        response["items"][0]
        ["contentDetails"]
        ["relatedPlaylists"]
        ["uploads"]
    )

    next_page_token = None

    while True:

        response1 = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response1["items"]:

            video_ids.append(
                item["snippet"]["resourceId"]["videoId"]
            )

        next_page_token = response1.get("nextPageToken")

        if next_page_token is None:
            break

    return video_ids


# -----------------------------
# Get Video Information
# -----------------------------

def get_video_info(video_ids):

    video_data = []

    for video_id in video_ids:

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )

        response = request.execute()

        for i in response["items"]:

            data = {
                "channel_name":
                    i["snippet"]["channelTitle"],

                "channel_id":
                    i["snippet"]["channelId"],

                "video_id":
                    i["id"],

                "video_title":
                    i["snippet"]["title"],

                "published_at":
                    i["snippet"]["publishedAt"],

                "description":
                    i["snippet"].get("description"),

                "tags":
                    i["snippet"].get("tags"),

                "thumbnails":
                    i["snippet"]["thumbnails"]["default"]["url"],

                "duration":
                    i["contentDetails"]["duration"],

                "total_views":
                    i["statistics"].get("viewCount"),

                "total_likes":
                    i["statistics"].get("likeCount"),

                "total_comments":
                    i["statistics"].get("commentCount"),

                "favourite_count":
                    i["statistics"].get("favoriteCount"),

                "definition":
                    i["contentDetails"]["definition"],

                "caption":
                    i["contentDetails"]["caption"]
            }

            video_data.append(data)

    return video_data


# -----------------------------
# Get Comments
# -----------------------------

def get_comment_info(video_ids):

    comment_data = []

    try:

        for video_id in video_ids:

            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )

            response = request.execute()

            for i in response["items"]:

                data = {
                    "comment_id":
                        i["snippet"]["topLevelComment"]["id"],

                    "vid_id":
                        i["snippet"]["topLevelComment"]
                        ["snippet"]["videoId"],

                    "comment_text":
                        i["snippet"]["topLevelComment"]
                        ["snippet"]["textDisplay"],

                    "comment_author":
                        i["snippet"]["topLevelComment"]
                        ["snippet"]["authorDisplayName"],

                    "comment_published":
                        i["snippet"]["topLevelComment"]
                        ["snippet"]["publishedAt"]
                }

                comment_data.append(data)

    except Exception as e:

        print("Comment error:", e)

    return comment_data


# -----------------------------
# Get Playlist Information
# -----------------------------

def get_playlist_data(channel_id):

    playlist_data = []

    next_page_token = None

    while True:

        request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )

        response = request.execute()

        for i in response["items"]:

            data = {
                "playlist_id": i["id"],
                "title": i["snippet"]["title"],
                "channel_id": i["snippet"]["channelId"],
                "channel_name": i["snippet"]["channelTitle"],
                "published_at": i["snippet"]["publishedAt"],
                "video_count": i["contentDetails"]["itemCount"]
            }

            playlist_data.append(data)

        next_page_token = response.get("nextPageToken")

        if next_page_token is None:
            break

    return playlist_data


# -----------------------------
# Collect & Store Channel Data
# -----------------------------

def channel_details(channel_id):

    ch_details = get_channel_info(channel_id)

    plist_details = get_playlist_data(channel_id)

    video_ids = get_video_id(channel_id)

    vid_details = get_video_info(video_ids)

    comment_details = get_comment_info(video_ids)

    collection = db["channel_details"]

    collection.insert_one({
        "channel_information": ch_details,
        "playlist_information": plist_details,
        "video_information": vid_details,
        "comment_information": comment_details
    })

    return "success"
print("Testing YouTube API...")

try:
    test = youtube.channels().list(
        part="snippet",
        id="UCY6KjrDBN_tlRFT_QNqQbRQ"
    ).execute()

    print("YouTube API connection working!")
    print(test)

except Exception as e:
    print("YouTube API ERROR:")
    print(e)