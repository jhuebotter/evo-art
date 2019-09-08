from psonic import *


def play_piano(genes):
    send_message('/trigger/piano', genes['note'], genes['cutoff'], genes['amp'])
    return

def play_mod_synth(genes):
    send_message('/trigger/mod_synth', genes['note'], genes['cutoff'], genes['amp'], genes['sustain'], genes['release'], genes['mod_pulse_width'])
    return


genes = {'note' : 'C5', 'cutoff' : 100, 'amp' : 1., 'sustain' : 1, 'release': 10}

send_message('/trigger/piano', genes['note'], genes['cutoff'], genes['amp'])
print('Here we go! ')

#----------------------

'''
# Welcome to Sonic Pi v3.1

# --- CREATE METRONOME
in_thread
do
loop
do
cue: tick
sleep
1
end
end

# --- START ADDING INSTRUMENTS
#in_thread do

# SYNC INSTR TO METRONOME
#sync: tick

live_loop :piano do
  n, c, a, s, r = sync "/osc/trigger/piano"
  synth :piano, note: n, cutoff: c, amp: a, sustain: s, release: r
end

live_loop :mod_synth do
  n1, c1, a1, s1, r1, m1 = sync "/osc/trigger/mod_synth"
  synth :mod_dsaw, note: n1, cutoff: c1, amp: a1, decay: 0.05, decay_level: 0.6, sustain: s1, sustain_level: 0.5, release: r1, detune: 0.4, env_curve: 7, mod_pulse_width: m1
end

'''

