function root = vlb_path(set, imdb, featsname, benchname)
%VLB_ROOT Get the root path of the VLB toolbox.
%   VLB_ROOT() returns the path to the VLB toolbox.

% Copyright (C) 2017 Karel Lenc.
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

root = fileparts(fileparts(mfilename('fullpath'))) ;
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
      root = fullfile(root, 'data', set, imdb_name, featsname);
    case 'scores'
      assert(nargin == 4, 'Invalid input (imdb, feats, bench)');
      root = fullfile(root, 'data', 'scores', benchname, imdb_name, featsname);
    otherwise
      error('Invalid set %s.', set);
  end
end