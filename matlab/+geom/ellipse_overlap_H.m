function [tcorr, corr_score, info] = ellipse_overlap_H(geom, fa, fb, varargin)
%VLB_ELLIPSE_OVERLAP_H Get overlapping ellipses 
%
%   maxOverlapError:: 0.4
%     Maximal overlap error of frames to be considered as
%     correspondences.
%
%   normaliseFrames:: true
%     Normalise the frames to constant scale (defaults is true for
%     detector repeatability tests, see Mikolajczyk et. al 2005).
%
%   normalisedScale:: 30
%     When frames scale normalisation applied, fixed scale to which it is
%     normalised to.
%
%   cropFrames:: true
%     Crop the frames out of overlapping regions (regions present in both
%     images).
%
%   magnification:: 3
%     When frames are not normalised, this parameter is magnification
%     applied to the input frames. Usually is equal to magnification
%     factor used for descriptor calculation.
%
%   warpMethod:: 'linearise'
%     Numerical method used for warping ellipses. Available mathods are
%     'standard' and 'linearise' for precise reproduction of IJCV2005 
%     benchmark results.
% TODO finish the documentation

% Copyright (C) 2011-16 Karel Lenc, Andrea Vedaldi
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.mode = 'frames';
[opts, varargin] = vl_argparse(opts, varargin);
switch opts.mode
  case 'descriptors'
    % A definition for matching descriptors ala K. Mikolajczyk
    opts.normaliseFrames = false;
    opts.maxOverlapError = 0.5;
    opts.cropFrames = false;
  otherwise
    % The frames mode, a default one
    opts.normaliseFrames = true;
    opts.maxOverlapError = 0.4;
    opts.cropFrames = true;
end
opts.normalisedScale = 30;
opts.magnification = 3;
opts.warpMethod = 'linearise';
opts.cropFramesSafetyEdge = [];
opts = vl_argparse(opts, varargin);

info = struct(); tcorr = []; corr_score = [];
overlapThresh = 1 - opts.maxOverlapError;

% convert frames from any supported format to unortiented
% ellipses for uniformity
ella = utls.frame2ellipse(fa) ;
ellb = utls.frame2ellipse(fb) ;

% map frames from image A to image B and viceversa
ella_rep = utls.ellipse_warp(geom.H, ella, 'Method', opts.warpMethod);
ellb_rep = utls.ellipse_warp(inv(geom.H), ellb, 'Method', opts.warpMethod);

% optionally remove frames that are not fully contained in
% both images
fa_valid = true(1, size(fa, 2));
fb_valid = true(1, size(fb, 2));
if opts.cropFrames
  % find frames fully visible in both images
  bba = [1 1 geom.ima_size(2)+1 geom.ima_size(1)+1] ;
  bbb = [1 1 geom.imb_size(2)+1 geom.imb_size(1)+1] ;
  if ~isempty(opts.cropFramesSafetyEdge)
    ser = opts.cropFramesSafetyEdge;
    bba = bba + [geom.refimsize(1:2).*ser, -geom.refimsize(1:2).*ser];
    bbb = bbb + [geom.imsize(1:2).*ser, -geom.imsize(1:2).*ser];
  end
  fa_valid = utls.ellipse_in_bbox(ella, bba) & utls.ellipse_in_bbox(ella_rep, bbb);
  fb_valid = utls.ellipse_in_bbox(ellb_rep, bba) & utls.ellipse_in_bbox(ellb, bbb);
end

info.fa_valid = fa_valid;
info.fb_valid = fb_valid;

info.ella = ella(:, fa_valid);
info.ellb = ellb(:, fb_valid);
info.ella_rep = ella_rep(:, fa_valid);
info.ellb_rep = ellb_rep(:, fb_valid);
if all(~fa_valid) || all(~fb_valid), return; end

%fix the problem that all features are not in the box. 
%In this case, it can't pass to the next function
if isempty(info.ella)||isempty(info.ellb)
    return;
end

if ~opts.normaliseFrames
  % When frames are not normalised, account the descriptor region
  magFactor = opts.magnification^2;
  ella = [ella(1:2, :); ella(3:5, :).*magFactor];
  ellb_rep = [ellb_rep(1:2, :); ellb_rep(3:5, :).*magFactor];
end

% Find all frames overlaps (in one-to-n array)
[ellipsesPairs, ellipsesOverlaps] = utls.ellipse_overlap_fast(...
  ellb_rep(:, fb_valid), ella(:, fa_valid), ...
  'NormaliseFrames', opts.normaliseFrames, 'MinAreaRatio', overlapThresh,...
  'NormalisedScale', opts.normalisedScale);

% Remove frame pairs that have insufficient overlap
isValid = ellipsesOverlaps > overlapThresh;
tcorr = ellipsesPairs(:, isValid);
corr_score = ellipsesOverlaps(:, isValid);
