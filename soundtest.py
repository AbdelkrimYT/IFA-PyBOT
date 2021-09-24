import vlc
import time


playsound = vlc.MediaPlayer('.//bin//audio.mp3')
playsound.play()
time.sleep(1.5)
duration = playsound.get_length() / 1000
time.sleep(duration)
