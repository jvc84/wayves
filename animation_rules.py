from time import sleep
from pathlib import Path
import secrets

import os
import subprocess
import threading
from shared import check_sound_and_player_status
token = secrets.token_urlsafe(8)
animation_token = 'animation_' + token
cava_token = 'cava_' + token

current_directory = str(Path(__file__).parent.resolve())
play_animation = current_directory + '/scripts/play_animation.sh'


# @staticmethod
def kill_cava(category, pid, stop_event):
    while True:
        print("Wait")
        sound, player = check_sound_and_player_status()
        if ((category == 'off' and player is True) or
                (category == 'inactive' and (sound is True or player is False)) or
                (category == 'active' and (sound is False or player is False)) or
                stop_event.is_set()
        ):
            # os.system(f'pkill -f {token}')
            pid.kill()
            print("Kill")
            break
        sleep(1)

class Animation(object):
    def __init__(self, time, frames):
        self.time = time
        self.frames = frames[:-1]



    @staticmethod
    def check_cava(category, stop_event, run_me):
        string_args = ""

        for i in run_me:
            string_args += f"'{i}' "


        try:
            pid = subprocess.Popen([string_args], shell=True)
            print("trying ")
            thread1 = threading.Thread(target=pid.wait, args=())
            thread2 = threading.Thread(target=kill_cava, args=(category, pid, stop_event))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()

        except KeyboardInterrupt:
            print("Error")
            pid.kill()

        remaining_pids = str(
            subprocess.check_output([f"ps aux | grep {token} " + " | awk '{print $2}'"], shell=True))[
                         2:-3].split("\\n")

        for pid in remaining_pids:
            os.system(f"kill -9 {pid}")


        stop_event.set()

    @staticmethod
    def check_player(category, stop_event):
        while True:
            sound, player = check_sound_and_player_status()
            if ((category == 'off' and player is True) or
                (category == 'inactive' and (sound is True or player is False)) or
                (category == 'active' and (sound is False or player is False)) or
                stop_event.is_set()
            ):
                break
            sleep(1)

        stop_event.set()

    @staticmethod
    def animate_raw(time, frames):
        frames_list = frames.split(',')

        for frame in frames_list:
            os.system(f"echo '{frame}'")
            sleep(time)

    @staticmethod
    def animate_full(time, frames, stop_event):
        frames_list = frames.split(',')
        while True:
            for frame in frames_list:
                os.system(f"echo '{frame}'")
                sleep(time)

            if stop_event.is_set():
                break

        stop_event.set()

    @staticmethod
    def animate(time, frames, stop_event):
        frames_list = frames.split(',')

        for frame in frames_list:
            if stop_event.is_set():
                break
            os.system(f"echo '{frame}'")
            sleep(time)


        stop_event.set()


    def animation_without_transition(self, category, *args):
        if category == 'raw':
            self.animate_raw(self.time, self.frames)

        else:
            stop_event = threading.Event()

            if 'full' in args:
                thread1 = threading.Thread(target=self.animate_full, args=(self.time, self.frames, stop_event))
            else:
                thread1 = threading.Thread(target=self.animate, args=(self.time, self.frames, stop_event))

            thread2 = threading.Thread(target=self.check_player, args=(category, stop_event,))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()
