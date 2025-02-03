#!/usr/bin/python3

from assets.animations.waves_animations import waves_main, waves_start, waves_stop
from assets.animations.nothing_animations import nothing_empty, nothing_flat
from assets.animations.info_animations import info_sound, info_no_sound
from assets.animations.splash_animations import splash_animations_list
from assets.animations.cat_animations import cat_animations_list
from shared import show_help, check_sound_and_player_status
from animation_rules import token
from pathlib import Path
import subprocess
from time import sleep
import shared
import random
import sys
import os


current_directory = str(Path(__file__).parent.resolve())
splash_animation_index = 0

options = ["cat", "waves", "cava", "info", "splash", "empty", "flat"]
options_with_values = [
    "cava",
    "flat",
    "empty"
]
option_values = {
    'empty_values': {
        'off_empty_sections': 0,
        'inactive_empty_sections': 0,
        'active_empty_sections': 0,

    },

    'flat_values': {
        'off_flat_sections': 16,
        'inactive_flat_sections': 16,
        'active_flat_sections': 16,
    },

    'cava_values': {
        'off_cava_sections': 'all',
        'inactive_cava_sections': 'all',
        'active_cava_sections': 'all',
    }
}
animation_flags = {
    'active_flags': ["--active", "-a"],
    'inactive_flags': ["--inactive", "-i"],
    'off_flags': ["--off", "-o"],

}
flag_values = {
    'active': 'cava',
    'inactive': 'flat',
    'off': 'cat',
}



def kill_cava(category, pid, stop_event):
    while True:
        sound, player = check_sound_and_player_status()
        if ((category == 'off' and player is True) or
                (category == 'inactive' and (sound is True or player is False)) or
                (category == 'active' and (sound is False or player is False)) or
                stop_event.is_set()
        ):
            pid.kill()
            break
        sleep(1)


class Show(object):
    @staticmethod
    def show_empty(category):
        empty_output = ' ' * option_values['empty_values'][f'{category}_empty_sections']
        empty_frames = (empty_output + ',') * 10
        nothing_empty.animation(category, 1, empty_frames)

        return

    @staticmethod
    def show_flat(category):
        flat_output = '▁' * option_values['flat_values'][f'{category}_flat_sections']
        flat_frames = (flat_output + ',') * 10

        nothing_flat.animation(category, 1, flat_frames)

        return

    @staticmethod
    def show_waves(category):
        waves_start.animation('raw')
        waves_main.animation_without_transition(category, 'full')
        waves_stop.animation('raw')

        return

    @staticmethod
    def show_info(category):
        sound, player = check_sound_and_player_status()
        if sound is True:
            info_sound.animation(category)
        else:
            info_no_sound.animation(category)

        return

    @staticmethod
    def show_splash(category):
        global splash_animation_index

        if splash_animation_index > len(splash_animations_list) - 1:
            splash_animation_index = 0
            os.system(f"echo 'wrong inactive value: {splash_animation_index} !!!'")
            sleep(15)

        for index, inactive in enumerate(splash_animations_list, 0):

            if index >= len(splash_animations_list) - 1:
                inactive.animation(category)
                splash_animation_index = 0
                break

            elif index == splash_animation_index:
                inactive.animation(category)
                splash_animation_index = index + 1
                break

        return

    @staticmethod
    def show_cat(category):
        index = random.randint(0, len(cat_animations_list) - 1)
        cat_animations_list[index].animation(category)

        return

    @staticmethod
    def show_cava(category):
        cache_dir = " ~/.cache/wayves"
        cache_files = str(subprocess.check_output([f"ls {cache_dir}| wc -l 2>/dev/null"], shell=True))[2:-3]
        if int(cache_files) > 3:
            os.system(f"rm  {cache_dir}/*")

        import  threading
        stop_event = threading.Event()

        cava_position = option_values['cava_values'][f'{category}_cava_sections']
        play_cava = current_directory + '/scripts/play_cava.sh'

        run_me = [play_cava, cava_position, token]

        string_args = ""

        for i in run_me:
            string_args += f"'{i}' "

        try:
            proc = subprocess.Popen([string_args], shell=True)
            thread1 = threading.Thread(target=proc.wait, args=())
            thread2 = threading.Thread(target=kill_cava, args=(category, proc, stop_event))

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()

        except KeyboardInterrupt:
            print("Exit!")
            os.system(f"pkill -f {token}")
            stop_event.set()
        except Exception as e:
            print("Cannot run CAVA")
            sys.exit(1)

        remaining_pids = str(
            subprocess.check_output([f"ps aux | grep {token} " + " | awk '{print $2}'"], shell=True)
        )[2:-3].split("\\n")

        for pid in remaining_pids:
            os.system(f"kill -9 {pid}")

        stop_event.set()

        return


def detect_category(detect_fl):
    category = ""
    for category_flags in animation_flags:
        if detect_fl in animation_flags[category_flags]:
            category = animation_flags[category_flags][0][2:]
            break

    return category


def parse_flag(parse_fl, opt):
    category = detect_category(parse_fl)
    flag_values[category] = opt


def parse_option_with_value(arg_fl, opt):
    try:
        opt_value = int(opt.split('=')[-1])
    except ValueError:
        opt_value = opt.split('=')[-1]

    opt_name = opt.split('=')[0]
    parse_flag(arg_fl, opt_name)

    opt_name_values = opt_name + '_values'
    category = detect_category(arg_fl)

    option_values[f'{opt_name_values}'][f'{category}_{opt_name}_sections'] = opt_value


def single_animation():
    while True:
        option = 'show_' + flag_values['off']

        show_animation = getattr(Show, option)
        if flag_values['off'] == "cava":
            shared.player = "cava"
            current_category = "off"
        elif flag_values['off'] == "waves":
            current_category = "off"
        else:
            current_category = 'full'
         
        show_animation(current_category)


def multiple_animations():
    current_category = 'off'

    if shared.player == "":
        print("No player specified!")
        show_help()
    while True:
        sound, player = check_sound_and_player_status()
        if player is False:
            current_category = 'off'

        elif sound is False:
            current_category = 'inactive'

        elif sound is True:
            current_category = 'active'

        option = 'show_' + flag_values[current_category]

        show_animation = getattr(Show, option)
        show_animation(current_category)


def parse_arguments():
    received_flags = sys.argv

    for i, fl in enumerate(received_flags, 0):

        if i == 0 or fl in options:
            continue

        if "=" in fl:
            parse_option_with_value(received_flags[i - 1], fl)
        else:
            match fl:
                case "-h" | "--help":
                    show_help()
                case "-p" | "--player":
                    shared.player = received_flags[i + 1]
                case _:
                    if (received_flags[i - 1] != "-p" and
                            received_flags[i - 1] != "--player"):
                        try:
                            parse_flag(fl, received_flags[i + 1])
                        except IndexError:
                            print("\nIncorrect flag was used!")
                            show_help()
                
                
def main():
    parse_arguments()

    if flag_values['off'] == flag_values['inactive'] == flag_values['active']:
        single_animation()
    else:
        multiple_animations()


if __name__ == "__main__":
    main()
