import os
import json
from googleapiclient.discovery import build

class Channel:
    instances = []
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

        # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.__class__.instances.append(self)

    # вывод данных по id каналу
    def print_info(self):
        print(f'{self.channel_id}')
        print(json.dumps(self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2, ensure_ascii=False))