from flask import Flask, render_template, request, redirect, url_for, send_file
import youtube_dl
import os

app = Flask(__name__)
MAX_LENGTH = 30 * 60

def get_download_folder():
    home = os.path.expanduser("~")
    return os.path.join(home, "tmp")

path = get_download_folder()

ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': path+"/%(title)s.%(ext)s",
    'noplaylist': True,
    'playliststart': 1,
    'playlistend': 1
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'GET':
        return redirect(url_for('index'))
    link = request.form['link']
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        try:
            info = ytdl.extract_info(link, download=False)
            if "_type" in info and info["_type"] == 'playlist':
                return render_template('error.html', error="Cannot download playlist.")
            else:
                duration = info["duration"]
                title = str(info["title"]+'.mp3')
            if  duration > MAX_LENGTH:
                return render_template('error.html', error="Video duration exceeds 30 minutes.")
            ytdl.download([link])
            filename=str(path+'/'+title) 
            return send_file(filename, as_attachment=True, mimetype='audio/mpeg')
        except youtube_dl.utils.DownloadError as e:
            error=str(e).lstrip('[0;31mERROR:[0m')
            if error.find('is not a valid URL.') != -1:
                error='Invalid URL.'
            return render_template('error.html', error=error)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))