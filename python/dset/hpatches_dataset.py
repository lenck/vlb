from dataset import SequenceDataset
import urllib
import tarfile
import os
import sys

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


class HPatches_Dataset(SequenceDataset):

    def __init__(self,root_dir = './datasets/', download_flag = False):
        super(HPatches_Dataset,self).__init__(name = 'HPatches', root_dir = root_dir, download_flag = download_flag)

    def download(self):
        try:
            os.stat(self.root_dir)
        except:
            os.mkdir(self.root_dir)

        try:
            os.stat('{}{}'.format(self.root_dir,self.name))
        except:
            os.mkdir('{}{}'.format(self.root_dir,self.name))

        download_url = "{}".format(self.url)
        download_filename = "{}{}/{}.tar.gz".format(self.root_dir, self.name, self.name)
        try:
            urlretrieve(download_url,download_filename)
            tar = tarfile.open(download_filename)
            tar.extractall('{}'.format(self.root_dir))
            tar.close()
            os.remove(download_filename)
        except Exception as e:
            print(str(e))
            print('Cannot download from {}.'.format(download_url))

    def read_image_data(self):
        self.read_image_data_vggh()

    def read_link_data(self):
        self.read_link_data_vggh()
