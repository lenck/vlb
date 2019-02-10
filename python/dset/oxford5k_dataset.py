from retrieval_dataset import RetrievalDataset
import urllib
import tarfile
import os
import sys

from glob import glob
if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

class oxford5k_Dataset(RetrievalDataset):

    def __init__(self, root_dir = './datasets/', download_flag = False):
        super(oxford5k_Dataset,self).__init__(name = 'oxford5k', root_dir = root_dir, download_flag = download_flag)

    def download(self):
        try:
            os.stat(self.root_dir)
        except:
            os.mkdir(self.root_dir)

        try:
            os.stat('{}{}'.format(self.root_dir,self.name))
        except:
            os.mkdir('{}{}'.format(self.root_dir,self.name))

        print("Download Oxford5K")
        download_url = "{}{}.tgz".format(self.url, 'oxbuild_images')
        download_gt_url = "{}{}.tgz".format(self.url, 'gt_files_170407')
        download_filename = "{}{}/{}.tgz".format(self.root_dir, self.name, 'oxbuild_images')
        download_gt_filename = "{}{}/{}.tgz".format(self.root_dir, self.name, 'gt_files_170407')
        try:
            os.stat('{}{}'.format(self.root_dir,self.name))
        except:
            os.mkdir('{}{}'.format(self.root_dir,self.name))

        try:
            urlretrieve(download_url, download_filename)
            tar = tarfile.open(download_filename)
            tar.extractall('{}{}/images/'.format(self.root_dir,self.name))
            tar.close()
            os.remove(download_filename)

            urlretrieve(download_gt_url, download_gt_filename)
            tar = tarfile.open(download_gt_filename)
            tar.extractall('{}{}/gt/'.format(self.root_dir,self.name))
            tar.close()
            os.remove(download_gt_filename)
        except:
            print('Cannot download from {}.'.format(self.url))

    def read_gallery_list(self):
        self.gallery_list = glob('{}{}/images/*.jpg'.format(self.root_dir,self.name))

    def read_query_list(self):
        query_txt_list = glob('{}{}/gt/*query.txt'.format(self.root_dir,self.name))
        self.query_list = []
        self.positive_lists = []
        self.junk_lists = []
        for query_txt in query_txt_list:
            with open(query_txt, 'r') as fp:
                for line in fp:
                    filename, left, top, right, bottom = line.split(' ')
                    left = float(left)
                    top = float(top)
                    right = float(right)
                    bottom = float(bottom)
                    filename = filename[5:] + '.jpg'
                    self.query_list.append([filename, left, top, right, bottom])
            query_txt = query_txt[:-10]
            pos_txt = query_txt + '_good.txt'
            pos_list = []
            with open(pos_txt, 'r') as fp:
                for line in fp:
                    line = line[:-1]
                    pos_list.append(line+'.jpg')
            ok_txt = query_txt + '_ok.txt'
            with open(ok_txt, 'r') as fp:
                for line in fp:
                    line = line[:-1]
                    pos_list.append(line+'.jpg')
            self.positive_lists.append(pos_list) 
            junk_txt = query_txt + '_junk.txt'
            junk_list = []
            with open(junk_txt, 'r') as fp:
                for line in fp:
                    line = line[:-1]
                    junk_list.append(line+'.jpg')
            self.junk_lists.append(junk_list)

    
if __name__ == "__main__":
    a = oxford5k_Dataset(download_flag = True)

