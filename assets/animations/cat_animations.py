from animation_rules import Animation
from shared import frame_multiplier
from subprocess import check_output, CalledProcessError
from os import system

# je = just_eye
# lec = left_eye_closed


try:
    check_output(["pgrep -x waybar"], shell=True)
    waybar_tty = check_output(["ps ax | grep waybar | awk '{print $2}'"], shell=True) 
    my_tty = check_output(["ps ax | grep \"^$$\" | awk '{print $2}'"], shell=True) 
    
    if waybar_tty == my_tty:     
        je = "･"
        lec = "&#60;"
    else:
        je = "•"
        lec = "<"
except CalledProcessError:
    je = "•"
    lec = "<"


cat_frames_dict = {
    'cat_default_frames':
        f'(=^ {je} ω {je}^=),'
        f'(=^{je} ω {je} ^=),'
        f'(=^ {je} ω {je}^=),',

    'cat_blinks_frames':
        f'(=^ {je} ω {je}^=),' +

        frame_multiplier(
            f'(=^ > ω {lec}^=),(=^ {je} ω {je}^=),',
            2
        ),

    'cat_watches_frames':
        f'(=^ {je} ω {je}^=),'
        f'(=^{je} ω {je} ^=),'
        f'(=^. ω . ^=),'
        f'(=^ . ω .^=),'
        f'(=^ {je} ω {je}^=),',

    'cat_watches_alt_frames':
        f'(=^ {je} ω {je}^=),'
        f'(=^{je} ω {je} ^=),'
        f'(=^ {je} ω {je}^=),'
        f'(=^ . ω .^=),'
        f'(=^. ω . ^=),'
        f'(=^ . ω .^=),'
        f'(=^ {je} ω {je}^=),'
        f'(=^{je} ω {je} ^=),',

    'cat_sleeps_frames':
        f'(=^ {je} ω {je}^=),' +
        frame_multiplier(
            f'(=^> ω {lec}^=)z,(=^> ω {lec}^=) ,',
            10
        ),

    'cat_looks_up_frames':
        f'(=^ {je} ω {je}^=),' +
        frame_multiplier(
            f'(=^ • ω •^=),',
            2
        ) +
        f'(=^• ω • ^=),' +
        frame_multiplier(
            f'(=^{je} ω {je} ^=),',
            2
        ) +
        f'(=^ {je} ω {je}^=),',

    'cat_disco_frames':
        f'(=^ {je} ω {je}^=),'
        f'(=^ > ω {lec}^=),'
        f'(=^ ◕ ω ◕^=),'
        f'(=^ ✧ ω ✧^=),'
        f'(=^ ♡ ω ♡^=),'
        f'(=^ ✧ ω ✧^=),'
        f'(=^ ◕ ω ◕^=),'
        f'(=^ ♡ ω ♡^=),'
        f'(=^ ◕ ω ◕^=),'
        f'(=^ > ω {lec}^=),',

    'cat_thinks_frames':
        f'(=^ {je} ω {je}^=),' +

        frame_multiplier(
            f'(=^ ◕ ω ◕^=),',
            3
        ) +

        frame_multiplier(
            f'(=^ ㅇ ω ㅇ^=),',
            3
        ),

    'cat_yawns_frames':
        f'(=^ {je} ω {je}^=),' +

        frame_multiplier(
            f'(=^ {je} ω {je}^=),(=^ > ∇ {lec}^=),',
            2
        )
}

# Main

just_cat = Animation(
    time=1,
    frames=frame_multiplier(f'(=^ {je} ω {je}^=),', 10)
)


class CatAnimation(Animation):

    def animation(self, category):
        just_cat.animation_without_transition(category)
        self.animation_without_transition(category)


cat_default = CatAnimation(
    time=3,
    frames=cat_frames_dict['cat_default_frames']
)

cat_blinks = CatAnimation(
    time=0.4,
    frames=cat_frames_dict['cat_blinks_frames']
)

cat_watches = CatAnimation(
    time=2,
    frames=cat_frames_dict['cat_watches_frames']
)

cat_watches_alt = CatAnimation(
    time=2,
    frames=cat_frames_dict['cat_watches_alt_frames']
)

cat_sleeps = CatAnimation(
    time=1.7,
    frames=cat_frames_dict['cat_sleeps_frames']
)

cat_looks_up = CatAnimation(
    time=2,
    frames=cat_frames_dict['cat_looks_up_frames']
)

cat_disco = CatAnimation(
    time=1,
    frames=cat_frames_dict['cat_disco_frames']
)

cat_thinks = CatAnimation(
    time=1,
    frames=cat_frames_dict['cat_thinks_frames']
)

cat_yawns = CatAnimation(
    time=1,
    frames=cat_frames_dict['cat_yawns_frames']
)


cat_animations_list = [
    cat_default,
    cat_blinks,
    cat_watches,
    cat_watches_alt,
    cat_sleeps,
    cat_looks_up,
    cat_disco,
    cat_thinks,
    cat_yawns
]
