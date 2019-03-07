#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: vgg_dataset.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 09-26-2017
#  Last Modified: Sun Mar  3 16:56:21 2019
#
#  Description: VGG dataset
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

from dset.dataset import SequenceDataset
import urllib
import tarfile
import os
import sys

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


class vggh_Dataset(SequenceDataset):
    """
    Oxford image matching
    """

    def __init__(self,root_dir = './datasets/', download_flag = False):
        super(vggh_Dataset,self).__init__(name = 'vggh', root_dir = root_dir, download_flag = download_flag)

    def download(self):
        """
        Download data
        """
        try:
            os.stat(self.root_dir)
        except:
            os.mkdir(self.root_dir)

        try:
            os.stat('{}{}'.format(self.root_dir,self.name))
        except:
            os.mkdir('{}{}'.format(self.root_dir,self.name))

        for sequence_name in self.sequence_name_list:
            print("Download and extract {} sequence".format(sequence_name))
            download_url = "{}{}.tar.gz".format(self.url, sequence_name)
            download_filename = "{}{}/{}.tar.gz".format(self.root_dir, self.name, sequence_name)
            try:
                os.stat('{}{}/{}'.format(self.root_dir,self.name,sequence_name))
            except:
                os.mkdir('{}{}/{}'.format(self.root_dir,self.name,sequence_name))

            try:
                urlretrieve(download_url,download_filename)
                tar = tarfile.open(download_filename)
                tar.extractall('{}{}/{}'.format(self.root_dir,self.name,sequence_name))
                tar.close()
                os.remove(download_filename)
            except:
                print('Cannot download from {}.'.format(download_url))
    
    def read_image_data(self):
        """
        Load image data
        """
        self.read_image_data_vggh()

    def read_link_data(self):
        """
        Load link data
        """
        self.read_link_data_vggh()

