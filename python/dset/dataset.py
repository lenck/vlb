

import json

class SequenceDataset():
 
    def __init__(self, name):
        self.name = name 
        self.

    def download(self):
        

    def load_dataset_info(self):
        with open('../data/dataset_info/{}.json'.format(self.name)) as info_file:    
            json_info = json.load(info_file)
            self.url = json_info['url']
            self.sequence_name_list = json_info['sequence_name_list
        
