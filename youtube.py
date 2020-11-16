from __future__ import unicode_literals
import os.path
import youtube_dl

HOMEDIR = os.path.expanduser('~')

ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': HOMEDIR + '/Music/Music/Media.localized/Automatically Add to Music.localized/%(title)s.%(ext)s',
    'ignoreerrors': True
}

def main():
    url = input('input a youtube/youtube playlist url: ')
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([url])

if __name__ == '__main__':
    main()