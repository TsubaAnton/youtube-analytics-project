import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.environ.get("API_KEY")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_channel_info(self):
        """Получает информацию о канале через API."""
        request = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=self.channel_id
        )
        response = request.execute()
        return response.get('items', [])[0] if response.get('items') else None

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_info = self.get_channel_info()

        if channel_info:
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            print(f"Title: {snippet['title']}")
            print(f"Description: {snippet['description']}")
            print(f"Published At: {snippet['publishedAt']}")
            print(f"View Count: {statistics['viewCount']}")
            print(f"Subscriber Count: {statistics['subscriberCount']}")
            print(f"Video Count: {statistics['videoCount']}")
        else:
            print("Unable to fetch channel information.")
