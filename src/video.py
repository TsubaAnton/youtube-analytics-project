from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id, title=None, url=None, views=None, likes=None):
        self.video_id = video_id
        self.title = title
        self.url = url
        self.views = views
        self.likes = likes
        self.get_video_info()

    @staticmethod
    def get_api_key():
        return 'AIzaSyDZeYWTqGyYojWbDWHQf7d7Nconhf9T5uw'

    def get_video_info(self):
        api_key = self.get_api_key()

        youtube = build('youtube', 'v3', developerKey=api_key)

        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()

        self.title = video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.views = video_response['items'][0]['statistics']['viewCount']
        self.likes = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return str(self.title)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.get_video_info()

    def __str__(self):
        return str(self.title)
