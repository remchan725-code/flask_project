import time
import datetime
import pygame

def set_alarm(alarm_time):
    print (f"Set alarm for {alarm_time}")
    sound_file = "C:/Users/remch/flask_project\Y2Mate.is - Metro Boomin - Space Cadet TikTok Remix Lyrics ft Gunna _ bought a spaceship now imma space cadet.mp3"
    is_running = True

    while is_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S").strip()
        print(current_time)

        if current_time == alarm_time:
            print("WAKE UP!")

            is_running = False 
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        
        time.sleep(1)
        
if __name__ == "__main__":
    alarm_time = input("Enter the alarm time (H:M:S): ")
    set_alarm(alarm_time)