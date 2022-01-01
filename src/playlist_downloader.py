from pytube import Playlist
from youtube_dl import YoutubeDL

import shutil

import os
import threading
import time
import math

from bpm_detector import get_bpm 

playlistLink = "https://www.youtube.com/playlist?list=PLHsUZjFcs-UoYd0jSbUbkrRAhQOZe8m11"
playlist = Playlist(playlistLink)

# C:\Users\shup3\.cache\youtube-dl

def download_video(url):    
    ydl_opts = {
        'outtmpl': '%(title)s.%(etx)s',
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as video:
        video.download([url])

    print("Done ->", url) 

def start(playlist):
    threads = list()

    for url in playlist.video_urls:
        print("Downloading ->", url)
        thread = threading.Thread(target=download_video, args=(url,))
        threads.append(thread)
        thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

    time.sleep(1)

def print_songs(playlist):
    root_path = os.curdir
    files = os.listdir(root_path)

    destinationpath = ''
    
    print("\nSongs: ")
    #for video in playlist.videos:
    #    print(video.title)

    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root_path, file)
            bpm = math.floor(get_bpm(file_path))
            print(file, bpm)
            # shutil.move(file_path, os.path.join(destinationpath, file))

        
start(playlist)
print_songs(playlist)
