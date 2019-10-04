from genetics import *
import json
import os

presets_path = 'data/presets/'
default_config_path = 'data/presets/default/config.json'

# for inputting a preset name to load an existing preset as the base
'''
preset_name = ''
config_path = presets_path + preset_name + '/' + 'config.json'
'''

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def create_preset(preset_path, config_path = default_config_path):
    config = load_config(config_path)
    create_data_structure(preset_path, config)
    save_config(preset_path, config)

def load_config(config_path):   # loads .json config file for a preset
    with open(config_path) as f:
        config = json.load(f)
    return config

def save_config(preset_path, config):
    with open(preset_path + 'config.json', 'w') as fp:
        json.dump(config, fp)

def create_data_structure(preset_path, config):
    create_folder(preset_path)
    create_folder(preset_path + 'initial')
    for nature in config['natures']:
        create_initial_genes(preset_path + 'initial/', config, nature)
    create_folder(preset_path + 'current')

def create_initial_genes(preset_path, config, nature):
    df = make_genepool2(config['size'])   # pull size from config here if needed
    df.to_csv(preset_path + nature + '.csv')


# example to create a copy of default
'''
preset_path = presets_path + 'new/'
create_preset(preset_path, config_path)
'''

# example to create a copy of a config located at config_path
'''
preset_path = presets_path + 'new/'
create_preset(preset_path, config_path)
'''