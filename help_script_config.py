import json

data_path = 'data/'

dummy = {"mut_rate" : 1}
json.dumps(dummy)

with open(data_path + 'master_config.json') as f:
    conf_file = json.load(f)
    print(conf_file['mut_rate'])

