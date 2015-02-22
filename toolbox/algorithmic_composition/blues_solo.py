""" Synthesizes a blues solo algorithmically """

from Nsound import *
import numpy as np
from random import choice

def add_note(out, instr, key_num, duration, bpm, volume):
    """ Adds a note from the given instrument to the specified stream

        out: the stream to add the note to
        instr: the instrument that should play the note
        key_num: the piano key number (A 440Hzz is 49)
        duration: the duration of the note in beats
        bpm: the tempo of the music
        volume: the volume of the note
	"""
    freq = (2.0**(1/12.0))**(key_num-49)*440.0
    stream = instr.play(duration*(60.0/bpm),freq)
    stream *= volume
    out << stream



# Controls the sample rate for the sound file generated
sampling_rate = 44100.0
Wavefile.setDefaults(sampling_rate, 16)

bass = GuitarBass(sampling_rate)	# use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

# Creates a stream of the same format as solo from 'backing.wav' file
backing_track = AudioStream(sampling_rate, 1) 
Wavefile.read('backing.wav', backing_track)

m = Mixer()

""" these are the piano key numbers for a 3 octave blues scale in A
	See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
phrigian_scale = [25, 26, 28, 30, 32, 33, 35, 37, 38, 42, 44, 45, 47, 49, 50, 52, 54, 56, 57]
beats_per_minute = 45				# Let's make a slow blues solo

curr_note = 0
add_note(solo, bass, blues_scale[curr_note], 1.0, beats_per_minute, 1.0)

curr_vol = 1.0



licks = [ [ [1, 0.5], [1, 0.5], [1, 0.5], [1, 0.5] ], [ [-1, 0.5], [-1, 0.5], [-1, 0.5], [-1, 0.5] ], [ [3, 0.5], [-1, 0.5], [1, 0.5], [-1, 0.5] ] ]
swing_licks = [ [ [1, 0.5*1.1], [1, 0.5*0.9], [1, 0.5*1.1], [1, 0.5*0.9] ], [ [-1, 0.5*1.1], [-1, 0.5*0.9], [-1, 0.5*1.1], [-1, 0.5*0.9] ], [ [3, 0.5*1.1], [-1, 0.5*0.9], [1, 0.5*1.1], [-1, 0.5*0.9] ] ]

# Creates set of licks that either crescendo or decrescendo for additional dynamics to the solo
v_chng = 0.1
licks_cres = [ [ [1, 0.5,v_chng], [1, 0.5, v_chng], [1, 0.5, v_chng], [1, 0.5, v_chng] ], [ [1, 0.5, -v_chng], [1, 0.5, -v_chng], [1, 0.5, -v_chng], [1, 0.5, -v_chng] ], [ [-1, 0.5, v_chng], [-1, 0.5, v_chng], [-1, 0.5, v_chng], [-1, 0.5, v_chng] ], [ [-1, 0.5, -v_chng], [-1, 0.5, -v_chng], [-1, 0.5, -v_chng], [-1, 0.5, -v_chng] ] , [ [3, 0.5, v_chng], [-1, 0.5, v_chng], [1, 0.5, v_chng], [-1, 0.5, v_chng] ], [ [3, 0.5, -v_chng], [-1, 0.5, -v_chng], [1, 0.5, -v_chng], [-1, 0.5, -v_chng] ] ]


for i in range(20):
    lick = choice(licks_cres)
    for note in lick:
        curr_note = choice([(curr_note+note[0])%len(blues_scale),6*choice([0,1,2,3])])
        curr_vol += note[2]
        add_note(solo, bass, blues_scale[curr_note], note[1], beats_per_minute, curr_vol)

solo *= 1.0             # adjust relative volumes to taste
backing_track *= 2.0

m.add(2.25, 0, solo)    # delay the solo to match up with backing track    
m.add(0, 0, backing_track)

m.getStream(500.0) >> "slow_blues.wav"

solo >> "blues_solo.wav"