function [res, info] = vlb(cmd, varargin)
%VLB VLBenchmarks command line interface
%  `VLB help`
%     Print this help string.
%  `VLB help COMMAND`
%     Print a help string for a COMMAND.
%   
%  `VLB view` Various visualisations
%  `VLB imagelist` Create image list and feature list
%
%  `VLB detect`
%  `VLB extract`
%  `VLB describe`
%
%  `VLB detrep`
%  `VLB detmatch`
%  `VLB descmatch`



% Copyright (C) 2016-2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).
vlb_setup();
usage = @(varargin) utls.helpbuilder(varargin{:}, 'name', 'vlb');

cmds = struct();
cmds.view = struct('fun', @vlb_view, 'help', '');
cmds.imagelist = struct('fun', @vlb_imagelist, 'help', '');
% Generate features
cmds.detect = struct('fun', @vlb_detect, 'help', '');
cmds.extract = struct('fun', @vlb_extract, 'help', '');
cmds.describe = struct('fun', @vlb_describe, 'help', '');
% Benchmarks
cmds.detrep = struct('fun', ...
  @(varargin) vlb_evalfeatures(@bench.detrep, varargin{:}), ...
  'help', @(a) fprintf(['VLB DETREP Evaluate detector repeatability.\n',...
  '   VLB DETREP imdb featsname\n\n']));
cmds.detrepthr = struct('fun', ...
  @(varargin) vlb_evalfeatures(@bench.detrepthr, varargin{:}), ...
  'help', @(a) fprintf(['VLB DETREPTHR Evaluate detector repeatability over all thresholds.\n',...
  '   VLB DETREPTHR imdb featsname\n\n']));
cmds.detmatch = struct('fun', ...
  @(varargin) vlb_evalfeatures(@bench.detmatch, varargin{:}), ...
  'help', @(a) fprintf(['VLB DETMATCH Evaluate detector matching score.\n',...
  '   VLB DETMATCH imdb featsname\n\n']));
cmds.descmatch = struct('fun', ...
  @(varargin) vlb_evalfeatures(@bench.descmatch, varargin{:}), ...
  'help', @(a) fprintf(['VLB DESCMATCH Evaluate descriptor matching score.\n',...
  '   VLB DESCMATCH imdb featsname\n\n']));

% The last command is always help
if isempty(varargin), varargin = {''}; end
cmds.help = struct('fun', @(varargin) usage(cmds, varargin{:}));

if nargin < 1, cmd = nan; end
if ~ischar(cmd), usage(cmds, ''); return; end
if strcmp(cmd, 'commands'), res = cmds; return; end;

if isfield(cmds, cmd) && ~isempty(cmds.(cmd).fun)
  if nargout == 1
    res = cmds.(cmd).fun(varargin{:});
  elseif nargout == 2
    [res, info] = cmds.(cmd).fun(varargin{:});
  else
    cmds.(cmd).fun(varargin{:});
  end
else
  error('Invalid command. Run help for list of valid commands.');
end

end

