function vlb_setup()
%VLB_SETUP Setup the VLB toolbox.
%   VLB_SETUP() function adds the VLB toolbox to MATLAB path.

% Copyright (C) 2014-16 Andrea Vedaldi, Karel Lenc.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

root = vlb_root() ;
addpath(fullfile(root, 'matlab')) ;
addpath(fullfile(root, 'matlab', 'mex')) ;
addpath(fullfile(root, 'examples')) ;
addpath(fullfile(root, 'xtest')) ;
run(fullfile(root, 'vlfeat', 'toolbox', 'vl_setup'));