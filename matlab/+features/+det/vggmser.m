function [ res ] = vggmser( img, varargin )
%VGG_MSER Detect frames using the MSER detector
%  FRAMES = VGG_MSER(IMG) Computes the MSER features using the
%   implementation by [1].
%
%  Function supports the following options:
%   ES:: [binary default, 1.0]
%     Scale of the ellipse
%
%   PER:: [binary default, 0.01]
%     Maximum relative area
%
%   MS:: [binary default, 30]
%     Minimum size of output region
%
%   MM:: [binary default, 10]
%     Minimum margin
%
%   REFERENCES
%   [1] J. Matas, O. Chum, M. Urban and T. Pajdla. Robust wide-baseline 
%   stereo from maximally stable extremal regions. BMVC, 384-393, 2002.

% Copyright (C) 2011-16 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.es = 1;
opts.per = -1;
opts.ms = -1;
opts.mm = -1;
opts = vl_argparse(opts, varargin);
res.detName = 'vggmser'; res.args = opts;
if isempty(img), res.frames = zeros(5, 0); return; end;

% Constants
BIN_DIR = fullfile(vlb_path('vendor'), 'vgg_mser');
switch(computer)
  case  {'GLNX86','GLNXA64'}
    BIN_PATH = fullfile(BIN_DIR, 'mser.ln');
  case  {'PCWIN','PCWIN64'}
    BIN_PATH = fullfile(BIN_DIR, 'mser.exe');
  otherwise
    error('Unsupported platform.');
end
BIN_URL = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/mser.tar.gz';
% Make sure the detector is present
if ~exist(BIN_PATH, 'file'), untar(BIN_URL, BIN_DIR); end

tmpImgName = [tempname(), '.png'];
if ischar(img) && exist(img, 'file')
  tmpImgName = img;
else
  imwrite(img, tmpImgName);
end

framesFile = [tempname() '.feat'];
args = ' -t 2'; % Define the output type
fields = fieldnames(opts);
for i = 1:numel(fields)
  val = opts.(fields{i});
  if val >= 0, args = [args, ' -', fields{i}, ' ', num2str(val)]; end
end
cmd = sprintf('%s %s -i "%s" -o "%s"', BIN_PATH, args, tmpImgName, framesFile);
[status,msg] = system(cmd);
if status, error('Error running VGG_MSER: %s: %s', cmd, msg) ; end
frames = legacy.vgg_frames_read(framesFile);
if ~strcmp(img, tmpImgName), delete(tmpImgName); end;
delete(framesFile);
res.frames = frames;