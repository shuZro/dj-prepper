from pytube import Playlist
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

import shutil

import os
import threading
import time
import math

from bpm_detector import get_bpm
from key_finder import get_key

threads = list()

playlistLink = 'https://www.youtube.com/playlist?list=PLHsUZjFcs-UoYd0jSbUbkrRAhQOZe8m11'
playlist = Playlist(playlistLink)

def download_video(url, aca, ins, out_name = 'Downloaded/%(title)s.%(etx)s'):
    ydl_opts = {
        'outtmpl': out_name,
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL({'quiet': True}) as video:
        title = video.extract_info(url, download=False)['title'].replace('/', '')

        if (aca == True):
            acapella_search = VideosSearch(title + ' studio acapella', limit = 1)
            acapella_url = acapella_search.result()['result'][0]['id']

            print("Downloading Acapella ->", acapella_url)
            acapella_name = 'Downloaded/Acapella/' + title + ' - Acapella.wav'
            thread = threading.Thread(target=download_video, args=(acapella_url, False, False, acapella_name))
            threads.append(thread)
            thread.start()

        if (ins == True):
            instrumental_search = VideosSearch(title + ' official instrumental', limit = 1)
            instrumental_url = instrumental_search.result()['result'][0]['id']

            print("Downloading Instrumental ->", instrumental_url)
            instrumental_name = 'Downloaded/Instrumental/' + title + ' - Instrumental.wav'
            thread = threading.Thread(target=download_video, args=(instrumental_url, False, False, instrumental_name))
            threads.append(thread)
            thread.start()
        
    
    with YoutubeDL(ydl_opts) as video:
        video.download([url])

    print("Done ->", url) 

def download_playlist(playlist, aca = False, ins = False):
    threads = list()

    for url in playlist.video_urls:
        print("Downloading ->", url)
        thread = threading.Thread(target=download_video, args=(url, aca, ins,))
        threads.append(thread)
        thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

    time.sleep(1)

def prep_wav(file):
    root_path = os.curdir
    file_path = os.path.join(root_path, file)
    
    bpm = math.floor(get_bpm(file_path))
    key = get_key(file_path)
    
    file_no_ext = file.split('.wav')[0]

    if 'BPM' not in file_no_ext:
        new_name = "{key} - {bpm} BPM - {file}".format(key = key, bpm = bpm, file = file_no_ext)
        os.rename(file, new_name + '.wav')
        print(new_name)
    else:
        print(file_no_ext)

def prep_wavs():
    threads = list()
    
    root_path = os.curdir
    files = os.listdir(root_path)
    
    print("\nSongs: ")
    #for video in playlist.videos:
    #    print(video.title)

    for file in files:
        if file.endswith('.wav'):
            if 'aca' not in file.lower() and 'ins' not in file.lower():
                thread = threading.Thread(target=prep_wav, args=(file,))
                threads.append(thread)
                thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

            # shutil.move(file_path, os.path.join(destinationpath, file))
download_playlist(playlist, True, True)
prep_wavs()
