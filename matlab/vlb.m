function res = vlb(cmd, varargin)

% Copyright (C) 2016-2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).
vlb_setup();
usage = @(varargin) utls.helpbuilder(varargin{:}, 'name', 'vlb');

cmds = struct();
cmds.view = struct('fun', @vlb_view, 'help', '');
cmds.det = struct('fun', @vlb_det, 'help', '');
cmds.extract = struct('fun', @vlb_extract, 'help', '');
cmds.desc = struct('fun', @vlb_desc, 'help', '');
cmds.detdesc = struct('fun', @vlb_detdesc, 'help', '');
cmds.descmatch = struct('fun', @(varargin) vlb_desceval(varargin{:}, ...
  'benchFun', @bench.descmatch), 'help', '');
cmds.detmatch = struct('fun', @(varargin) vlb_desceval(varargin{:}, ...
  'benchFun', @bench.detmatch), 'help', '');
cmds.detrep = struct('fun', @(varargin) vlb_deteval(varargin{:}, ...
  'benchFun', @bench.detrep), 'help', '');
cmds.detrepthr = struct('fun', @(varargin) vlb_deteval(varargin{:}, ...
  'benchFun', @bench.detrepthr), 'help', '');

% The last command is always help
cmds.help = struct('fun', @(varargin) usage(cmds, '', varargin{:}));
if nargin < 1, cmd = nan; end;
if ~ischar(cmd), usage(cmds, ''); return; end
if strcmp(cmd, 'commands'), res = cmds; return; end;

if isfield(cmds, cmd) && ~isempty(cmds.(cmd).fun)
  if nargout == 1
    res = cmds.(cmd).fun(varargin{:});
  else
    cmds.(cmd).fun(varargin{:});
  end
else
  error('Invalid command. Run help for list of valid commands.');
end

end

