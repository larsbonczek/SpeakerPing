import sounddevice as sd
import numpy as np
import time
import configparser

config = configparser.ConfigParser()
config.read('speakerping.ini')

samplerate = config.getint('speakerping', 'Samplerate', fallback=44100)
duration = config.getfloat('speakerping', 'Duration', fallback=2.)
frequency = config.getfloat('speakerping', 'Frequency', fallback=10.)
volume = config.getfloat('speakerping', 'Volume', fallback=100.)
interval = config.getfloat('speakerping', 'Interval', fallback=1200.)

samples = np.arange(int(samplerate * duration)) / float(samplerate)

amplitude = np.iinfo(np.int16).max * volume / 100.
envelope = np.power(np.sin(np.pi * samples / duration), 2)
wave = amplitude * envelope * np.sin(2 * np.pi * frequency * samples)

wav_wave = np.array(wave, dtype=np.int16)

sd.default.samplerate = samplerate

print(f'Start playing {frequency} Hz tone for {duration} s every {interval} s')

while True:
    print('beep')
    sd.play(wav_wave, samplerate, blocking=True)
    time.sleep(max(interval - duration, 0))
