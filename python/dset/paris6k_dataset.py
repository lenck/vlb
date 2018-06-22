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

class paris6k_Dataset(RetrievalDataset):

    def __init__(self, root_dir = './datasets/', download_flag = False):
        super(paris6k_Dataset,self).__init__(name = 'paris6k', root_dir = root_dir, download_flag = download_flag)

    def download(self):
        try:
            os.stat(self.root_dir)
        except:
            os.mkdir(self.root_dir)

        try:
            os.stat('{}{}'.format(self.root_dir,self.name))
        except:
            os.mkdir('{}{}'.format(self.root_dir,self.name))

        print("Download Paris6K")
        download_url_1 = "{}{}.tgz".format(self.url, 'paris_1')
        download_url_2 = "{}{}.tgz".format(self.url, 'paris_2')
        download_gt_url = "{}{}.tgz".format(self.url, 'paris_120310')
        download_filename_1 = "{}{}/{}.tgz".format(self.root_dir, self.name, 'paris_1')
        download_filename_2 = "{}{}/{}.tgz".format(self.root_dir, self.name, 'paris_2')
        download_gt_filename = "{}{}/{}.tgz".format(self.root_dir, self.name, 'paris_120310')
        try:
            os.stat('{}{}'.format(self.root_dir,self.name))
        except:
            os.mkdir('{}{}'.format(self.root_dir,self.name))

        try:
            urlretrieve(download_url_1, download_filename_1)
            tar = tarfile.open(download_filename_1)
            tar.extractall('{}{}/'.format(self.root_dir,self.name))
            tar.close()
            os.remove(download_filename_1)

            urlretrieve(download_url_2, download_filename_2)
            tar = tarfile.open(download_filename_2)
            tar.extractall('{}{}/'.format(self.root_dir,self.name))
            tar.close()
            os.remove(download_filename_2)

            urlretrieve(download_gt_url, download_gt_filename)
            tar = tarfile.open(download_gt_filename)
            tar.extractall('{}{}/gt/'.format(self.root_dir,self.name))
            tar.close()
            os.remove(download_gt_filename)
        except:
            print('Cannot download from {}.'.format(self.url))

    def read_gallery_list(self):
        self.gallery_list = []
        for directory in glob('{}{}/paris/*'.format(self.root_dir,self.name)):
            if os.path.isdir(directory):
                self.gallery_list.extend(glob('{}/*.jpg'.format(directory)))
        print(len(self.gallery_list))

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
                    filename = filename + '.jpg'
                    self.query_list.append([filename, left, top, right, bottom])
            #remove _query.txt
            query_txt = query_txt[:-10]
            #find positive image set
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
            #find junk image set
            junk_txt = query_txt + '_junk.txt'
            junk_list = []
            with open(junk_txt, 'r') as fp:
                for line in fp:
                    line = line[:-1]
                    junk_list.append(line+'.jpg')
            self.junk_lists.append(junk_list)

    
if __name__ == "__main__":
    a = paris6k_Dataset(download_flag = True)

