from psonic import *
import os

def play_piano(genes):
    send_message('/trigger/piano', genes['note'], genes['mix'], genes['note'], genes['note'])
    #os.system("sonic-pi-tool.py eval 'play :C4'")
    print('play note')
    return

def play_mod_synth(genes):
    send_message('/trigger/mod_synth', genes['note'], genes['cutoff'], genes['amp'], genes['sustain'], genes['release'], genes['mod_pulse_width'])
    return


'''
genes = {'note' : 'C5', 'cutoff' : 100, 'amp' : 1., 'sustain' : 1, 'release': 10}
send_message('/trigger/piano', genes['note'], genes['cutoff'], genes['amp'])
print('Here we go! ')

live_loop :piano do
  n, c, a, s, r = sync "/osc/trigger/piano"
  synth :piano, note: n, cutoff: c, amp: a, sustain: s, release: r
end

'''
