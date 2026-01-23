import os
import subprocess
import threading
import secrets

from asyncio import Event
from time import sleep
from pathlib import Path

from shared import check_sound_and_player_status


TOKEN = secrets.token_urlsafe(8)
ANIMATION_TOKEN = 'animation_' + TOKEN
CAVA_TOKEN = 'cava_' + TOKEN

PROJECT_DIRECTORY = str(Path(__file__).parent.resolve())
ANIMATION_SCRIPT = PROJECT_DIRECTORY + '/scripts/play_animation.sh'

animation_stop_event: Event | None = None
full_animation_stop_event: Event | None = None




def kill_token_processes():
    remaining_pids = str(
        subprocess.check_output([f"ps aux | grep {TOKEN} " + " | awk '{print $2}'"], shell=True)
    )[2:-3].split("\\n")

    for pid in remaining_pids:
        os.system(f"kill -9 {pid} 2&> /dev/null")


def stop_cava(category, pid, animation_stop_event):
    while True:
        sound, player = check_sound_and_player_status()
        if ((category == 'off' and player is True) or
                (category == 'inactive' and (sound is True or player is False)) or
                (category == 'active' and (sound is False or player is False)) or
                animation_stop_event.is_set()
        ):
            pid.kill()
            break
        sleep(1)


class Animation(object):
    def __init__(self, time, frames):
        self.time = time
        self.frames = frames[:-1]

    @staticmethod
    def check_cava(category, animation_stop_event, run_me):
        string_args = ""

        for i in run_me:
            string_args += f"'{i}' "

        try:
            pid = subprocess.Popen([string_args], shell=True)

            thread1 = threading.Thread(target=pid.wait, args=())
            thread2 = threading.Thread(target=stop_cava, args=(category, pid, animation_stop_event))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()

        except KeyboardInterrupt:
            raise KeyboardInterrupt()

        kill_token_processes()

        animation_stop_event.set()

    @staticmethod
    def check_player(category, animation_stop_event):
        while True:
            try:
                sound, player = check_sound_and_player_status()
                if ((category == 'off' and player is True) or
                    (category == 'inactive' and (sound is True or player is False)) or
                    (category == 'active' and (sound is False or player is False)) or
                    animation_stop_event.is_set()
                ):
                    break
                sleep(1)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()

        animation_stop_event.set()

    @staticmethod
    def animate_raw(time, frames):
        frames_list = frames.split(',')

        for frame in frames_list:
            os.system(f"echo '{frame}'")
            sleep(time)

    @staticmethod
    def animate_full(time, frames, animation_stop_event):
        frames_list = frames.split(',')
        while True:
            for frame in frames_list:
                os.system(f"echo '{frame}'")
                sleep(time)

                if full_animation_stop_event.is_set():
                    break

            if animation_stop_event.is_set():
                break

        animation_stop_event.set()

    @staticmethod
    def animate(time, frames, animation_stop_event):
        frames_list = frames.split(',')

        for frame in frames_list:
            if animation_stop_event.is_set():
                break
            os.system(f"echo '{frame}'")
            sleep(time)

        animation_stop_event.set()

    def animation_without_transition(self, category, *args):
        if category == 'raw':
            self.animate_raw(self.time, self.frames)

        else:
            global animation_stop_event
            animation_stop_event = threading.Event()
            animate_args = (self.time, self.frames, animation_stop_event)

            if 'full' in args:
                global full_animation_stop_event
                full_animation_stop_event = threading.Event()

                thread1 = threading.Thread(target=self.animate_full, args=animate_args)
            else:
                thread1 = threading.Thread(target=self.animate, args=animate_args)

            thread2 = threading.Thread(target=self.check_player, args=(category, animation_stop_event,))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()
