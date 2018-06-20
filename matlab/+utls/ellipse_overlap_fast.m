function [ellipsePairs, scores] = ellipse_overlap_fast(f1, f2, varargin)
% ELLIPSE_OVERLAP_FAST Compute overlaps of two sets ov ellipses
%   EVAL = ELLIPSE_OVERLAP_FAST(F1, F2) computes the overlap scores
%   beteen all pairs of ellipses in F1 and F2.  EVAL output structure
%   of size(F2,2) contains following values:
%
%    EVAL(1:2,:)
%      The list of correspondences between ellipses F1 and F2.
%      EVAL(1:2,~) = [a;b] means that ellipses F1(:,a) and F2(:,b) has
%      overlap smaller than a threshold.
%
%    EVAL(3,:)
%      The correpsonding overlaps.
%
%   When frame scale normalisation is not applied the function is
%   symmetric. With rescaling, the frames of F2 are used to fix the
%   scaling factors.
%
%   FASTELLIPSEOVERLAP(F1, F2, 'OptionName', OptionValue) accepts the
%   following options:
%
%   NormaliseFrames:: [true]
%     Fix the the frames scale so that each F2 frame has got scale
%     defined by the 'NormalisedScale' option value.
%
%   NormalisedScale:: [30]
%      When frames scale normalisation applied, fixed scale of frames
%      in F2.
%
%   MinAreaRatio:: [0.3]
%      Precise ellipse overlap is calculated only for ellipses E1
%      and E2 which area ratio is bigger than 'minAreaRatio', s.t.:
%
%        area(E1)/area(E2) > minAreaRatio, area(E1) < area(E2)

% Copyright (C) 2011-16 Andrea Vedaldi, Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.normaliseFrames = true ;
opts.normalisedScale = 30 ;
opts.minAreaRatio = 0.3;
opts.frame2frame = false;
opts.fix = false;
opts = vl_argparse(opts, varargin) ;

f1 = utls.frame2ellipse(f1);
f2 = utls.frame2ellipse(f2);

% eigenvalues (radii squared)
[e1,eigVec1] = utls.ellipse_eigen(f1) ;
[e2,eigVec2] = utls.ellipse_eigen(f2) ;

vggEll1 = utls.ellipse2vggformat(f1, e1, eigVec1);
vggEll2 = utls.ellipse2vggformat(f2, e2, eigVec2);

% areas
a1 = pi * sqrt(prod(e1, 1)) ;
a2 = pi * sqrt(prod(e2, 1)) ;

N2 = size(f2, 2) ;
ellipsePairs = cell(1, N2) ;
scores = cell(1, N2) ;

if isempty(f1) || isempty(f2), return; end

% Given two ellipses f1, f2, we want to upper bound their overlap
% (inters over union). We have
%
%   overlap(f1,f2) = |inters(f1,f2)| / |union(f1,f2)| <= maxOverlap
%   maxOverlap = min(|f1|,|f2|) / max(|f1|,|f2|)
%
%
for i2 = 1:N2
  if opts.normaliseFrames
    s = opts.normalisedScale / sqrt(a2(i2) / pi)  ;
  else
    s = 1;
  end
  
  % Constant 4 is here because it is the maximal elongation of the
  % ellipse in baumberg iteration generally implemnted
  if opts.frame2frame
    ellipsePairs{i2} = [i2*ones(1, size(f1, 2)); 1:size(f1, 2)];
  else
    thr = 4 * sqrt(a2(i2) / pi) ;
    if opts.fix, thr = thr * s; end
    canOverlap = sqrt(vl_alldist2(single(f2(1:2, i2)), single(f1(1:2, :)))) < thr;
    maxOverlap = min(a2(i2), a1) ./ max(a2(i2), a1) .* canOverlap ;
    ellipsePairs{i2} = find(maxOverlap > opts.minAreaRatio);
    ellipsePairs{i2} = [repmat(i2, 1, numel(ellipsePairs{i2}));
      ellipsePairs{i2}];
  end

  
  if isempty(ellipsePairs{i2})
    ellipsePairs{i2} = zeros(2, 0);
    scores{i2} = [];
    continue;
  end
  if opts.normaliseFrames
    vggS = [1 1 1/s^2 1/s^2 1/s^2 s s s s]';
    lhsEllipse = vggS.*vggEll2(:, i2);
    rhsEllipse = bsxfun(@times,vggEll1(:, ellipsePairs{i2}(2, :)), vggS);
  else
    lhsEllipse = vggEll2(:, i2);
    rhsEllipse = vggEll1(:, ellipsePairs{i2}(2, :));
  end
  [~, tw, ~, ~] = vgg_compute_ellipse_overlap(lhsEllipse, rhsEllipse, -1);
  scores{i2} = (1 - tw / 100)' ;
  
end

% Convert to a matrix
ellipsePairs = cell2mat(ellipsePairs);
scores = cell2mat(scores);
