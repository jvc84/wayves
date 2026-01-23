import subprocess
import threading

from sys import exit


PLAYER_NAME = "any"
ANY_PLAYER_STATUS = b'Paused\n'


def check_sound_and_player_status() -> (bool, bool):
    global PLAYER_NAME

    if PLAYER_NAME == "cava":
        return True, False

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


def check_playerctl(player_slug):
    try:
        output = subprocess.check_output([f'playerctl status --player="{player_slug}"'], shell=True)

        if b"Playing" in output:
            return 1
        else:
            return 0
    except subprocess.CalledProcessError:
        return 0


def check_player_status(player_slug, stop_event):
    result = check_playerctl(player_slug)

    if result == 1 and not stop_event.is_set():
        global ANY_PLAYER_STATUS
        ANY_PLAYER_STATUS = b'Playing\n'
        stop_event.set()
    return 0


def get_status():
    global PLAYER_NAME

    if PLAYER_NAME == "any":
        command = 'playerctl -l'
    else:
        command = f'playerctl status --player="{PLAYER_NAME}"'

    output = subprocess.check_output([command], shell=True) or None

    if PLAYER_NAME == "any":
        global ANY_PLAYER_STATUS

        if not output:
            return  b'Stopped\n'

        ANY_PLAYER_STATUS = b'Paused\n'

        stop_event = threading.Event()
        players = str(subprocess.check_output(['playerctl', '-l'], text=True))[:-1].split('\n')

        threads = []
        for player_slug in players:
            thread = threading.Thread(target=check_player_status, args=(player_slug, stop_event))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        output = ANY_PLAYER_STATUS

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
        -o, --off  <OPTION>          -    script, that shows when player is down. 'cat' by default
        -i, --inactive   <OPTION>    -    script, that shows when player is up, but music is on pause. 'splash' by default
        -a, --active  <OPTION>       -    script, that shows when player is up, and music is playing. 'cava' by default
    
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
