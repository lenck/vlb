How to Create New Feature
=========================================================
To test your own detector or descriptor, you need to create your own feature detector or descriptor. 

Any detector or descriptor should be a subclass of :class:`features.DetectorDescriptorTemplate.DetectorAndDescriptor`. Create the py file under features/.

To make it work, you should set proper properties and implement corresponding function of feature detection or/and descriptor extraction. Just implement what your module. For example, if the module is a detector only, just implement detect_feature(). 

Here is an example (features/cyvlsift_official.py):

.. code-block:: python
    class cyvlsift_official(DetectorAndDescriptor):
        #name is the string to identify you detector
        #if the model is a detector, set is_detector to be True
        #if the model is a descriptor, set is_descriptor to be True
        #if the model is a detector and a descriptor, set is_both to be True
        #add addtional parameter
        def __init__(self, peak_thresh=0.0):
            super(
                cyvlsift_official,
                self).__init__(
                name='cyvlsift_official',
                is_detector=True,
                is_descriptor=True,
                is_both=True)
            self.peak_thresh = peak_thresh

        #Given an image return a n*d feature array
        def detect_feature(self, image):
        
        #Given an image and an array of feature, return a n*d' descriptor array
        def extract_descriptor(self, image):
        
        #Given an image return a n*d feature array and a n*d' descriptor array
        def extract_all(self, image):
        
:class:`features.DetectorDescriptorTemplate.DetectorDescriptorBundle` helps bundle a feature detecor and a feature extractor. For example, you can bundle the DOG detector with your own descriptor and vice versa. 

.. code-block:: python
    DetectorDescriptorBundle(detector, descriptor):

Full code:

.. literalinclude:: ../features/cyvlsift_official.py


Load Precomputed Feature
--------------------------------------------------
Similar to the previous example. Set csv_flag = True and don't need to implement any function here. 

.. code-block:: python
    class vlsift_load_matlab(DetectorAndDescriptor):
    def __init__(self, csv_flag=True):
        super(
            vlsift_load_matlab,
            self).__init__(
            name='vlsift_load_matlab',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            csv_flag=csv_flag)

    def detect_feature(self, image):
        pass

    def extract_descriptor(self, image, feature):
        pass

    def extract_all(self, image):
        pass

Store feature file and descriptor file to ./data/features/$dataset_name/$feature_name. The feature file is a csv file with name $sequence-$imageid.frames.csv. In the file, there are N features. Each in one line of d dims seperated by ";". 

4.5111;501.33;1.768;-1.8145

The descriptor csv file has a name of $sequence-$imageid.descs.csv. The file contains N lines, each line is a descripor cossponding to the feature seperated by ";".

An example can be find `here <https://drive.google.com/open?id=1-D_v1LV64FPQf1Kb9RXQYa9zvYzHvtTu>`_ . Download the file and extract to ./data/features/vggh/. Then you can use the detector and descriptor "vlsift_load_matlab". 

There is the full code:

.. literalinclude:: ../features/vlsift_load_matlab.py
