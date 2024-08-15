from bids import BIDSLayout
import bids
from collections import defaultdict
import re
import json
import sys
import yaml
import argparse
from pathlib import Path


class BIDStoNDAConfigGenerator:
    def __init__(self):
        # TODO:
        # add below in the command line args
        # -d: destination folder where the yaml and json files need to be saved
        # -s: source directory where the BIDS dataset is located
        bids.config.set_option('extension_initial_dot', True)
        parser = argparse.ArgumentParser(description='Process a dataset path.')
        parser.add_argument('dataset_path', type=str, help='The path to the dataset directory')
        args = parser.parse_args()
        self.path = args.dataset_path

        self.layout = BIDSLayout(self.path, derivatives=False)
        self.A = 'image03'
        self.pattern = r'^(?P<A>[^_]+)_(?P<X>[^.]+)\.(?P<Y>[^.]+)\.(?P<Z>[^.]+)\..+$'

        self.scan_type = {
            'anat': {
                'mprage': 'MR structural (MPRAGE)',
                't1w': 'MR structural (T1)',
                'pd': 'MR structural (PD)',
                'fspgr': 'MR structural (FSPGR)',
                'fsip': 'MR structural (FISP)',
                't2w': 'MR structural (T2)',
                'pd_t2': 'MR structural (PD, T2)',
                'b0_map': 'MR structural (B0 map)',
                'b1_map': 'MR structural (B1 map)',
                'flash': 'MR structural (FLASH)',
                'mp2rage': 'MR structural (MP2RAGE)',
                'tse': 'MR structural (TSE)',
                't1w_t2w': 'MR structural (T1, T2)',
                'mpnrage': 'MR structural (MPnRAGE)'
            },
            'pet': {
                'pet': 'PET'
            }
        }
        self.image_modality = {
            'pet': 'PET',
            'anat': 'MRI',
            'func': 'MRI',
            'dwi': 'MRI',
            'fmap': 'MRI'
        }

    def extract_file_name_components(self, file_name):
        match = re.match(self.pattern, file_name)
        if match:
            A = match.group('A')
            X = match.group('X')
            Y = match.group('Y')
            Z = match.group('Z')
            return A, X, Y, Z
        else:
            return None

    def prepare_json_contents(self, file_name):
        json_contents = {}
        _, X, Y, _ = self.extract_file_name_components(file_name)
        files = self.layout.get(
            scope=X if X != 'inputs' else 'raw', datatype=Y, return_type='file')
        for file_path in files:
            sub_index = file_path.find('derivatives')
            
            if sub_index != -1:
                sub_path = file_path[sub_index:]
                entities = self.layout.parse_file_entities(sub_path)
                subject = entities.get('subject')
                session = entities.get('session')
                if subject:
                    sub_path = sub_path.replace(subject, '{SUBJECT}')
                if session:
                    sub_path = sub_path.replace(session, '{SESSION}')
                sub_path = re.sub(r'-\d', '-{#}', sub_path)
                json_contents[sub_path] = sub_path
            else:
                sub_index = file_path.find('sub-')
        finalPath = '/'.join(self.path.split('/')[:-2]) + '/prepared_jsons'
        Path(finalPath).mkdir(parents=True, exist_ok=True)
        with open(f'{finalPath}/'+file_name, 'w') as f:
            json.dump(json_contents, f)

    def fetch_scan_type(self, Y, Z):
        scan_type = ''
        if Z.lower() in self.scan_type[Y]:
            scan_type = self.scan_type[Y][Z.lower()]
        elif '_' in Z:
            first = Z.split('_')[0]
            if first.lower() in self.scan_type[Y]:
                scan_type = self.scan_type[Y][first.lower()]
        if Y in self.scan_type[Y]:
            scan_type = self.scan_type[Y][Y]
        return scan_type

    def prepare_yaml_contents(self, file_name):
        _, _, Y, Z = self.extract_file_name_components(file_name)

        yaml_contents = {
            "scan_type": self.fetch_scan_type(Y, Z),
            "scan_object": 'Live',
            "image_file_format": 'NIFTI',
            "image_modality": self.image_modality[Y],
            "transformation_performed": 'Yes'
        }
        finalPath = '/'.join(self.path.split('/')[:-2]) + '/prepared_yamls'
        Path(finalPath).mkdir(parents=True, exist_ok=True)
        with open(f'{finalPath}/'+file_name, 'w') as f:
            yaml.dump(yaml_contents, f)

    def fetch_Z_value(self, files):
        Z = set()
        ignore_list = ['desc', 'subject', 'session', 'extension', 'suffix', 'datatype']
        for file in files:
            entities = self.layout.parse_file_entities(file)
            filtered_entities = {k: v for k,
                                 v in entities.items() if k not in ignore_list}
            for key, value in filtered_entities.items():
                if key != 'space':
                    z = key + '-' + value
                else:
                    z = value
                if ({'suffix', 'datatype'} <= entities.keys() and entities['suffix'] != entities['datatype']) or \
                        ('suffix' in entities and 'datatype' not in entities):
                    if z:
                        z = z + '_'
                    z = z + entities['suffix']
                if z:
                    Z.add(z) 
            if not Z and entities['suffix'] != entities['datatype']:
                Z.add(entities['suffix'])
        return list(Z)

    def prepare_file_names(self, X, Y, Z):
        file_names = defaultdict(set)
        '''
            file_names =  {
                json: [],
                yaml: []
            }
        '''

        filename = f"{self.A}_{X}"
        file_base = f"{filename}.{Y}."
        for z in Z:
            file_names['json'].add(file_base + z + '.json')
            file_names['yaml'].add(file_base + z + '.yaml')
        file_names['json'] = list(file_names['json'])
        file_names['yaml'] = list(file_names['yaml'])
        return file_names

    def run(self):
        X = []
        Xi = self.layout.get(scope='raw')  # inputs
        # Xd = self.layout.get(scope='derivatives')  # derivatives
        Xs = self.layout.get(scope='sourcedata')  # sourcedata
        if Xi:
            X.append('inputs')
        # if Xd:
        #     X.append('derivatives')
        if Xs:
            X.append('sourcedata')

        Y_types = self.layout.get_datatypes()

        for x in X:
            for y in Y_types:
                files = self.layout.get(
                    scope=x if x != 'inputs' else 'raw', datatype=y, return_type='file')
                Z = self.fetch_Z_value(files)
                file_names = self.prepare_file_names(X=x, Y=y, Z=Z)
                for file in file_names['json']:
                    self.prepare_json_contents(file)
                for file in file_names['yaml']:
                    self.prepare_yaml_contents(file)
        print()
        print('Please check the following folders for the json and yaml files generated:')
        print('JSON files: ' + '/'.join(self.path.split('/')[:-2]) + '/prepared_jsons')
        print('YAML files: ' + '/'.join(self.path.split('/')[:-2]) + '/prepared_yamls')
        print()

# Instructions on how to use:
# 1. Make sure you are in 'json_yaml_files' folder of the codebase
# 2. Use the below command to run the script
#   python3 prepare_files.py /Users/pbaba1/Downloads/NDA_Dataset/ds004733/
# where '/Users/pbaba1/Downloads/NDA_Dataset/ds004733/' is the path where the BIDS dataset is located

generator = BIDStoNDAConfigGenerator()
generator.run()
