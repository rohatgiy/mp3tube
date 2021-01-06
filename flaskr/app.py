from flask import Flask, render_template, request, redirect, url_for
import youtube_dl
import os

app = Flask(__name__)

MAX_LENGTH = 30 * 60

if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ] 

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")

path = get_download_folder()+"/%(title)s.%(ext)s"

ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': path,
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
            if  duration > MAX_LENGTH:
                return render_template('error.html', error="Video duration exceeds 30 minutes.")
            ytdl.download([link]) 
            return render_template('video.html', title=info["title"], link=link)
        except youtube_dl.utils.DownloadError as e:
            error=str(e).lstrip('[0;31mERROR:[0m')
            if error.find('is not a valid URL.') != -1:
                error='Invalid URL.'
            return render_template('error.html', error=error)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))