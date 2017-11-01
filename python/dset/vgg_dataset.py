from dataset import SequenceDataset
import urllib
import tarfile
import os


class vggh_Dataset(SequenceDataset):

    def __init__(self,root_dir = './datasets/', download_flag = False):
        super(vggh_Dataset,self).__init__(name = 'vggh', root_dir = root_dir, download_flag = download_flag)

    def download(self):
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
                urllib.urlretrieve(download_url,download_filename)
                tar = tarfile.open(download_filename)
                tar.extractall('{}{}/{}'.format(self.root_dir,self.name,sequence_name))
                tar.close()
                os.remove(download_filename)
            except:
                print('Cannot download from {}.'.format(download_url))
    
    def read_image_data(self):
        self.read_image_data_vggh()

    def read_link_data(self):
        self.read_link_data_vggh()

if __name__ == "__main__":

    a = vggh_Dataset()
    
