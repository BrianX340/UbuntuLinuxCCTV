# UbuntuLinuxCCTV
This Python application uses PyQt5 to create a graphical interface for viewing multiple real-time RTSP video streams.

Key Features
Secure Login: Allows users to input credentials and define the number of streaming channels.
Remember Settings: Uses QSettings to save credentials and the number of channels if the user chooses to remember them.
Multi-stream Display: Dynamically generates URLs for each channel and displays streams in organized layouts, supporting up to four channels simultaneously.
Multimedia Support: Uses QMediaPlayer and QVideoWidget for real-time video playback.
Resource Management: Releases media players upon closing the application, optimizing memory usage.

This application is ideal for viewing IP camera feeds in a local network environment.



## Important
You need to change the local address to that of your dvr.
