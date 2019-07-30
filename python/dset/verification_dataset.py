""" Dataset based on dataset used in `Learning to Find Good Correspondences`
    https://github.com/vcg-uvic/learned-correspondence-release"""

import os
import pickle
import numpy as np
from bench.geom import get_E_matrix, get_F_matrix, to_pixel_coords, get_inliers_F
dirname = os.path.dirname(os.path.abspath(__file__))

class verification_dataset():

    def __init__(self, data_names=['reichstag','brown_bm_3_05']):
        """Verification dataset

        Attributes
        ----------
        data_names: list
            List of data sets to be used. By default loads 'reichstag' and 'brown_bm_3_05'
            dataset.
        """

        self.name='verification_dset'
        self.data_dump_prefix = os.path.join(dirname,"../../datasets/Verification/data_dump")
        self.data_names = data_names

        self._load_data()
        self.sequences = list(self.data.keys())
        self._prepare_data()


    def _load_data(self, var_mode='test'):

        """Main data loading routine adapted from
        https://github.com/vcg-uvic/learned-correspondence-release

        Loads data defined in @var_name_list from files at @data_dump_prefix and @data_names
        into @self.data

        Attributes
        ----------
        var_mode: str
            what split to us in the dataset. Default is 'test' but 'train' or 'val' can be
            used as well.
        """

        print("Loading {} data".format(var_mode))

        # use only the first two characters for shorter abbrv
        var_mode = var_mode[:2]

        # Now load data.
        var_name_list = [
            "xs", "ys", "Rs", "ts",
            "img1s", "cx1s", "cy1s", "f1s",
            "img2s", "cx2s", "cy2s", "f2s", "k1s", "k2s",
        ]

        data_folder = self.data_dump_prefix

        # Let's unpickle and save data
        data = {}

        for data_name in self.data_names:
            cur_data_folder = "/".join([
                data_folder,
                data_name,
                "numkp-2000",
                "nn-1",
                "nocrop",
            ])


            suffix = "{}-1000".format(var_mode)

            cur_folder = os.path.join(cur_data_folder, suffix)
            ready_file = os.path.join(cur_folder, "ready")
            if not os.path.exists(ready_file):
                # data_gen_lock.unlock()
                raise RuntimeError("Data is not prepared!")

            for var_name in var_name_list:
                cur_var_name = var_name + "_" + var_mode
                in_file_name = os.path.join(cur_folder, cur_var_name) + ".pkl"
                with open(in_file_name, "rb") as ifp:
                    if data_name in data:
                        if var_name in data[data_name]:
                            data[data_name][var_name] += pickle.load(ifp)
                        else:
                            data[data_name][var_name] = pickle.load(ifp)
                    else:
                        data[data_name] = {}
                        data[data_name][var_name] = pickle.load(ifp)

        self.data = data

    def _prepare_data(self):
        """
        Prepares/calculates data from original data. Calculates Essential Matrix (E),
        Fundamental Matrix (F), pixel coordinates, and inlier correspondence pairs.
        """
        for seq in self.sequences:
            d = self.data[seq]

            #define new values
            norm_coords1, norm_coords2 = list(), list()
            px_coords1, px_coords2 = list(), list()
            cam_centers1, cam_centers2 = list(),  list()
            K1s, K2s = list(), list()
            Es, Fs = list(), list()
            inlier_mask = list()

            for idx in range(len(d['xs'])):
                pt1s = d['xs'][idx][0,:,:2]
                pt2s = d['xs'][idx][0,:,2:]
                cam_center1 = np.vstack((d['cx1s'], d['cy1s'])).T[idx]
                cam_center2 = np.vstack((d['cx2s'], d['cy2s'])).T[idx]
                norm_coords1.append(pt1s)
                norm_coords2.append(pt2s)
                cam_centers1.append(cam_center1)
                cam_centers2.append(cam_center2)

                f1 = d['f1s'][idx]
                f2 = d['f2s'][idx]
                K1 = d['k1s'][idx]
                K2 = d['k2s'][idx]
                img1 = d['img1s'][idx]
                img2 = d['img2s'][idx]

                #offset for principal point (origin at top left corner)
                K1[:,2] = np.array([img1.shape[2]/2.0, img1.shape[1]/2.0, 1.0])
                K2[:,2] = np.array([img2.shape[2]/2.0, img2.shape[1]/2.0, 1.0])

                K1s.append(K1)
                K2s.append(K2)

                px1 = to_pixel_coords(K1,pt1s)
                px2 = to_pixel_coords(K2,pt2s)

                px_coords1.append(px1)
                px_coords2.append(px2)

                R = d['Rs'][idx]
                t = d['ts'][idx]
                F = get_F_matrix(R, t, K1, K2)

                _, _, mask = get_inliers_F(px1, px2, F, thresh=1)
                inlier_mask.append(mask)
                Es.append(get_E_matrix(R, t))
                Fs.append(F)

            self.data[seq]['inlier_mask'] = inlier_mask
            self.data[seq]['norm_coords1'] = norm_coords1
            self.data[seq]['norm_coords2'] = norm_coords2

            self.data[seq]['px_coords1'] = px_coords1
            self.data[seq]['px_coords2'] = px_coords2
            self.data[seq]['K1s'] = K1s
            self.data[seq]['K2s'] = K2s
            self.data[seq]['Es'] = Es
            self.data[seq]['Fs'] = Fs

    def get_data(self):
        return self.data

    def get_data_sequence_pair(self, seq, idx):
        """
        Return data for a specific sequence and image pair within the sequence of dataset

        Attributes
        ----------
        seq: str
            A data sequence listed in @self.sequences
        idx: int
            The index of the desired image pair whose data will be returned

        Output
        ------
        data_dict: dict
            dictionary of relevant information for the verification task

            Dict Structure:
                norm_coords1: np.array (Nx2)
                    normalized camera coordinates of the keypoints in image1 of pair @idx
                norm_coords2: np.array (Nx2)
                    normalized camera coordinates of the keypoints in image2 of pair @idx
                px_coords1: np.array (Nx2)
                    pixel coordinates of the keypoints in image1 of pair @idx
                px_coords2: np.array (Nx2)
                    pixel coordinates of the keypoints in image2 of pair @idx
                K1: np.array (3x3)
                    intrinsic calibration matrix of camera from img1
                K2: np.array (3x3)
                    intrinsic calibration matrix of camera of img2
                E: np.array (3x3)
                    Essential matrix between img1 and img2 such that x2.TEx1 = 0
                    where x1 from img1 and x2 from img2
                F: np.array (3x3)
                    Fundamental matrix between img1 and img2 such that x2.TFx1 = 0
                    where x1 from img1 and x2 from img2
                inlier_mask: np.array (Nx1)
                    Array of 1's and 0's where a 1 at index n denotes that
                    the putative correspondence at index n is a true match and 0 not
        """
        return {'norm_coords1' : self.data[seq]['norm_coords1'][idx],
                'norm_coords2' : self.data[seq]['norm_coords2'][idx],
                'px_coords1' : self.data[seq]['px_coords1'][idx],
                'px_coords2' : self.data[seq]['px_coords2'][idx],
                'K1' : self.data[seq]['K1s'][idx],
                'K2' : self.data[seq]['K2s'][idx],
                'E' : self.data[seq]['Es'][idx],
                'F' : self.data[seq]['Fs'][idx],
                'inlier_mask': self.data[seq]['inlier_mask'][idx]}
