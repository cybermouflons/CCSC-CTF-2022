from pydub import AudioSegment

FLAG = 'CCSC{ririck&momorty}'

INPUT_AUDIO_FILE_NAME = 'original.mp3'
OUTPUT_AUDIO_FILE_NAME = 'ufo.mp3'

sound = AudioSegment.from_mp3(f'./{INPUT_AUDIO_FILE_NAME}')

sound_clip_0 = sound[35596:35596 + 225]
sound_clip_1 = sound[35288:35288 + 225]

flag_bin = ''.join([bin(x)[2:] for x in FLAG.encode('ascii')])

soundmap = {'0': sound_clip_0, '1': sound_clip_1}

flag_sound = sound
for b in flag_bin:
    flag_sound += soundmap[b]

flag_sound.export(f'../public/{OUTPUT_AUDIO_FILE_NAME}', format='mp3')
