""" Dataset based on dataset used in `Learning to Find Good Correspondences`
    https://github.com/vcg-uvic/learned-correspondence-release"""

import os
import pickle
import numpy as np
from ..verifiers.geom import get_E_matrix, get_F_matrix, to_pixel_coords
dirname = os.path.dirname(os.path.abspath(__file__))

class verification_dataset():

    def __init__(self, data_names=['reichstag','brown_bm_3_05']):

        self.name='verification_dset'
        self.data_dump_prefix = os.path.join(dirname,"../../datasets/Verification/data_dump")
        self.data_names = data_names

        self._load_data()
        self.sequences = list(self.data.keys())
        self._prepare_data()


    def _load_data(self, var_mode='test'):

        """Main data loading routine adapted from
        https://github.com/vcg-uvic/learned-correspondence-release"""

        print("Loading {} data".format(var_mode))

        # use only the first two characters for shorter abbrv
        var_mode = var_mode[:2]

        # Now load data.
        var_name_list = [
            "xs", "ys", "Rs", "ts",
            "img1s", "cx1s", "cy1s", "f1s",
            "img2s", "cx2s", "cy2s", "f2s",
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
        for seq in self.sequences:
            d = self.data[seq]

            #define new values
            norm_coords1 = list()
            norm_coords2 = list()
            px_coords1 = list()
            px_coords2 = list()
            cam_centers1 = list()
            cam_centers2 = list()
            K1s = list()
            K2s = list()
            Es = list()
            Fs = list()

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

                if isinstance(f1, tuple):
                    K1 = np.diag(np.array([f1[0], f1[1], 1]))
                    K1s.append(K2)
                else:
                    K1 = np.diag(np.array([f1, f1, 1]))
                    K1s.append(K1)
                if isinstance(f2, tuple):
                    K2 = np.diag(np.array([f2[0], f2[1], 1]))
                    K2s.append(K2)
                else:
                    K2 = np.diag(np.array([f2, f2, 1]))
                    K2s.append(K2)

                px_coords1.append(to_pixel_coords(K1,pt1s)+cam_center1)
                px_coords2.append(to_pixel_coords(K2,pt2s)+cam_center2)

                R = d['Rs'][idx]
                t = d['ts'][idx]
                Es.append(get_E_matrix(R, t))
                Fs.append(get_F_matrix(R, t, K1, K2))

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
        return {'norm_coords1' : self.data[seq]['norm_coords1'][idx],
                'norm_coords2' : self.data[seq]['norm_coords2'][idx],
                'px_coords1' : self.data[seq]['px_coords1'][idx],
                'px_coords2' : self.data[seq]['px_coords2'][idx],
                'K1s' : self.data[seq]['K1s'][idx],
                'K2s' : self.data[seq]['K2s'][idx],
                'Es' : self.data[seq]['Es'][idx],
                'Fs' : self.data[seq]['Fs'][idx]}
