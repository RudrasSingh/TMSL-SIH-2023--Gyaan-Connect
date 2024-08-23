from pytube import *
from googleapiclient.discovery import build
class YTStats():
    def __init__(self,apiKey):
        #eself.channelId = channel_id
        self.apiKey = apiKey 
        self.channel_stats = None

    def get_channel_stats(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channelId}&key={self.apiKey}'
        return url    

    def get_video_stats(self,video_ids):
        url = f"https://www.googleapis.com/youtube/v3/videos?id={video_ids}&key={self.apiKey}&part=snippet,contentDetails,statistics,status"
        return url
    
    def youtube_search_topic(self,query, max_results):
        # Set up the YouTube Data API
        youtube = build('youtube', 'v3', developerKey=self.apiKey)

        # Call the search.list method to retrieve search results
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=max_results
        ).execute()
        vid = search_response["items"][0]["id"]["videoId"]
        # print(t.YTStats().get_video_stats(vid))



        # Extract video details from the search results
        videos = []
        # for search_result in search_response.get('items', []):
        #     video = {
        #         'title': search_result['snippet']['title'],
        #         'video_id': search_result['id']['videoId'],
        #         'url': f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
        #     }
        #     videos.append(video)

        print()
        return search_response
    

'''getting video ids of of urls'''


# URL_PLAYLIST = input("Enter Playlist Url")

# Retrieve URLs of videos from playlist
# playlist = Playlist(URL_PLAYLIST)
# print("Number Of Videos In playlist:",len(playlist.video_urls))

# urls = []
# for url in playlist:
#     urls.append(url)

# for i in urls:
    # vId = extract.video_id(i)
    # print(vId)
