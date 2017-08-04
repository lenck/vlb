function [ frames, info ] = vggaff( img, varargin )
%VGG_AFF Detect frames using VGG Affine co-variant detector
%  FRAMES = VGG_AFF(IMG) Detects FRAMES from image IMG.
%  Only supported architectures are GLNX86 and GLNXA64 as for these the
%  binaries are avaialable.
%
% Function takes the following options:
%   Detector:: 'hesaff'
%     One of {'hesaff', 'haraff', 'heslap', 'harlap','har'} which are
%     supported by the binary.
%
%   Threshold:: -1
%     If specified, passes a threshold option to the binary.

% Copyright (C) 2011-16 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.detector = 'hesaff';
opts.threshold = -1;
opts = vl_argparse(opts, varargin);
info.name = sprintf('vggaff-%s', opts.detector);
if isempty(img), frames = zeros(5, 0); return; end;

% Constants
VALID_DETECTORS = {'hesaff', 'haraff', 'heslap', 'harlap', 'har'};
BIN_DIR = fullfile(vlb_path(), 'data','vgg_aff');
BIN_PATH = fullfile(BIN_DIR, 'h_affine.ln');
BIN_URL = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/h_affine.ln.gz';

% Make sure the detector is present
if ~exist(BIN_PATH, 'file')
  vl_xmkdir(BIN_DIR);
  utls.ungzip(BIN_URL, BIN_DIR);
  system(sprintf('chmod +x %s', BIN_PATH));
end
assert(ismember(computer, {'GLNXA64', 'GLNX86'}), 'Unsupported platform');
assert(ismember(opts.detector, VALID_DETECTORS), 'Invalid detector');

% Write the input image
tmpImgName = [tempname(), '.png'];
if ischar(img) && exist(img, 'file'), img = imread(img); end;
imwrite(img, tmpImgName);

framesFile = [tempname() '.' opts.detector];
thr = '';
if opts.threshold >= 0, thr = sprintf('-thres %f', opts.threshold); end
detCmd = sprintf('%s %s -%s -i "%s" -o "%s" %s', BIN_PATH, thr, ...
  opts.detector, tmpImgName, framesFile);
[status, msg] = system(detCmd);
if status
  error('Error: %d: %s: %s', status, detCmd, msg) ;
end
frames = legacy.vgg_frames_read(framesFile);
if strcmp(opts.detector, 'har'), frames([3, 5], :) = 3.5^2; end
delete(framesFile); delete(tmpImgName);
