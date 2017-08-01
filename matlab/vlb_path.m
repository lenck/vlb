function root = vlb_path(set, varargin)
%VLB_ROOT Get the root path of the VLB toolbox.
%   VLB_ROOT() returns the path to the VLB toolbox.

% Copyright (C) 2014,2017 Andrea Vedaldi, Karel Lenc.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

root = fileparts(fileparts(mfilename('fullpath'))) ;
if nargin > 0
  switch set
    case 'dets'
      assert(numel(varargin) == 2, 'Invalid args (imdb, det)');
      names = cellfun(@(a) a.name, varargin, 'Uni', false);
      root = fullfile(root, 'data', 'dets', names{:});
    case 'descs'
      assert(numel(varargin) == 3, 'Invalid args (imdb, det, desc)');
      names = cellfun(@(a) a.name, varargin, 'Uni', false);
      root = fullfile(root, 'data', 'descs', names{:});
    case 'patches'
      assert(numel(varargin) == 2, 'Invalid input (imdb, det)');
      names = cellfun(@(a) a.name, varargin, 'Uni', false);
      root = fullfile(root, 'data', 'patches', names{:});
    case 'scores'
      assert(numel(varargin) == 4 || numel(varargin) == 3, ...
        'Invalid input (bench, imdb, det, desc) | (bench, imdb, det)');
      names = cellfun(@(a) a.name, varargin, 'Uni', false);
      root = fullfile(root, 'data', 'scores', names{:});
    otherwise
      error('Invalid set %s.', set);
  end
end