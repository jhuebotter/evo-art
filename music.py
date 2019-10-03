from psonic import *

#synths = ['piano', 'saw', 'dull_bell', 'pretty_bell', 'beep', 'saw', 'pulse', 'dark_waves', 'supersaw', 'subpulse']
#synths = ['piano', 'mod_daw', 'bass']

#synths = ['blade', 'sine', 'dull_bell', 'saw', 'tb303']

# instuments
synths = ['pluck', 'mod_pulse', 'mod_sine', 'piano']
#rsynths = ['pluck', 'pluck', 'pluck', 'pluck']
#high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'tabla_tun1']
#low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'tabla_re']
#snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
snares = ['drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_phone1']
vox = ['ambi_choir']




instruments = [synths, bass, low_percs, high_percs, synths, synths, high_percs, synths, bass, bass]


def setup_listeners2(df, instr):
    for instrument in instr:
        print("setting up listener for")





def setup_listeners():
    print("setting up metronome TICK")

    run("""use_debug false
        
            live_loop :metronome do
                cue :tick
                sleep 0.0625
            end""")

    for synth in synths:
        print("setting up listener for", synth)
        run(f"""in_thread do
            live_loop :{synth}, sync: :tick do
            n, c, r, a, p, m, m2 = sync "/osc/trigger/{synth}"
            with_fx :reverb, mix: m, room: 0.5, pre_amp: 0.1 do
            synth :{synth}, note: n, cutoff: c, attack: a, release: r, pan: p, mod_range: m2
            end
            end
            end""")

    for sample in low_percs:
        print('Setting up listener for: ', sample)
        run(f"""in_thread do
            live_loop :{sample}, sync: :tick do              
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, pre_amp: 0.5         
            end
            end""")

    for sample in high_percs:
        print('Setting up listener for: ', sample)
        run(f"""in_thread do
            live_loop :{sample}, sync: :tick do           
            a, m, m_echo = sync "/osc/trigger/{sample}"
            with_fx :echo, mix: m_echo, pre_mix: 0.2, phase: 0.5 do
            with_fx :reverb, mix: m, pre_amp: 0.3, room: 0.2 do
            sample :{sample}, amp: a, pre_amp: 0.5
            end
            end      
            end
            end""")
    for sample in bass:
        print('Setting up listener for: ', sample)
        run(f"""in_thread do
            live_loop :{sample}, sync: :tick do            
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, lpf: 70, pre_amp: 0.5       
            end
            end""")
    for snare in snares:
        print('Setting up listener for: ', snare)
        run(f"""live_loop :{snare}, sync: :tick do          
            a, = sync "/osc/trigger/{snare}"
            sample :{snare}, amp: a        
            end""")



def play_piano(genes):
    send_message('/trigger/piano', genes['note'], genes['mix']) #genes['amp'])
    return

#def play_mod_synth(genes):
#    send_message('/trigger/mod_synth', genes['note'], genes['cutoff'], genes['amp'], genes['sustain'], genes['release'], genes['mod_pulse_width'])
#    return

def play_synth(genes):
    #print()
    #print('Nature:   ', genes['nature'])
    print('Instrument', instruments[genes['instrument']])
    #print('Low Perc: ', low_percs[genes['low_perc']])
    #print('High Perc: ', high_percs[genes['high_perc']])
    #print('Bass     : ', bass[genes['bass']])
    #print('Synth: ', synths[genes['synth']])
    print('Note:  ', genes['note'])
    #print('Radius:', genes['radius'])
    if genes['nature'] == 0:
        print('Bass playing:  ', bass[genes['instrument']])
        send_message(f"/trigger/{bass[genes['instrument']]}", genes['amp'], genes['pitch'])
    elif genes['nature'] == 1:
        print('Low Perc: ', low_percs[genes['instrument']])
        send_message(f"/trigger/{low_percs[genes['instrument']]}", genes['amp'])
    elif genes['nature'] == 2:
        print(high_percs[genes['instrument']])
        send_message(f"/trigger/{high_percs[genes['instrument']]}", genes['amp'], genes['mix_reverb'], genes['mix_echo'])
    elif genes['nature'] >= 3:
        print('Synth: ', synths[genes['instrument']])
        send_message(f"/trigger/{synths[genes['instrument']]}", genes['note'], genes['cutoff'], genes['release'],
                     genes['attack'], genes['mix_reverb'], genes['mod_range'])



    '''
    if genes['nature'] <= 3:
        print(' ')
        print('Synth Playing: ', synths[genes['synth']])
        print('Note:           ', genes['note'])
        print('Attack, Release :', round(genes['attack'], 2), round(genes['release'], 2))
        send_message(f"/trigger/{synths[genes['synth']]}", genes['note'], genes['cutoff'], genes['release'], genes['attack'], genes['decay'], genes['mix'], genes['mod_range'])
    elif genes['nature'] == 4:
        print('\n---PERC LOW')
        print('Low perscussion: ', low_percs[genes['low_perc']])
        send_message(f"/trigger/{low_percs[genes['low_perc']]}", genes['amp'])
    elif genes['nature'] == 5:
        print('\n---SNARE')
        print('SNARE          : ', snares[genes['snare']])
        send_message(f"/trigger/{snares[genes['snare']]}", genes['amp'])
    '''
    ##################
    '''
    if genes['nature'] <= 45:
        print(' ')
        print('Synth Playing: ', synths[genes['synth']])
        print('Note:           ', genes['note'])
        print('Attack, Release :', round(genes['attack'], 2), round(genes['release'], 2))
        send_message(f"/trigger/{synths[genes['synth']]}", genes['note'], genes['cutoff'], genes['release'], genes['attack'], genes['decay'], genes['mix'], genes['mod_range'])
    elif genes['nature']  >= 46 and genes['nature'] <= 60:
        print(' ')
        print('Bass playing:  ', bass[genes['bass']])
        print('Note:           ', genes['note'])
        send_message(f"/trigger/{bass[genes['bass']]}", genes['amp'], genes['pitch'])
    elif genes['nature'] >= 61 and genes['nature'] <= 70:
        print('\n---PERC LOW')
        print('Low perscussion: ', low_percs[genes['low_perc']])
        send_message(f"/trigger/{low_percs[genes['low_perc']]}", genes['amp'])
    elif genes['nature'] >= 71 and genes['nature'] <= 80:
        print('\n---SNARE')
        print('SNARE          : ', snares[genes['snare']])
        send_message(f"/trigger/{snares[genes['snare']]}", genes['amp'])
    else:
        print('\n---PERC HIGH')
        print(high_percs[genes['high_perc']])
        send_message(f"/trigger/{high_percs[genes['high_perc']]}", genes['amp'], genes['mix'], genes['mix_echo'])
    '''
    return





'''

live_loop :piano do
  n, c, a, s, r = sync "/osc/trigger/piano"
  synth :piano, note: n, cutoff: c, amp: a, sustain: s, release: r
end

'''