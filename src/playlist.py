import os
from googleapiclient.discovery import build
import isodate
import datetime


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.videos = []
        self.fetch_playlist_info()

    def fetch_playlist_info(self):
        api_key = os.getenv('YT_API_KEY', 'AIzaSyDZeYWTqGyYojWbDWHQf7d7Nconhf9T5uw')  # Если переменная окружения YT_API_KEY не установлена, используем значение по умолчанию
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Получение данных о плейлисте
        playlist_response = youtube.playlists().list(
            id=self.playlist_id,
            part='snippet'
        ).execute()

        if 'items' not in playlist_response or not playlist_response['items']:
            print(f"Плейлист с id {self.playlist_id} не найден.")
            return

        playlist_item = playlist_response['items'][0]

        if 'snippet' not in playlist_item:
            print("Информация о плейлисте не содержит ключ 'snippet'.")
            return

        self.title = playlist_item['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

        # Получение видео из плейлиста
        playlist_videos = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos.get('items', [])]

        # Получение данных о каждом видео
        video_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()

        for video in video_response.get('items', []):
            iso_8601_duration = video.get('contentDetails', {}).get('duration', 'PT0S')
            duration = isodate.parse_duration(iso_8601_duration)
            likes = int(video.get('statistics', {}).get('likeCount', 0))
            title = video.get('snippet', {}).get('title', '')
            video_id = video.get('id', '')

            # Добавляем данные о видео в список
            self.videos.append({'video_id': video_id, 'title': title, 'duration': duration, 'likes': likes})

    @property
    def total_duration(self):
        total_seconds = sum(video['duration'].total_seconds() for video in self.videos)
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        if not self.videos:
            return None

        best_video = max(self.videos, key=lambda video: video['likes'])
        return f"https://youtu.be/{best_video['video_id']}"

