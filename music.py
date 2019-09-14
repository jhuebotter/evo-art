from psonic import *

#synths = ['piano', 'saw', 'dull_bell', 'pretty_bell', 'beep', 'saw', 'pulse', 'dark_waves', 'supersaw', 'subpulse']
#synths = ['piano', 'mod_daw', 'bass']

synths = ['piano', 'sine', 'pretty_bell']
samples = ['elec_soft_kick', 'sn_dub', 'tabla_ke3', 'tabla_na_s', 'elec_wood', 'bass_voxy_hit_c', 'drum_cowbell', 'drum_cymbal_pedal']
                                          



def setup_listeners():

    for synth in synths:
        print("setting up listener for", synth)
        run(f"""live_loop :{synth} do
            a, = sync "/osc/trigger/{synth}"
            synth :{synth}, note: a
            end """)
    for sample in samples:
        print('Setting up listener for: ', sample)
        run(f"""live_loop :{sample} do              
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, pre_amp: 0.5         
            end """)


def play_piano(genes):
    send_message('/trigger/piano', genes['note'], genes['mix']) #genes['amp'])
    return

#def play_mod_synth(genes):
#    send_message('/trigger/mod_synth', genes['note'], genes['cutoff'], genes['amp'], genes['sustain'], genes['release'], genes['mod_pulse_width'])
#    return

def play_synth(genes):
    print()
    print('Nature: ', genes['nature'])
    print('Sample ', samples[genes['sample']])
    print('Synth: ', synths[genes['synth']])

    print('Note:  ', genes['note'])
    print('Radius:', genes['radius'])
    if genes['nature'] == 1:
        send_message(f"/trigger/{synths[genes['synth']]}", genes['note']) #, genes['amp'], genes['sustain'], genes['release'])
    else:
        send_message(f"/trigger/{samples[genes['sample']]}", genes['amp']) #, genes['amp'], genes['sustain'], genes['release'])


setup_listeners()


'''

live_loop :piano do
  n, c, a, s, r = sync "/osc/trigger/piano"
  synth :piano, note: n, cutoff: c, amp: a, sustain: s, release: r
end

'''