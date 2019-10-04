from genetics import *
import json
import os

PRESETS_PATH = 'data/presets/'
MASTER_CONFIG_PATH = 'data/master_config.json'
DEFAULT_CONFIG_PATH = 'data/presets/default/config.json'

'''
# for inputting a preset name to load an existing preset as the base
preset_name = ''
config_path = PRESETS_PATH + preset_name + '/' + 'config.json'

# example to create a copy of default
preset_path = PRESETS_PATH + 'new/'
create_preset(preset_path, config_path)

# example to create a copy of a config located at config_path
preset_path = PRESETS_PATH + 'new/'
create_preset(preset_path, config_path)
'''

def read_preset_path(master_config_path='data/presets/master_config.json'):
    master_config = load_config(master_config_path)
    return master_config['']

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

def create_preset(preset_name, config_path = DEFAULT_CONFIG_PATH):
    preset_path = 'data/presets/' + preset_name + '/'
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
    df = make_genepool(config['size'])   # pull size from config here if needed
    df.to_csv(preset_path + nature + '.csv')


# these lines could also be in the main file
master_config = load_config(MASTER_CONFIG_PATH)
current_config_path = master_config['preset_path']
create_preset('default3') # test line