import subprocess
from sys import exit
import threading


player_name = "any"
status_any = b'Paused\n'


def try_to_check_output(command):
    try:
        out = subprocess.check_output([command], shell=True)
    except Exception as e:
        out =  b''

    return out

def check_sound_and_player_status() -> (bool, bool):
    global player_name

    if player_name == "cava":
        return True

    try:
        status = get_status()

        if status == b'Playing\n':
            output_sound = True
        else:
            output_sound = False

        if b'P' in status:
            output_player = True
        else:
            output_player = False

    except subprocess.CalledProcessError:
        output_sound = False
        output_player = False

    return output_sound, output_player


def check_playerctl(player_name):
    try:
        output = subprocess.check_output([f'playerctl status --player="{player_name}"'], shell=True)
        if b"Playing" in output:
            return 1
        else:
            return 0
    except subprocess.CalledProcessError as e:
        return 0

def check_player_status(player_name, stop_event):
    result = check_playerctl(player_name)
    if result == 1 and not stop_event.is_set():
        global status_any
        status_any = b'Playing\n'
        stop_event.set()
    return 0


def get_status():
    global player

    if player == "any":
        command = 'playerctl -l'
    else:
        command = f'playerctl status --player="{player}"'

    output = try_to_check_output(command)

    if player == "any":
        global status_any

        if output == b'':
            return  b'Stopped\n'

        status_any = b'Paused\n'

        stop_event = threading.Event()
        players = str(subprocess.check_output(['playerctl', '-l'], text=True))[:-1].split('\n')

        threads = []
        for player_name in players:
            thread = threading.Thread(target=check_player_status, args=(player_name, stop_event))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


        output = status_any

    return output


def frame_multiplier(frames, repeats):
    more_frames = ''
    for n in range(repeats):
        more_frames += frames

    return more_frames


def show_help():
    print("""
    Usage:
    
        python /path/to/wayves/wayves.py [--off <OPTION>] [--inactive <OPTION>] [--active <OPTION>] [--player PLAYER]
    
    Animation flags:
    
        -h, --help                   -    displays this help end exit
        -p, --player <PLAYER>        -    player whit activity will be represented by this module. 
            Default value is "any", which stands for detecting any mpris (playerctl) playback.   
            Unnecessary if all other flag have same value. You can get names of active players by command 'playerctl -l'  
        -o, --off  <OPTION>          -    scripts, that shows whe player is down. 'cat' by default
        -i, --inactive   <OPTION>    -    scripts, that shows when player is up, but music is on pause. 'splash' by default
        -a, --active  <OPTION>       -    scripts, that shows whe player is up, and music is playing. 'cava' by default
    
    Options:
        
        cat                 -    ASCII cat animations
        info                -    'no sound'/'sound'
        splash              -    some different animations of 3 bars
        waves               -    scripts of 3 bars moving up and down
        cava[=SECTION]      -    dynamic waves, that depend on sound. Requires cava
                                 available SECTIONS: left, right, all. SECTION=all by default
        empty[=NUM]         -    shows NUM spaces. NUM=0 by default
        flat[=NUM]          -    shows NUM '▁'. NUM=16 by default
        
    Cava config:
        
        In config you can configure number of bars and frame rate (and other stuff)
        Config path         -    $HOME/.config/cava/cava_option_config    
    """)

    exit()
