#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: dataset.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 09-26-2017
#  Last Modified: Sun Mar  3 16:39:33 2019
#
#  Description:Dataset template
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

"""
This module describe dataset template
"""

import numpy as np
import json
import os
import cv2
from abc import ABCMeta, abstractmethod

import scipy.ndimage

class Image:
    """Image data structure.

    Attributes
    ----------

    id: str
        ID of the image
    image_data: array
        Image data
    label:  str
        Description for the label
    filename:  str
        Name of the file
    """

    idx = ''
    image_data = None
    label = ''
    filename = ''

class Link:
    """Link data structure. Describe an image pair, it's useful for matching dataset.
    
    Attributes
    ----------

    source: str
        ID of the source image
    target: str
        ID of the target image
    filename: str
        filename of the transformation matrix
    transform_matrix:  array
        Transform Matrix of the image pair
    task:  dict
        Task information 
    """

    source = ''
    target = ''
    filename = ''
    transform_matrix = None
    task = {}

class Sequence:
    """Sequence for a list of images and links.

    Attributes
    ----------

    name: str
        Name of the sequence
    description: str
        Description of the sequence
    image_id_list: list
        List of image id (for keep the order of the images)
    image_dict: dict
        Dict for image data
    link_id_list:  list
        List of link id (for keep the order of the links)
    link_dict:  dict
        link_dict: Dict for all links in the sequence
    """

    name = ''
    description = ''
    image_id_list = None
    image_dict = None # list cannot be initialized here!
    link_id_list = None
    link_dict = None
    
    def images(self):
        """
        Return images in the sequence.
        
        :returns: images
        :rtype: list
        """

        return self.image_dict.items()

    def links(self):
        """
        Return links in the sequence.
        
        :returns: links
        :rtype: list
        """

        return self.link_dict.items()

class SequenceDataset():
    """Sequence dataset for image matching test
    
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

        self.read_image_data()
        self.read_link_data()
        self.set_task()

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
        self.sequence_name_list = json_info['Sequence Name List']
        self.sequence_num = len(self.sequence_name_list)
        self.sequences = {}
        
        for read_sequence in json_info['Sequences']:
            this_sequence = Sequence()
            try:
                this_sequence.name = read_sequence['Name']
                this_sequence.description = read_sequence['Description']
                this_sequence.label = read_sequence['Label']
            except:
                pass
            
            this_sequence.image_dict = {}
            this_sequence.image_id_list = []

            for read_image in read_sequence['Images']:
                this_image = Image()
                this_image.idx = read_image['id'] 
                this_image.label = read_image['label']
                this_image.filename = read_image['file']

                this_sequence.image_dict[this_image.idx] = this_image
                this_sequence.image_id_list.append(this_image.idx)

            this_sequence.link_dict = {}
            this_sequence.link_id_list = []

            for read_link in read_sequence['Links']:
                this_link = Link()
                this_link.source = read_link['source']
                this_link.target = read_link['target']
                this_link.filename = None
                this_link.transform_matrix = None

                this_link.task = {}
                
                try:
                    this_link.filename = read_link['file']
                except:
                    this_link.filename = None
                    try:
                        this_link.transform_matrix = []
                        for line in read_link['transform_matrix'].split(';'):
                            array_line = []
                            for element in line.split(' '):
                                number = float(element)
                                array_line.append(number)
                            this.link.transform_matrix.append(array_line)
                        this_link.transform_matrix = np.array(this_link.transform_matrix)
                    except:
                        this_link.transform_matrix = np.eye(3,dtype = np.float)

                
                this_sequence.link_dict["{}_{}".format(read_link['source'],read_link['target'])] = this_link
                this_sequence.link_id_list.append("{}_{}".format(read_link['source'],read_link['target']))
                
            self.sequences[this_sequence.name] = this_sequence

    def read_image_data_vggh(self):
        """
        Load image data from vggh like dataset
        """

        for sequence_name in self.sequence_name_list:
            sequence = self.sequences[sequence_name]
            for image_id in sequence.image_id_list:
                img = scipy.ndimage.imread('{}{}/{}'.format(self.root_dir, self.name, sequence.image_dict[image_id].filename))
                try:
                    #opencv image read cause issue when read pgm file
                    #img = cv2.imread('{}{}/{}'.format(self.root_dir, self.name, sequence.image_dict[image_id].filename))
                    img = scipy.ndimage.imread('{}{}/{}'.format(self.root_dir, self.name, sequence.image_dict[image_id].filename))
                    #print('{}{}/{}'.format(self.root_dir, self.name, sequence.image_dict[image_id].filename))
                    if len(img.shape) == 3:
                        if img.shape[2] == 4:
                            img = img[:,:,:3]

                    _, file_extension = os.path.splitext(sequence.image_dict[image_id].filename)

                    if file_extension == 'jpg' or file_extension == 'JPG' \
                            or file_extension == 'jpeg' or file_extension == 'JPEG':
                        ftest = open('{}/{}/{}'.format(self.root_dir, self.name, sequence.image_dict[image_id].filename), 'rb')
                        tags = exifread.process_file(ftest)
                        
                        try:
                            if str(tags['Thumbnail Orientation']) == 'Rotated 90 CW':
                                img = cv2.transpose(img)  
                                img = cv2.flip(img, 1)
                            elif str(tags['Thumbnail Orientation']) == 'Rotated 90 CCW':
                                img = cv2.transpose(img)  
                                img = cv2.flip(img, 0)
                            elif str(tags['Thumbnail Orientation']) == 'Rotated 180':
                                img = cv2.flip(img, -1)
                        except:
                            pass
                    sequence.image_dict[image_id].image_data = img
                except:
                    print('Cannot read image file: {}{}/{}. Did you download the dataset correctly?'\
                            .format(self.root_dir, self.name, sequence.image_dict[image_id].filename))
                    exit()


    def read_link_data_vggh(self):
        """
        Load link data from vggh like dataset
        """

        for sequence_name in self.sequence_name_list:
            sequence = self.sequences[sequence_name]
            for link_id in sequence.link_id_list:
                if sequence.link_dict[link_id].filename is not None:
                    sequence.link_dict[link_id].transform_matrix = np.eye(3,dtype = np.float)
                    try:
                        with open('{}{}/{}'.format(self.root_dir, self.name, sequence.link_dict[link_id].filename)) as f:
                            sequence.link_dict[link_id].transform_matrix = []
                            for line in f:
                                if len(line)<2:
                                    continue
                                array_line = []
                                for element in line.split(' '):
                                    if element == '' or element =='\n':
                                        continue
                                    number = float(element)
                                    array_line.append(number)
                                sequence.link_dict[link_id].transform_matrix.append(array_line)
                            sequence.link_dict[link_id].transform_matrix = np.array(sequence.link_dict[link_id].transform_matrix)
                    except:
                        print('Cannot read transform matrix: {}. Did you download the dataset correctly?'\
                            .format(sequence.link_dict[link_id].filename))
                        exit()

    def set_task(self):
        """
        Deprecated
        """

        for sequence_name in self.sequence_name_list:
            sequence = self.sequences[sequence_name]
            for link_id in sequence.link_id_list:
                this_link = sequence.link_dict[link_id]
                image_a = sequence.image_dict[this_link.source]
                image_b = sequence.image_dict[this_link.target]
                this_link.task['ima'] = str(image_a.idx)
                this_link.task['imb'] = str(image_b.idx)
                
                try:
                    imga_ch = image_a.image_data.shape[2]
                except:
                    imga_ch = 1
                try:
                    imgb_ch = image_b.image_data.shape[2]
                except:
                    imgb_ch = 1

                this_link.task['ima_size'] = [image_a.image_data.shape[0], image_a.image_data.shape[1], imga_ch]
                this_link.task['imb_size'] = [image_b.image_data.shape[0], image_b.image_data.shape[1], imgb_ch]
                this_link.task['H'] = this_link.transform_matrix

                this_link.task['name'] = str(sequence.name)
                this_link.task['description'] = {}
                this_link.task['description']['impair'] = [str(image_a.idx), str(image_b.idx)]
                try:
                    this_link.task['description']['nuisanceName'] = str(sequence.label)
                    this_link.task['description']['nuisanceValue'] = str(imageb.label)
                except:
                    pass


    def get_sequence(self, sequence_name):
        """
        Get a sequence by name.
        
        :param sequence_name: Name of the sequence
        :type sequence_name: str
        :returns: sequence
        :rtype: Sequence
        """

        return self.sequences[sequence_name]

    def get_image(self,sequence_name, image_id):
        """
        Get a image by sequence name and image ID.
        
        :param sequence_name: Name of the sequence
        :type sequence_name: str
        :param image_id: Image ID
        :type image_id: str
        :returns: image
        :rtype: Image
        """

        return self.sequences[sequence_name].image_dict[image_id].image_data

    def get_link(self, sequence_name, link_id):
        """
        Get a link by sequence name and link ID.
        
        :param sequence_name: Name of the sequence
        :type sequence_name: str
        :param link_id: Link ID
        :type link_id: str
        :returns: link
        :rtype: Link
        """

        return self.sequences[sequence_name].link_dict[link_id].transform_matrix
    
    def get_task(self, sequence_name, link_id):
        """
        Get a task by sequence name and link ID.
        
        :param sequence_name: Name of the sequence
        :type sequence_name: str
        :param link_id: Link ID
        :type link_id: str
        :returns: task
        :rtype: dict
        """

        return self.sequences[sequence_name].link_dict[link_id].task

    def __getitem__(self,idx):
        """
        Get a sequence by index.
        
        :param idx: Index of the sequence
        :type idx: int
        :returns: sequence
        :rtype: Sequence
        """

        return self.sequences[self.sequence_name_list[idx]]
    
    @abstractmethod
    def download(self):
        """
        Download data
        """

        pass

    @abstractmethod
    def read_image_data(self):
        """
        Read image data
        """

        pass

    @abstractmethod
    def read_link_data(self):
        """
        Read Link data
        """

        pass
