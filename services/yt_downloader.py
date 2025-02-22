"""
An attempt to download youtube videos through script.
In the process want to learn about DRM, streaming, ... used by YouTube

- Download public videos 
- Download private videos (i.e. vidoes accessible through membership)
"""
import requests
from bs4 import BeautifulSoup

class YoutubeDownloader():
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_video_info(self, video_id):
        pass
    
    def download_video(self, video_id, output_path=None):
        info = self.extract_video_info(video_id)