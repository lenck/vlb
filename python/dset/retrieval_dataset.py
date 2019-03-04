#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: retrieval_dataset.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 09-26-2017
#  Last Modified: Sat Mar  2 20:48:02 2019
#
#  Description:Retrieval dataset template
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

"""
This module describe dataset template for image retrieval task
"""

import json
import os
from abc import ABCMeta, abstractmethod


class RetrievalDataset():
    """Sequence dataset for image retrieval
    
    Attributes
    ----------

    name: str
        Name of the dataset
    root_dir: str
        Directory for the data
    download_flag: boolean
        Download data or not. Keep it False, unless you need to update the dataset. 
                    Data will automatically download, if there is no data in the root_dir.
    """

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
        """
        Load data from hard disk
        """
        try:
            with open('{}/dataset_info/{}.json'.format(self.root_dir, self.name)) as info_file:    
                json_info = json.load(info_file)
        except:
            print('Cannot load database information file: {}dataset_info/{}.json'.format(self.root_dir, self.name))
            return

        self.url = json_info['url']

    @abstractmethod
    def download(self):
        """
        Download data
        """
        pass

    @abstractmethod
    def read_gallery_list(self):
        """
        Load gallery image list
        """
        pass

    @abstractmethod
    def read_query_list(self):
        """
        Load query image list
        """
        pass
