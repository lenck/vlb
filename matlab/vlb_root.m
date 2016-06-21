function root = vlb_root()
%VLB_ROOT Get the root path of the VLB toolbox.
%   VLB_ROOT() returns the path to the VLB toolbox.

% Copyright (C) 2014,2016 Andrea Vedaldi, Karel Lenc.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

root = fileparts(fileparts(mfilename('fullpath'))) ;