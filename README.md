# mp3tube
mp3tube is a lightweight web application that downloads Youtube videos to MP3 files. Try it out [here](http://ytmp3tube.herokuapp.com)!

<img width="1440" alt="Screen Shot 2021-01-07 at 7 29 51 PM" src="https://user-images.githubusercontent.com/55343494/103959851-c6234100-511e-11eb-9751-9a4ec0961e3a.png">

## How to use:

##### Downloading a video:
Enter the URL of a Youtube video that is less than 30 minutes long (minimize load on server/client wait times). Then, simply click the button and wait for the download to commence!

<img width="1440" alt="Screen Shot 2021-01-07 at 7 33 43 PM" src="https://user-images.githubusercontent.com/55343494/103960018-48136a00-511f-11eb-895d-256dbc9a429c.png">

After the download is finished, the link field will clear and the downloaded mp3 will appear in your default Downloads directory!

## Technologies used:
mp3tube is a **Flask** application written in **Python**. It makes use of the **youtube-dl** Python module to download the Youtube videos as MP3 files. All webpages for this application were styled using **Bootstrap**. 

## Copyright and License:
Licensed under the [MIT License](https://github.com/rohatgiy/mp3tube/blob/master/LICENSE).
