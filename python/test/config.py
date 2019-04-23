import os
import sys
cwd = os.getcwd()
sys.path.insert(0, '{}/python/'.format(cwd))

import features.cyvlsift_official
import features.cv_orb
import features.cv_mser
import features.cv_brisk
import features.cv_fast
import features.cv_akaze
import features.cv_kaze
import features.superpoint
import features.lf_net
from importlib import import_module



what_models_to_test = {
    'superpoint': {
        'class':'SuperPoint',
        'test':False
        },
    'cyvlsift_official':{
        'class':'cyvlsift_official',
        'test':False},
    'cv_orb':{
        'class':'cv_orb',
        'test':False},
    'cv_mser':{
        'class':'cv_mser',
        'test':False},
    'cv_brisk':{
        'class':'cv_brisk',
        'test':False},
    'cv_fast':{
        'class':'cv_fast',
        'test':False},
    'cv_akaze':{
        'class':'cv_akaze',
        'test':False},
    'cv_kaze':  {
        'class':'cv_kaze',
        'test':False},
    'lf_net':  {
        'class':'LFNet',
        'test':True}}


models_to_test = list()

for model, conf in what_models_to_test.items():
    if conf['test']:
        mod = import_module(f"features.{model}")
        cl = getattr(mod, conf['class'])
        models_to_test.append((model, cl()))
