from animation_rules import Animation
from shared import frame_multiplier

#     ▁ ▂ ▃ ▄ ▅ ▆ ▇ █
#     1 2 3 4 5 6 7 8
f1 = "▁"
f2 = "▂"
f3 = "▃"
f4 = "▄"
f5 = "▅"
f6 = "▆"
f7 = "▇"
f8 = "█"

inactive_frames_dict = {
    'dot_inactive_frames':
        f'{f1}{f1}{f1},'
        f'*{f1}{f1},'
        f'{f1}*{f1},'
        f'{f1}{f1}*,'
        f'{f1}{f1}{f1},',

    'right_splash_frames':
        f'{f1}{f1}{f1},'
        f'{f1}{f1}{f3},'
        f'{f1}{f1}{f5},'
        f'{f1}{f3}{f7},'
        f'{f1}{f5}{f5},'
        f'{f3}{f7}{f3},'
        f'{f5}{f5}{f1},'
        f'{f7}{f3}{f1},'
        f'{f5}{f1}{f1},'
        f'{f3}{f1}{f1},'
        f'{f1}{f1}{f1},',


    'center_splash_frames':
        f'{f1}{f1}{f1},'
        f'{f1}{f2}{f1},'
        f'{f1}{f4}{f1},'
        f'{f1}{f7}{f1},'
        f'{f1}{f4}{f1},'
        f'{f1}{f2}{f1},'

        f'{f2}{f1}{f2},'
        f'{f4}{f1}{f4},'
        f'{f5}{f1}{f5},'
        f'{f4}{f1}{f4},'
        f'{f3}{f1}{f3},'

        f'{f1}{f1}{f1},'
        f'{f1}{f2}{f1},'
        f'{f1}{f3}{f1},'
        f'{f1}{f2}{f1},'
        f'{f1}{f1}{f1},',


    'left_splash_frames':
        f'{f1}{f1}{f1},'
        f'{f3}{f1}{f1},'
        f'{f5}{f1}{f1},'
        f'{f7}{f1}{f1},'
        f'{f5}{f3}{f1},'
        f'{f3}{f5}{f1},'
        f'{f1}{f7}{f1},'
        f'{f1}{f5}{f3},'
        f'{f1}{f3}{f5},'
        f'{f1}{f1}{f7},'
        f'{f1}{f1}{f5},'
        f'{f1}{f1}{f3},'
        f'{f1}{f1}{f1},',

}

just_splash = Animation(
    frames=frame_multiplier(f'{f1}{f1}{f1},', 4),
    time=2
)


class SplashAnimation(Animation):
    def animation(self, category):
        just_splash.animation_without_transition(category)

        self.animation_without_transition(category)


dot_splash = SplashAnimation(
    time=0.4,
    frames=inactive_frames_dict['dot_inactive_frames']
)

right_splash = SplashAnimation(
    time=0.1,
    frames=inactive_frames_dict['right_splash_frames']
)

center_splash = SplashAnimation(
    time=0.1,
    frames=inactive_frames_dict['center_splash_frames']
)

left_splash = SplashAnimation(
    time=0.1,
    frames=inactive_frames_dict['left_splash_frames']
)

splash_animations_list = [
    dot_splash,
    center_splash,
    left_splash,
    right_splash
]
