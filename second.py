import os
import json
from googleapiclient.discovery import build

class Channel:
    instances = []
    api_key: str = os.getenv('YT_API_KEY')

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
        api_object = self.get_api_object()
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

class Video:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        self._video_id = video_id
        self._title = None
        self._view_count = None
        self._like_count = None
        self.initialize_attributes()

    def initialize_attributes(self):
        api_object = self.get_api_object()
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

    def get_api_object(self):
        return build('youtube', 'v3', developerKey=self.api_key)
    
class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self._playlist_id = playlist_id
        self._playlist_title = None
        self.initialize_playlist_attributes()

    def initialize_playlist_attributes(self):
        api_object = self.get_api_object()
        playlist_info = api_object.playlists().list(id=self.playlist_id, part='snippet').execute()['items'][0]
        self._playlist_title = playlist_info['snippet']['title']

    def __str__(self):
        return f'{self.title} ({self.playlist_title})'

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def playlist_title(self):
        return self._playlist_title