import os
import regex as re
import zipfile
import general_codes as gc

files_mexico = os.listdir('geodata\\Mexico')
n_states = {}
states_n = {}
for e in files_mexico:
    le = re.findall('^\d{2}',e)
    if len(le) > 0:
        est = re.findall('_(.+).zip', e)
        n_states[le[0]] = est[0]
        states_n[est[0]] = le[0]

def create_filepath(state):
    n_s = states_n[state]
    path = f'{n_s}_{state}.zip'
    return path

def get_statefile(state):
    if state == 'all':
        path = os.listdir('geodata\\Mexico')[-1]
        gc.create_folder(f'geodata\\region\\rpmex')
        with zipfile.ZipFile(f'geodata\\Mexico\\{path}') as sf:
            sf.extractall(f'geodata\\region\\rpmex')
    else:
        path = create_filepath(state)
        gc.create_folder(f'geodata\\region\\{state}')
        with zipfile.ZipFile(f'geodata\\Mexico\\{path}') as sf:
            sf.extractall(f'geodata\\region\\{state}')

def get_map_types(state):
    state_path = f'geodata\\region\\{state}\\conjunto_de_datos'
    files = os.listdir(state_path)
    ff = [f.split('.')[0] for f in files]
    mpt = []
    for f in ff:
        mpt = gc.actu_list(mpt, f)
    return mpt