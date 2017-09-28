function vlb_setup()
%VLB_SETUP Setup the VLB toolbox.
%   VLB_SETUP() function adds the VLB toolbox to MATLAB path.

% Copyright (C) 2014-16 Andrea Vedaldi, Karel Lenc.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

root = vlb_path() ;
pathCell = regexp(path, pathsep, 'split');
check_and_add(fullfile(root, 'matlab'), pathCell)
check_and_add(fullfile(root, 'matlab', 'mex'), pathCell)
check_and_add(fullfile(root, 'examples'), pathCell)
check_and_add(fullfile(root, 'matlab', 'xtest'), pathCell)
utls.setup_vlfeat();
end

function check_and_add(add_folder,all_path)
    if ispc  % Windows is not case-sensitive
        onPath = any(strcmpi(add_folder, all_path));
    else
        onPath = any(strcmp(add_folder, all_path));
    end
    
    if ~onPath
        addpath(add_folder);
    end
end
