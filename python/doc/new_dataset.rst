How to Create New Dataset 
=========================================================
To test your own dataset with off-the-shelf detector and descriptor, you need to create your own dataset class.


Image Matching Dataset
----------------------------------------------

To create new image matching dataset like VGG-Affine or HPatches, follow code `dset.vgg_dataset.vgg_Dataset`. There is an download() function helping users to download data from Internet, extract and orgnize the file. read_image_data() defines how to read all the images. And read_link_data() defines how to read link data (relation of image pair). 

Each dataset will have a json file in datasets/dataset_info/. dataset.json defines the general format for the matching dataset. The json file contains name, descriptor of the dataset, url, number of sequence and each sequence. In each sequence, there are the information of each image and each link. dset/write_dataset_vggh.py provides an example of how to using python script to write the json file. 

.. literalinclude:: ../dset/write_dataset_vggh.py


Image Retrieval Dataset
----------------------------------------------

To create new image retrieval dataset like oxford5k or paris6k, follow code `dset.oxford5k_dataset.oxford_Dataset` and `dset.paris6k_dataset.paris6k_Dataset`. There is an download() function helping users to download data from Internet, extract and orgnize the file. read_gallery_list() defines how to read all galary images (world/dataset images). And read_query_list() defines how to read query_image and corresponding ground-truth in the gallery dataset. For the query image, each image name as well as a bounding box associate to the object [filename, left, top, right, bottom] are make an item in the query_list. There is one positive_lists each item is a list of filenames of the ground-truth images of the corresponding query. Also, there is one junk_lists each item is a list of filenames of the opt-out images of the corresponding query.

The json file of the retrieval dataset is pretty simple. See datasets/dataset_info/oxford5k.json. There are only one dataset name, one url and one description. 


Baseline Matching Dataset
----------------------------------------------
It's very similar to Image Matching dataset. See `dset.W1BS_dataset.W1BS_Dataset` and ../dset/write_dataset_W1BS.py. 


