How to create new feature
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


