function root = vlb_path(set, imdb, featsname, benchname)
%VLB_ROOT Get the root path of the VLB toolbox.
%   VLB_ROOT() returns the path to the VLB toolbox.
%
%   Otherwise can return paths to particular data locations of the VLB. In
%   all cases, several specifiers are required:
%     IMDBNM:  structure or a string, specifying the image database
%     FEATSNM: structure or a string, specifying the local features
%     FEATSNM: string, specifying the benchmark

%   To access the benchmark data and results one can call:
%   VLB_ROOT('features', IMDBNM, FEATSNM) returns features path
%   VLB_ROOT('patches', IMDBNM, FEATSNM) returns patches path
%   VLB_ROOT('results', IMDBNM, FEATSNM, BENCHNM) returns patches path
%
%   By default, all data are stored in a path relative to the location of
%   this script. This can be overriden with an environment variable
%   VLB_DATAROOT.
%
%   Additionally one can acces:
%   VLB_ROOT('datasets') returns the image database path
%   VLB_ROOT('vendor') returns the third party library path.


% Copyright (C) 2017 Karel Lenc.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

env_root = getenv('VLB_ROOT');
if ~isempty(env_root)
  root = strtrim(env_root);
else
  root = fileparts(fileparts(mfilename('fullpath'))) ;
end

% Allow to store data per project with a environment variable
env_scoresroot = getenv('VLB_DATAROOT');
if ~isempty(env_scoresroot)
  dataroot = strtrim(env_scoresroot);
else
  dataroot = fullfile(root, 'data');
end

if nargin > 0
  if nargin > 1
    assert(isstruct(imdb) && isfield(imdb, 'name'), 'Invalid imdb');
    imdb_name = imdb.name;
  end
  if nargin > 2
    switch class(featsname)
      case 'struct'
        featsname = featsname.name;
      case 'cell'
        featsname = fullfile(featsname{:});
      case 'char'
      otherwise
        error('Invalid featsname');
    end
  end
  if nargin > 3
    assert(ischar(benchname), 'Invalid benchmark name.');
  end
  switch set
    case {'features', 'patches'}
      assert(nargin == 3, 'Invalid args (imdb, feats)');
      root = fullfile(dataroot, set, imdb_name, featsname);
    case 'scores'
      assert(nargin == 4, 'Invalid input (imdb, feats, bench)');
      root = fullfile(dataroot, 'scores', benchname, imdb_name, featsname);
    case 'datasets'
      assert(nargin == 1, 'Too many args for datasets');
      root = fullfile(root, 'datasets');
    case 'vendor'
      assert(nargin == 1, 'Too many args for vendor');
      root = fullfile(root, 'vendor');
    case 'imagelists'
      assert(nargin == 1, 'Too many args for vendor');
      root = fullfile(dataroot, 'imagelists');
    otherwise
      error('Invalid set %s.', set);
  end
end