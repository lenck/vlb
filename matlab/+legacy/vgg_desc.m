function [ frames, descs ] = vgg_desc( img, frames, varargin )
%VGG_DESC Describe frames using the VGG binary
%   [FRAMES, DESCS] = VGG_DESC(IMG, FRAMES) computes the descriptors DESCS
%   of frames FRAMES on image IMG.
%
%   This version of VGG descriptor calculation internaly compute with 
%   magnification factor equal 3 and cannot be adjusted in the binary
%   parameters. Therefore these parameters are 'simulated' in this wrapper.
%
%   Only supported architectures are GLNX86 and GLNXA64 as for these the
%   binaries are avaialable.
%
%  Function supports the following options:
%   Descriptor:: 'sift'
%     One of {'sift','jla','gloh','mom','koen','kf','sc','spin','pca','cc'}.
%     See help string of the binary in
%     ./data/software/VggDescriptor/compute_descriptors.ln
%
%   NoAngle:: false
%     Compute rotation variant descriptors if true (no rotation esimation)
%
%   Magnification:: 3
%     Magnification of the measurement region for the descriptor
%     calculation.
%
%   CropFrames :: true
%     Crop frames which after magnification overlap the image borders.

% Copyright (C) 2011-16 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.noAngle = false;
opts.descriptor = 'sift';
opts.magnification = 3;
opts.cropFrames = true;
opts = vl_argparse(opts, varargin);

% Constants
VALID_DESCRIPTORS = {'sift', 'jla', 'gloh', 'mom', 'koen', 'cf', 'sc', ...
  'spin', 'pca', 'cc'};
BIN_DIR = fullfile(vlb_path(), 'data','vgg_desc');
BIN_PATH = fullfile(BIN_DIR, 'compute_descriptors.ln');
BIN_URL = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/compute_descriptors.ln.gz';
BUILTIN_MAGNIF = 3;

% Make sure the detector is present
if ~exist(BIN_PATH, 'file')
  vl_xmkdir(BIN_DIR);
  utls.ungzip(BIN_URL, BIN_DIR);
  system(sprintf('chmod +x %s', BIN_PATH));
end
assert(ismember(computer, {'GLNXA64', 'GLNX86'}), 'Unsupported platform');
assert(ismember(opts.descriptor, VALID_DESCRIPTORS), 'Invalid detector');

% Write the input image
tmpImgPath = [tempname(), '.png'];
if ischar(img) && exist(img, 'file'), img = imread(img); end;
imwrite(img, tmpImgPath);

frames = utls.frame2ellipse(frames);
if opts.cropFrames
  imgbox = [1 1 size(img, 2)+1 size(img, 1)+1];
  magFrames = [frames(1:2, :) ; frames(3:5, :) .* opts.magnification^2];
  isVisible = utls.ellipse_in_bbox(magFrames, imgbox);
  frames = frames(:, isVisible);
end
if isempty(frames), descs = []; delete(tmpImgPath); return; end;
if opts.magnification ~= BUILTIN_MAGNIF
  % Magnify the frames accordnig to set magnif. factor
  magFactor = opts.magnification / BUILTIN_MAGNIF;
  frames(3:5,:) = frames(3:5,:) .* magFactor^2;
end
% Make sure there is not only one frame, leads to segfault
numFrames = size(frames, 2);
if numFrames == 1, frames = [frames [1;1;1;0;1]]; end


framesFile = [tempname '.frames'];
legacy.vgg_features_write(framesFile, frames, []);

outDescFile = [tempname(), '.descs'];
% Prepare the options
descrCmd = sprintf('%s -%s -i "%s" -p1 "%s" -o1 "%s"', BIN_PATH, ...
  opts.descriptor, tmpImgPath, framesFile, outDescFile);
if opts.noAngle, descrCmd = [descrCmd, ' -noangle']; end
[status, msg] = system(descrCmd);
if status
  error('VGG_DESC failed. Offending command: %s\n %s', descrCmd, msg);
end
[frames, descs] = legacy.vgg_features_read(outDescFile, 'floatDesc', true);
delete(outDescFile); delete(framesFile); delete(tmpImgPath);
if numFrames == 1
  frames = frames(:, 1:numFrames);
  descs = descs(:, 1:numFrames);
end

if opts.magnification ~= BUILTIN_MAGNIF
  frames(3:5, :) = frames(3:5, :) ./ magFactor^2;
end

