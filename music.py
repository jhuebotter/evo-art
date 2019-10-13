from psonic import *
import glob as glob
import os

# instuments
synths = ['mod_beep', 'mod_pulse', 'mod_sine', 'growl']
#synths = ['hollow', 'dark_ambience', 'dull_bell', 'sine']
#synths = ['piano', 'piano', 'piano', 'piano']
#synths = ['tech_saws', 'tech_saws', 'tech_saws', 'tech_saws']

#high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'tabla_tun1']
#low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'tabla_re']
#snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
snares = ['drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_phone1']
vox = ['ambi_choir']

BASS = [x for x in glob.glob('samples/BASS/*')]
HIGH_PERC = [x for x in glob.glob('samples/HIGH_PERC/*')]
LOW_PERC = [x for x in glob.glob('samples/LOW_PERC/*')]

base_dir = os.getcwd() + '/'

#print(base_dir)
#print(LOW_PERC)
#print(HIGH_PERC)

instruments = [synths, bass, low_percs, high_percs, synths, synths, high_percs, synths, bass, bass]

def get_sample_name(path):
    
    string = str(path)
    elem = string.split('/')[-1]
    sample_name = elem.replace('.wav', '')
    return sample_name


def setup_listeners2():
    
    #print("setting up metronome TICK")

    run("""use_debug false
live_loop :metronome do
  cue :tick
  sleep 0.0625
end""")

    for synth in synths:
        #print("setting up listener for", synth)
        run(f"""in_thread do
  live_loop :{synth}, sync: :tick do
    n, c, a, r, p, m = sync "/osc/trigger/{synth}"
    with_fx :reverb, mix: m, room: 0.5, pre_amp: 0.1 do
      synth :{synth}, note: n, cutoff: c, attack: a, release: r, pan: p
    end
  end
end""")

    for bass in BASS:
        sample_name = get_sample_name(bass)
        #print(sample_name)
        #print('Setting up listener for: ', bass)
        run(f"""in_thread do
  live_loop :{sample_name}, sync: :tick do
    a, p = sync "/osc/trigger/{sample_name}"
    sample '{base_dir}{bass}', amp: a, pre_amp: 0.6, pitch: p
  end
end""")


    for perc in HIGH_PERC:
        sample_name = get_sample_name(perc)
        #print('Setting up listener for: ', perc)
        #print(sample_name)
        run(f"""in_thread do
  live_loop :{sample_name}, sync: :tick do
    a, m, m_echo, p = sync "/osc/trigger/{sample_name}"
    with_fx :echo, mix: m_echo, pre_mix: 0.2, phase: 1 do
      with_fx :reverb, mix: m, pre_amp: 0.3, room: 0.2 do
        sample '{base_dir}{perc}', amp: a, pitch: p, pre_amp: 0.7
      end
    end
  end
end""")


    for perc in LOW_PERC:
        sample = get_sample_name(perc)
        #print(sample)
        #print('Setting up listener for: ', sample)
        run(f"""in_thread do
  live_loop :{sample}, sync: :tick do
    a, p = sync "/osc/trigger/{sample}"
    sample '{base_dir}{perc}', amp: a, pre_amp: 0.3, pitch: p
  end
end""")





def setup_listeners():
    #print("setting up metronome TICK")

    run("""use_debug false
        
            live_loop :metronome do
                cue :tick
                sleep 0.0625
            end""")

    for synth in synths:
        #print("setting up listener for", synth)
        run(f"""in_thread do
            live_loop :{synth}, sync: :tick do
            n, c, r, a, p, m, m2 = sync "/osc/trigger/{synth}"
            with_fx :reverb, mix: m, room: 0.5, pre_amp: 0.1 do
            synth :{synth}, note: n, cutoff: c, attack: a, release: r, pan: p, mod_range: m2
            end
            end
            end""")

    for sample in low_percs:
        #print('Setting up listener for: ', sample)
        run(f"""in_thread do
            live_loop :{sample}, sync: :tick do              
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, pre_amp: 0.5         
            end
            end""")

    for sample in high_percs:
        #print('Setting up listener for: ', sample)
        run(f"""in_thread do
                live_loop :{sample}, sync: :tick do           
                    a, m, m_echo = sync '/osc/trigger/{sample}'
                    with_fx :echo, mix: m_echo, pre_mix: 0.2, phase: 0.5 do
                        with_fx :reverb, mix: m, pre_amp: 0.3, room: 0.2 do
                            sample :{sample}, amp: a, pre_amp: 0.5
                        end
                    end      
                end
            end""")

    for sample in bass:
        #print('Setting up listener for: ', sample)
        run(f"""in_thread do
            live_loop :{sample}, sync: :tick do            
            a, = sync "/osc/trigger/{sample}"
            sample :{sample}, amp: a, lpf: 70, pre_amp: 0.5       
            end
            end""")
    for snare in snares:
        #print('Setting up listener for: ', snare)
        run(f"""live_loop :{snare}, sync: :tick do          
            a, = sync "/osc/trigger/{snare}"
            sample :{snare}, amp: a        
            end""")


def play_synth(genes):

    # Play snyths

    if 'bass' in genes['nature']:
        #print('Bass playing:  ', BASS[genes['instrument']])
        send_message(f"/trigger/{get_sample_name(BASS[genes['instrument']])}", genes['amp'], genes['pitch'])
    elif 'low_perc' in genes['nature']:
        #print('Low Perc: ', LOW_PERC[genes['instrument']])
        send_message(f"/trigger/{get_sample_name(LOW_PERC[genes['instrument']])}", genes['amp'], genes['pitch'])
    elif 'high_perc' in genes['nature']:
        #print(HIGH_PERC[genes['instrument']])
        send_message(f"/trigger/{get_sample_name(HIGH_PERC[genes['instrument']])}", genes['amp'], genes['mix_reverb'], genes['mix_echo'], genes['pitch'])
    elif 'synths' in genes['nature']:
        #print('Synth: ', synths[genes['instrument']])
        send_message(f"/trigger/{synths[genes['instrument']]}", genes['note'], genes['cutoff'], genes['attack'], genes['release'], genes['mix_reverb'])

    return


def stop_all_listeners():

    # Stop running processes in Sonic Pi

    #run("/stop-all-jobs")
    stop()




'''

live_loop :piano do
  n, c, a, s, r = sync "/osc/trigger/piano"
  synth :piano, note: n, cutoff: c, amp: a, sustain: s, release: r
end

'''