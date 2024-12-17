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
        # Set BIDS configuration
        bids.config.set_option('extension_initial_dot', True)

        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Generate YAML and JSON files for a BIDS dataset.')
        parser.add_argument('-s', '--source', type=str, required=True, help='Path to the BIDS dataset directory')
        parser.add_argument('-d', '--destination', type=str, required=True, help='Path to save the generated YAML and JSON files')
        args = parser.parse_args()
        self.source_path = args.source
        self.destination_path = Path(args.destination)

        # Initialize BIDS layout
        self.layout = BIDSLayout(self.source_path, derivatives=True)

        # Define constants
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
        
        # Set output directories
        self.json_dir = self.destination_path / 'prepared_jsons'
        self.yaml_dir = self.destination_path / 'prepared_yamls'
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.yaml_dir.mkdir(parents=True, exist_ok=True)

    def extract_file_name_components(self, file_name):
        match = re.match(self.pattern, file_name)
        return match.groups() if match else (None, None, None, None)


    def prepare_json_contents(self, file_name, files):
        json_contents = {}
        _, X, _, _ = self.extract_file_name_components(file_name)

        sub_path_prefix = {
            'derivatives': 'derivatives',
            'inputs': 'sub-'
        }
        
        for file_path in files:
            sub_path = file_path[file_path.find(sub_path_prefix.get(X, '')):] if X in sub_path_prefix else file_path
            entities = self.layout.parse_file_entities(sub_path)
            subject, session = entities.get('subject'), entities.get('session')
            sub_path = self._replace_placeholders(sub_path, subject, session)
            json_contents[sub_path] = sub_path

        output_file = self.json_dir / file_name
        self._write_to_file(output_file, json_contents)


    def fetch_scan_type(self, Y, Z):
        if Z.lower() in self.scan_type.get(Y, {}):
            return self.scan_type[Y][Z.lower()]
        if '_' in Z:
            prefix = Z.split('_')[0]
            if prefix.lower() in self.scan_type.get(Y, {}):
                return self.scan_type[Y][prefix.lower()]
        return self.scan_type.get(Y, {}).get(Y, '')


    def prepare_yaml_contents(self, file_name):
        _, _, Y, Z = self.extract_file_name_components(file_name)

        yaml_contents = {
            "scan_type": self.fetch_scan_type(Y, Z),
            "scan_object": 'Live',
            "image_file_format": 'NIFTI',
            "image_modality": self.image_modality[Y],
            "transformation_performed": 'No'
        }
        output_file = self.yaml_dir / file_name
        self._write_to_file(output_file, yaml_contents, file_format='yaml')


    def fetch_Z_value(self, files):
        Z = set()
        ignore_list = ['desc', 'subject', 'session', 'extension', 'suffix', 'datatype']
        
        for file in files:
            entities = self.layout.parse_file_entities(file)
            filtered_entities = {k: v for k, v in entities.items() if k not in ignore_list}
            
            for key, value in filtered_entities.items():
                z = f"{key}-{value}" if key != 'space' else value
                if entities.get('suffix') and entities.get('suffix') != entities.get('datatype'):
                    z = f"{z}_{entities['suffix']}" if z else entities['suffix']
                if z:
                    Z.add(z) 
            if not Z and entities['suffix'] != entities['datatype']:
                Z.add(entities['suffix'])
                    
        return list(Z)

    def prepare_file_names(self, X, Y, Z):
        file_base = f"{self.A}_{X}.{Y}."
        return {
            'json': [f"{file_base}{z}.json" for z in Z],
            'yaml': [f"{file_base}{z}.yaml" for z in Z]
        }
    
    
    def _replace_placeholders(self, path, subject, session):
        if subject:
            path = path.replace(subject, '{SUBJECT}')
        if session:
            path = path.replace(session, '{SESSION}')
        return re.sub(r'-\d', '-{#}', path)
    
    def _write_to_file(self, output_file, contents, file_format='json'):
        with open(output_file, 'w') as f:
            if file_format == 'yaml':
                yaml.dump(contents, f)
            else:
                json.dump(contents, f, indent=2)
                
                
    def run(self): 
        scopes = {
            'raw': 'inputs',
            'derivatives': 'derivatives',
            'sourcedata': 'sourcedata'
        }
        X = [name for scope, name in scopes.items() if self.layout.get(scope=scope)]
        Y_types = self.layout.get_datatypes()
        
        for x in X:
            for y in Y_types:
                files = self.layout.get(
                    scope=x if x != 'inputs' else 'raw', datatype=y, return_type='file')
                
                Z = self.fetch_Z_value(files)
                file_names = self.prepare_file_names(X=x, Y=y, Z=Z)

                for file_name in file_names['json']:
                    self.prepare_json_contents(file_name, files)
                for file_name in file_names['yaml']:
                    self.prepare_yaml_contents(file_name)
                    
        print(f"\nJSON files: {self.json_dir}")
        print(f"YAML files: {self.yaml_dir}\n")

if __name__ == "__main__":
    generator = BIDStoNDAConfigGenerator()
    generator.run()
