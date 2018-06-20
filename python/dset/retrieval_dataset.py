import numpy as np
import json
import os
import cv2
from abc import ABCMeta, abstractmethod

import scipy.ndimage

class Image:
    idx = ''
    label = ''
    filename = ''

class RetrievalDataset():
    __metaclass__ = ABCMeta 
    def __init__(self, name, root_dir = './datasets/', download_flag = False):
        self.name = name
        self.root_dir = root_dir
        self.load_dataset_info()
        
        if download_flag:
            self.download()

        try:
            os.stat(root_dir + self.name + '/')
        except:
            self.download()

        self.read_gallery_list()
        self.read_query_list()

    def load_dataset_info(self):
        try:
            with open('{}/dataset_info/{}.json'.format(self.root_dir, self.name)) as info_file:    
                json_info = json.load(info_file)
        except:
            print('Cannot load database information file: {}dataset_info/{}.json'.format(self.root_dir, self.name))
            return

        self.url = json_info['url']

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def read_gallery_list(self):
        pass

    @abstractmethod
    def read_query_list(self):
        pass

