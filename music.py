from psonic import *

#synths = ['piano', 'saw', 'dull_bell', 'pretty_bell', 'beep', 'saw', 'pulse', 'dark_waves', 'supersaw', 'subpulse']
#synths = ['piano', 'mod_daw', 'bass']

#synths = ['blade', 'sine', 'dull_bell', 'saw']
synths = ['hollow', 'sine', 'fm', 'mod_sine', 'growl']
high_percs = ['tabla_na_s', 'elec_wood', 'drum_cymbal_pedal', 'drum_snare_soft', 'drum_cymbal_closed', 'drum_tom_hi_soft']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'glitch_perc2', 'drum_tom_mid_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_robot3', 'mehackit_phone1']

def setup_listeners():

    for synth in synths:
        print("setting up listener for", synth)
        run(f"""live_loop :{synth} do
            a, r = sync "/osc/trigger/{synth}"
            with_fx :reverb, room: 0.5, pre_amp: 0.1 do
            synth :{synth}, note: a, release: r
            end
            end """)
    for sample in low_percs:
        print('Setting up listener for: ', sample)
        run(f"""live_loop :{sample} do              
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, pre_amp: 0.5         
            end """)
    for sample in high_percs:
        print('Setting up listener for: ', sample)
        run(f"""live_loop :{sample} do              
            a, m = sync "/osc/trigger/{sample}"
            with_fx :reverb, mix: m, pre_amp: 0.3, room: 0.2, pre_mix: 0.5 do
            sample :{sample}, amp: a, pre_amp: 0.5
            end         
            end """)
    for sample in bass:
        print('Setting up listener for: ', sample)
        run(f"""live_loop :{sample} do              
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, note: :C4, finish: 0.5, pre_amp: 0, cutoff:50         
            end """)



def play_piano(genes):
    send_message('/trigger/piano', genes['note'], genes['mix']) #genes['amp'])
    return

#def play_mod_synth(genes):
#    send_message('/trigger/mod_synth', genes['note'], genes['cutoff'], genes['amp'], genes['sustain'], genes['release'], genes['mod_pulse_width'])
#    return

def play_synth(genes):
    #print()
    #print('Nature:   ', genes['nature'])
    #print('Low Perc: ', low_percs[genes['low_perc']])
    #print('High Perc: ', high_percs[genes['high_perc']])
    #print('Bass     : ', bass[genes['bass']])
    #print('Synth: ', synths[genes['synth']])
    #print('Note:  ', genes['note'])
    #print('Radius:', genes['radius'])
    #'''
    if genes['nature'] <= 4:
        print('Synth Playing: ', synths[genes['synth']])
        send_message(f"/trigger/{synths[genes['synth']]}", genes['note'], genes['release'])
    elif genes['nature'] == 5:
        print('Bass playing:  ', bass[genes['bass']])
        send_message(f"/trigger/{bass[genes['bass']]}", genes['amp'])
    elif genes['nature'] >= 6 and genes['nature'] < 8:
        #print('Low perscussion: ', low_percs[genes['low_perc']])
        send_message(f"/trigger/{low_percs[genes['low_perc']]}", genes['amp'])  # , genes['amp'], genes['sustain'], genes['release'])
    else:
        #print(high_percs[genes['high_perc']])
        send_message(f"/trigger/{high_percs[genes['high_perc']]}", genes['amp'], genes['mix'])
    #'''
    return


setup_listeners()


'''

live_loop :piano do
  n, c, a, s, r = sync "/osc/trigger/piano"
  synth :piano, note: n, cutoff: c, amp: a, sustain: s, release: r
end

'''