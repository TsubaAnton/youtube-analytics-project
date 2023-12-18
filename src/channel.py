import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.environ.get("API_KEY")
        self.youtube = Channel.get_service()

        self.title = None
        self.description = None
        self.channel_url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None

        self.get_channel_info()

    @property
    def url(self):
        return self.channel_url

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=os.environ.get("API_KEY"))

    def get_channel_info(self):
        """Получает информацию о канале через API."""
        request = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=self.channel_id
        )
        response = request.execute()
        channel_info = response.get('items', [])[0] if response.get('items') else None

        if channel_info:
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            self.title = snippet['title']
            self.description = snippet['description']
            self.channel_url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscriber_count = statistics['subscriberCount']
            self.video_count = statistics['videoCount']
            self.view_count = statistics['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"Название: {self.title}")
        print(f"Описание: {self.description}")
        print(f"Ссылка на канал: {self.channel_url}")
        print(f"Количество подписчиков: {self.subscriber_count}")
        print(f"Количество видео: {self.video_count}")
        print(f"Количество просмотров: {self.view_count}")

    def to_json(self, filename: str = "channel_info.json") -> None:
        """Сохраняет в файл значения атрибутов экземпляра Channel в формате JSON."""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "channel_url": self.channel_url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)


