#!/bin/bash

#LF-Net Pretrained Models
curl http://webhome.cs.uvic.ca/~kyi/files/2018/lf-net/pretrained.tar.gz | tar xz -C ./lf_net_misc/

#TF-Lift models
curl http://webhome.cs.uvic.ca/~kyi/files/2018/tflift/release-aug.tar.gz | tar xz -C ./tf-lift/

#SuperPoint
curl https://github.com/MagicLeapResearch/SuperPointPretrainedNetwork/raw/master/superpoint_v1.pth | tar xv -C ./superpoint_misc/


# Download HardNet pretrained model
#cd ./hardnet && { curl -O http://cs.unc.edu/~xufeng/matchnet/models/liberty_r_0.01_m_0.feature_net.pb; cd -;}
