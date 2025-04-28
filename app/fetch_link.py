import urllib.request
import re

html = urllib.request.urlopen("https://www.youtube.com/results?search_query=mozart")
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
video_ids = list(set(video_ids))  # Remove duplicates
video_ids = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]
print("total videos found:", len(video_ids))
for video_id in video_ids:
    print(video_id)