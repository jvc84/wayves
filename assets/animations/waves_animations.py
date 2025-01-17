from animation_rules import Animation


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

waves_frames_dict = {
    'show_waves_frames':
        f'{f8}{f3}{f5},'
        f'{f7}{f4}{f4},'
        f'{f6}{f5}{f3},'
        f'{f5}{f6}{f2},'
        f'{f4}{f7}{f1},'
        f'{f3}{f8}{f2},'
        f'{f2}{f7}{f3},'
        f'{f1}{f6}{f4},'
        f'{f2}{f5}{f5},'
        f'{f3}{f4}{f6},'
        f'{f4}{f3}{f7},'
        f'{f5}{f2}{f8},'
        f'{f6}{f1}{f7},'
        f'{f7}{f2}{f6},',


    'waves_start_frames':
        f'{f1}{f1}{f1},'
        f'{f1}{f1}{f2},'
        f'{f1}{f1}{f3},'
        f'{f1}{f1}{f4},'
        f'{f2}{f1}{f5},'
        f'{f3}{f1}{f6},'
        f'{f4}{f1}{f7},'
        f'{f5}{f1}{f8},'
        f'{f6}{f1}{f7},'
        f'{f7}{f2}{f6},',


    'waves_stop_frames':
        f'{f6}{f1}{f5},'
        f'{f5}{f1}{f4},'
        f'{f4}{f1}{f3},'
        f'{f3}{f1}{f2},'
        f'{f2}{f1}{f1},'
        f'{f1}{f1}{f1},',
}


class WavesAnimation(Animation):
    def animation(self,category):
        self.animation_without_transition(category)



waves_main = WavesAnimation(
    time=0.1,
    frames=waves_frames_dict['show_waves_frames']
)


waves_start = WavesAnimation(
    time=0.05,
    frames=waves_frames_dict['waves_start_frames']
)

waves_stop = WavesAnimation(
    time=0.05,
    frames=waves_frames_dict['waves_stop_frames']
)
