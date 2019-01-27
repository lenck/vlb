import numpy as np
import json
import os
import cv2
from abc import ABCMeta, abstractmethod

import scipy.ndimage
#import matlab

class Image:
    idx = ''
    image_data = None
    label = ''
    filename = ''

class Link:
    source = ''
    target = ''
    filename = ''
    transform_matrix = None
    matlab_task = {}

class Sequence:
    name = ''
    description = ''
    image_id_list = None
    image_dict = None # list cannot be initialized here!
    link_id_list = None
    link_dict = None
    
    def images(self):
        return self.image_dict.iteritems()

    def links(self):
        return self.link_dict.iteritems()

class SequenceDataset():
    __metaclass__ = ABCMeta 
    def __init__(self, name, root_dir = './datasets/', download_flag = False, matlab_flag = False):
        self.name = name
        self.root_dir = root_dir
        self.load_dataset_info()
        #print(self.sequence_name_list)
        
        if download_flag:
            self.download()

        try:
            os.stat(root_dir + self.name + '/')
        except:
            self.download()

        self.read_image_data()
        self.read_link_data()
        #need matlab warpper at this point
        self.matlab_flag = matlab_flag
        if matlab_flag:
            self.set_matlab_task()

    def load_dataset_info(self):
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

                this_link.matlab_task = {}
                
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

    def set_matlab_task(self):
        for sequence_name in self.sequence_name_list:
            sequence = self.sequences[sequence_name]
            for link_id in sequence.link_id_list:
                this_link = sequence.link_dict[link_id]
                image_a = sequence.image_dict[this_link.source]
                image_b = sequence.image_dict[this_link.target]
                this_link.matlab_task['ima'] = str(image_a.idx)
                this_link.matlab_task['imb'] = str(image_b.idx)
                
                try:
                    imga_ch = image_a.image_data.shape[2]
                except:
                    imga_ch = 1
                try:
                    imgb_ch = image_b.image_data.shape[2]
                except:
                    imgb_ch = 1

                #this_link.matlab_task['ima_size'] = matlab.double([image_a.image_data.shape[0], image_a.image_data.shape[1], imga_ch])
                #this_link.matlab_task['imb_size'] = matlab.double([image_b.image_data.shape[0], image_b.image_data.shape[1], imgb_ch])
                #this_link.matlab_task['H'] = matlab.double(this_link.transform_matrix.tolist())
                this_link.matlab_task['ima_size'] = [image_a.image_data.shape[0], image_a.image_data.shape[1], imga_ch]
                this_link.matlab_task['imb_size'] = [image_b.image_data.shape[0], image_b.image_data.shape[1], imgb_ch]
                this_link.matlab_task['H'] = this_link.transform_matrix

                this_link.matlab_task['name'] = str(sequence.name)
                this_link.matlab_task['description'] = {}
                this_link.matlab_task['description']['impair'] = [str(image_a.idx), str(image_b.idx)]
                try:
                    this_link.matlab_task['description']['nuisanceName'] = str(sequence.label)
                    this_link.matlab_task['description']['nuisanceValue'] = str(imageb.label)
                except:
                    pass


    def get_sequence(self, sequence_name):
        return self.sequences[sequence_name]

    def get_image(self,sequence_name, image_id):
        return self.sequences[sequence_name].image_dict[image_id].image_data

    def get_link(self, sequence_name, link_id):
        return self.sequences[sequence_name].link_dict[link_id].transform_matrix
    
    def get_matlab_task(self, sequence_name, link_id):
        return self.sequences[sequence_name].link_dict[link_id].matlab_task

    def __getitem__(self,i):
        return self.sequences[self.sequence_name_list[i]]
    
    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def read_image_data(self):
        pass

    @abstractmethod
    def read_link_data(self):
        pass
