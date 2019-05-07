import sys
import cv2
import os, sys
import math
import numpy as np
import lutorpy as lua
import scipy.io as sio
import torch

class deepdesc(DetectorAndDescriptor):
    def __init__(self):
        super(
            deepdesc,
            self).__init__(
                name='deepdesc',
                is_detector=False,
                is_descriptor=True,
                is_both=False,
                patch_input=True)

    """
    Wrapper to Torch for loading models
    """
    # TODO: check codes for a bigger batch size.
    # Now it only works with size of one.
    batch_sz = 10000
    # TFeat number of input channels
    input_channels = 1
    # TFeat image input size
    input_sz = 64
    # TFeat descriptor size
    descriptor_sz = 128
    mean_val = 1
    std = 1

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    self.net = torch.load(model_file, map_location=device)
    self.ones_arr = np.ones((self.input_sz, self.input_sz), dtype=np.uint8)

    def extract_descriptor(self, image, feature):
        """
        Extract descriptor from image with feature.

        :param image: The image
        :type image: array
        :param feature: The feature output by detector
        :type feature: array
        :returns: descriptor
        :rtype: array(n*d)
        """
        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = features.feature_utils.all_to_gray(new_image)
        feature, descriptor = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, frames=feature, magnification=5.0, compute_descriptor=True)
        return descriptor
    
    def rectify_patch(self, img, kp, patch_sz):
        """
        Extract and rectifies the patch from the original image given a keyopint

        :param img: The input image
        :param kp: The OpenCV keypoint object
        :param patch_sz: The size of the patch to extract

        :return rot: The rectified patch
        """
        # TODO: check this routine since it does not work at all

        scale = 1.0 * float(kp.size) / float(patch_sz)

        c = 1.0 if (kp.angle < 0) else np.cos(kp.angle)
        s = 0.0 if (kp.angle < 0) else np.sin(kp.angle)

        M = np.array([[scale*c, -scale*s, (-scale*c + scale*s) * patch_sz/2.0 + kp.pt[0]],
                      [scale*s,  scale*c, (-scale*s - scale*c) * patch_sz/2.0 + kp.pt[1]]])

        rot = cv2.warpAffine(img, np.float32(M), (patch_sz, patch_sz), \
              flags = cv2.WARP_INVERSE_MAP + cv2.INTER_CUBIC) #+ cv2.WARP_FILL_OUTLIERS

        return rot

    def extract_patches(self, img, kpts):
        """
        Extract the patches and subtract the mean

        :param img: The input image
        :param kpts: The set of OpenCV keypoint objects

        :return: An array with the patches with zero mean
        """
        patches = []
        for kp in kpts:
            # extract patch
            # sub = cv2.getRectSubPix(img, (int(kp.size*1.3), int(kp.size*1.3)), kp.pt)
            sub = self.rectify_patch(img, kp, self.input_sz)

            # resize the patch
            res = cv2.resize(sub, (self.input_sz, self.input_sz))
            # subtract mean
            nmean = res - (self.ones_arr * self.mean_val)
            nmean = nmean/self.std
            nmean = nmean.reshape(self.input_channels, self.input_sz, self.input_sz)
            patches.append(nmean)

        return np.asarray(patches)

    def compute(self, img, kpts):
        """
        Compute the descriptors given a set of keypoints

        :param img: The input image
        :param kpts: The set of OpenCV keypoint objects

        :return: An array the descriptors
        """
        # number of keypoints
        N = len(kpts)
        # extract the patches given the keypoints
        patches = self.extract_patches(img, kpts)


        # convert numpy array to torch tensor
        patches_t = torch.fromNumpyArray(patches)
        patches_t._view(N, self.input_channels, self.input_sz, self.input_sz)

        # split patches into batches
        patches_t   = patches_t._split(self.batch_sz)
        descriptors = []

        for i in range(int(np.ceil(float(N) / self.batch_sz))):
           # infere Torch network
            prediction_t = self.net._forward(patches_t[i]._cuda())

           # Cast TorchTensor to NumpyArray and append to results
            prediction = prediction_t.asNumpyArray()

           # add the current prediction to the buffer
            descriptors.append(prediction)

        return np.float32(np.asarray(descriptors).reshape(N, self.descriptor_sz))


def main():

    # create CNN descriptor
    torch_file = './models/CNN3_p8_n8_split4_073000_model_only.t7'
    net = LutorpyNet(torch_file)
    maxsize = 1024*768

        if img.shape[0]*img.shape[1]>maxsize:
            real_height = int(math.sqrt(float(maxsize)/(img.shape[1]*img.shape[0]))*img.shape[0])
            real_width = int(math.sqrt(float(maxsize)/(img.shape[1]*img.shape[0]))*img.shape[1])
            dst_img = np.zeros((real_height,real_width,3), np.uint8)
            dst_img = cv2.resize(img,(real_width,real_height))
            img = dst_img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # # find the keypoints and the descriptors
        features = net.compute(gray, kp_list)

if __name__ == '__main__':

    main()
