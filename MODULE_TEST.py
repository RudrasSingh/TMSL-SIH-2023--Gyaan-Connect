from youtube import YTStats
from pytube import *
import requests
import json


API_KEY = 'AIzaSyAMtysCv1YSFqck6UOtdpZWYuZ1qzGGNWY'

#channel_id = 'UCbXgNpp0jedKWcQiULLbDTA'


def get_video_ids(URL_PLAYLIST):

    playlist = Playlist(URL_PLAYLIST) 

    urls = []
    vid_ids = []
    for url in playlist:
        urls.append(url)

    for i in urls:
        vId = extract.video_id(i)
        vid_ids.append(vId)
    
    return (vid_ids,urls)

yt = YTStats(API_KEY)

#print((get_video_ids("https://youtube.com/playlist?list=PLU6SqdYcYsfJV8Lfq4KFA0U8kGeJ2NGWV&si=zq8VtON19aU-aL6g"))[1])



def post_video_stats(playlist_url):
    video_stats_list = []
    count = 0
    for x in (get_video_ids(playlist_url)[0]):

        json_url = requests.get(yt.get_video_stats(x))

        data = json.loads(json_url.text)
 
    
    
        #------------------------collecting all datas of youtube playlist videos------------------------
        

        video_url =  get_video_ids(playlist_url)[1][count]

        video_id = data["items"][0]["id"]  #id of the video

        title_of_video = data["items"][0]["snippet"]["title"]

        tags_of_video = (data["items"][0]["snippet"]["tags"])

        channel_title = data["items"][0]["snippet"]["channelTitle"]

        video_thumbnail = data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        
        duration_of_video = int(data["items"][0]["contentDetails"]["duration"][2:].split('M')[0])

        video_views = data["items"][0]["statistics"]["viewCount"]

        video_likes = data["items"][0]["statistics"]["likeCount"]

        video_comments_count = data["items"][0]["statistics"]["commentCount"]

        count+=1

        video_stats_list.append([playlist_url,video_url,video_id,title_of_video,tags_of_video,channel_title,video_thumbnail,duration_of_video,video_views,video_likes,video_comments_count])
    
    return video_stats_list
    
    
ids = get_video_ids("https://youtube.com/playlist?list=PLU6SqdYcYsfJV8Lfq4KFA0U8kGeJ2NGWV&si=zq8VtON19aU-aL6g")
json_url = requests.get(yt.get_video_stats(ids[0][0]))
data = json.loads(json_url.text)
print(json.dumps(data, indent=4))





# print(video_views,video_likes,video_comments_count)
        
# url = get_video_ids("https://youtube.com/playlist?list=PLU6SqdYcYsfJV8Lfq4KFA0U8kGeJ2NGWV&si=zq8VtON19aU-aL6g")[0]
# post_video_stats("https://youtube.com/playlist?list=PLU6SqdYcYsfJV8Lfq4KFA0U8kGeJ2NGWV&si=zq8VtON19aU-aL6g")

