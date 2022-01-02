from pytube import Playlist
from youtube_dl import YoutubeDL

import shutil

import os
import threading
import time
import math

from bpm_detector import get_bpm
from key_finder import get_key

playlistLink = 'https://www.youtube.com/playlist?list=PLHsUZjFcs-UoYd0jSbUbkrRAhQOZe8m11'
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

def download_playlist(playlist):
    threads = list()

    for url in playlist.video_urls:
        print("Downloading ->", url)
        thread = threading.Thread(target=download_video, args=(url,))
        threads.append(thread)
        thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

    time.sleep(1)

def rename_wav(file, bpm, key):
    file_no_ext = file.split('.wav')[0]
    if 'BPM' not in file_no_ext:
        new_name = "{key} - {bpm} BPM - {file}".format(key = key, bpm = bpm, file = file_no_ext)
        os.rename(file, new_name + '.wav')
        print(new_name)
    else:
        print(file_no_ext)

def print_wavs():
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
            key = get_key(file_path)
            rename_wav(file, bpm, key)
            # shutil.move(file_path, os.path.join(destinationpath, file))

     
download_playlist(playlist)
print_wavs()
