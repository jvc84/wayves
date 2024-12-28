#!/usr/bin/python3

from assets.animations.waves_animations import waves_main, waves_start, waves_stop
from assets.animations.nothing_animations import nothing_empty, nothing_flat
from assets.animations.info_animations import info_sound, info_no_sound
from assets.animations.splash_animations import splash_animations_list
from assets.animations.cat_animations import cat_animations_list
from shared import show_help, check_player, check_music
from animation_rules import token
from pathlib import Path
from time import sleep
import subprocess
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
    def show_cava(category):
        cava_position = option_values['cava_values'][f'{category}_cava_sections']
        play_cava = current_directory + '/scripts/play_cava.sh'

        active_proc = str(
            subprocess.check_output(
                ["ps aux | grep \"cava -p\" | grep \"wayves\" | awk '{print $13}' | awk -F 'cava_option_config_' '{print $2}' "],
                shell=True
            )
        )[2:-3].split("\\n")


        ap_string = active_proc[0]
        active_proc = active_proc[1:-1]

        for i in active_proc:
            ap_string += f"|{i}"

        if len(ap_string) > 1:
            # ap_string = f"{token}|" + ap_string
            # ap_string = ap_string[:-1]
            insert = f" | grep -Evw '{ap_string}'  "

        else:
            insert = ""

        to_kill_proc = str(
            subprocess.check_output(
            [f"ps aux | grep -E 'play_cava' {insert}" + " | awk '{print $2}'"],
            shell=True
            )
        )[2:-3].split("\\n")


        for i in to_kill_proc:
            os.system(f"kill  {i} &> /dev/null")

        cache_files = str(subprocess.check_output(["ls ~/.cache/wayves/ | wc -l"], shell=True))[2:-3]

        if int(cache_files) > 3:
            os.system("rm  ~/.cache/wayves/*")

        try:
            proc = subprocess.Popen([f"setsid {play_cava} {cava_position} {category} {token} {shared.player}"], shell=True)
            proc.wait()
        except KeyboardInterrupt:
            proc.kill()
        except E:
            proc.kill()

        return

    @staticmethod
    def show_waves(category):
        waves_start.animation('full')

        if category == 'active':
            while check_music() is True and check_player() is True:
                waves_main.animation('full')

        elif category == 'inactive':
            while check_music() is False and check_player() is True:
                waves_main.animation('full')

        elif category == 'off':
            while check_music() is False:
                waves_main.animation('full')

        waves_stop.animation('full')

        return

    @staticmethod
    def show_info(category):
        if check_music() is True:
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
        if check_player() is False:
            current_category = 'off'

        elif check_music() is False:
            current_category = 'inactive'

        elif check_music() is True:
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
