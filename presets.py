from genetics import *
from autopilot import *
import json
import os
import glob

PRESETS_DIR_PATH = 'data/presets/'
MASTER_CONFIG_PATH = 'data/master_'
DEFAULT_CONFIG_DIR_PATH = PRESETS_DIR_PATH + 'default/'


def read_preset_path(master_config_path=MASTER_CONFIG_PATH):
    
    master_config = load_config(master_config_path)
    return master_config["preset_path"]


def create_folder(directory):
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error creating directory: ' + directory)


def create_preset(preset_name, config_path=DEFAULT_CONFIG_DIR_PATH):
    
    preset_path = 'data/presets/' + preset_name + '/'
    config = load_config(config_path)
    create_data_structure(preset_path, config)
    save_config(preset_path, config)


def load_config(config_path=MASTER_CONFIG_PATH):   # loads .json config file for a preset
    
    with open(config_path + 'config.json') as f:
        config = json.load(f)
        
    return config


def save_config(path, config):
    
    with open(path + 'config.json', 'w') as fp:
        json.dump(config, fp)


def create_data_structure(preset_path, config):
    
    create_folder(preset_path)
    create_folder(preset_path + 'initial')
    for nature in config['natures']:
        create_initial_genes(preset_path + 'initial/', config, nature)
    create_folder(preset_path + 'current')


def create_initial_genes(preset_path, config, name):
    
    df = make_genepool(config['pop_size'])   # pull size from config here if needed
    df.to_csv(preset_path + name + '.csv')

def initialize_current(preset_path):

    create_folder(f'{preset_path}current')

    for file in glob.glob(f'{preset_path}initial/*'):
        data = load_genepool(file)
        name = file.split('/')[-1]
        save_genepool(data, f'{preset_path}current/{name}')

def create_preset_from_config_file(config, name):
    '''
    Create complete preset folder from config dict object

    :param config: dictionary containing all config keys and values
    :param name: name for the preset
    :return: preset folder with /initial, initialized /current and config.json
    '''

    preset_path = f'{PRESETS_DIR_PATH}{name}/'
    create_folder(preset_path)
    # place config.json in folder
    save_config(preset_path, config)

    # now create initial folder
    create_folder(f'{preset_path}initial')

    suffix = 1  # suffix for multiple pools of same instrument category

    for nature in config['natures']:
        # create initial gene pools
        create_initial_genes(f'{preset_path}initial/', config, f'{nature}_{suffix}')
        suffix += 1

    initialize_current(preset_path)




# these lines could also be in the main file
master_config = load_config(MASTER_CONFIG_PATH)
current_config_path = master_config['preset_path']
#create_preset('default3') # test line


#conf = {"mut_rate": [0,0.2,1,1], "gen_length": 8, "bpm_base": 10, "genre": "test", "natures": ["low_perc", "bass", "synths", "synths"], "size": 20, "refresh_rate": 8}

#create_preset_from_config_file(conf, 'l-b-s-s')