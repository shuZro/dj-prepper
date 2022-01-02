from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

import threading
import time

threads = list()

def download_video(url, aca, ins, out_name = 'Downloaded/%(title)s.%(etx)s'):
    with YoutubeDL({'quiet': True}) as video:
        title = video.extract_info(url, download=False)['title'] \
        .replace('/', '') \
        .replace('[', '').replace(']', '')\
        .replace('Video', '') \
        .replace('Official', '') \
        .replace(' MV', '') \
        .strip()

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

        if out_name == '':
            out_name = 'Downloaded/' + title + '.wav'

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
    
        with YoutubeDL(ydl_opts) as video:
            video.download([url])

    print("Done ->", url) 

def download_playlist(playlist, aca = False, ins = False):
    for url in playlist.video_urls:
        print("Downloading ->", url)
        thread = threading.Thread(target=download_video, args=(url, aca, ins,))
        threads.append(thread)
        thread.start()

    for index, thread in enumerate(threads): # close threads
        thread.join()

    time.sleep(2)

