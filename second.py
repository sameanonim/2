import os
import json
import datetime
import isodate
from googleapiclient.discovery import build

class YoutubeAPI:
    api_key: str = os.getenv('YT_API_KEY')

    @staticmethod
    def get_api_object():
        return build('youtube', 'v3', developerKey=YoutubeAPI.api_key)

class Channel(YoutubeAPI):
    instances = []

    def __init__(self, channel_id):
        self._channel_id = channel_id
        self._title = None
        self._description = None
        self._url = None
        self._subscriber_count = None
        self._video_count = None
        self._view_count = None
        self.instances.append(self)
        self.initialize_attributes()

    def initialize_attributes(self):
        api_object = YoutubeAPI.get_api_object()
        channel_info = api_object.channels().list(id=self.channel_id, part='snippet,statistics').execute()['items'][0]
        self._title = channel_info['snippet']['title']
        self._description = channel_info['snippet']['description']
        self._url = f"https://www.youtube.com/channel/{self.channel_id}"
        self._subscriber_count = int(channel_info['statistics']['subscriberCount'])
        self._video_count = int(channel_info['statistics']['videoCount'])
        self._view_count = int(channel_info['statistics']['viewCount'])

    def __str__(self):
        return f'Youtube-канал: {self.title}'
    
    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __add__(self, other):
        return f'{self.subscriber_count + other.subscriber_count}'

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def subscriber_count(self):
        return self._subscriber_count

    @property
    def video_count(self):
        return self._video_count

    @property
    def view_count(self):
        return self._view_count

    def get_api_object(self):
        return build('youtube', 'v3', developerKey=self.api_key)

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name):
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file_name, "w") as f:
            json.dump(data, f)

class Video(YoutubeAPI):
    def __init__(self, video_id):
        self._video_id = video_id
        self._title = None
        self._view_count = None
        self._like_count = None
        self.initialize_attributes()

    def initialize_attributes(self):
        api_object = YoutubeAPI.get_api_object()
        video_info = api_object.videos().list(id=self.video_id, part='snippet,statistics').execute()['items'][0]
        self._title = video_info['snippet']['title']
        self._view_count = int(video_info['statistics']['viewCount'])
        self._like_count = int(video_info['statistics']['likeCount'])

    def __str__(self):
        return f'{self.title}'

    @property
    def video_id(self):
        return self._video_id

    @property
    def title(self):
        return self._title

    @property
    def view_count(self):
        return self._view_count

    @property
    def like_count(self):
        return self._like_count
    
class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self._playlist_id = playlist_id
        self._playlist_title = None
        self._playlist_duration = None
        self.initialize_playlist_attributes()

    def initialize_playlist_attributes(self):
        api_object = YoutubeAPI.get_api_object()
        playlist_info = api_object.playlists().list(id=self._playlist_id, part='snippet').execute()['items'][0]
        self._playlist_title = playlist_info['snippet']['title']
        self._playlist_duration = isodate.parse_duration(api_object.videos().list(id=self.video_id, part='contentDetails').execute()['items'][0]['contentDetails']['duration'])

    def __str__(self):
        return f'{self.title} ({self.playlist_title})'
    
    @property
    def duration(self):
        return self._playlist_duration

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def playlist_title(self):
        return self._playlist_title
    
class PlayList(YoutubeAPI):

    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self._playlist_title = None
        self._playlist_link = None
        self._videos = []
        self.initialize_playlist_attributes()

    def initialize_playlist_attributes(self):
        api_object = YoutubeAPI.get_api_object()
        playlist_info = api_object.playlists().list(id=self._playlist_id, part='snippet').execute()['items'][0]
        self._playlist_title = playlist_info['snippet']['title']
        self._playlist_link = f'https://www.youtube.com/playlist?list={self._playlist_id}'
        self.get_videos()

    def get_videos(self):
        api_object = self.get_api_object()
        next_page_token = ''
        while next_page_token is not None:
            video_list = api_object.playlistItems().list(playlistId=self._playlist_id, part='contentDetails', maxResults=50, pageToken=next_page_token).execute()
            for item in video_list['items']:
                video_id = item['contentDetails']['videoId']
                self._videos.append(PLVideo(video_id, self._playlist_id))
            next_page_token = video_list.get('nextPageToken')

    @property
    def title(self):
        return f'{self._playlist_title}'

    @property
    def url(self):
        return self._playlist_link

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self._videos:
            total_duration += video.duration
        return total_duration

    def most_popular_video_link(self):
        most_popular_video = max(self._videos, key=lambda video: video.like_count)
        return f'https://youtu.be/{most_popular_video._video_id}'
    
    def show_best_video(self):
        best_video_link = self.most_popular_video_link()
        return best_video_link