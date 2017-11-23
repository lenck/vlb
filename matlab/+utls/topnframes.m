function [ feats ] = topnframes( feats, n )
%TOPNFEATS pick only top-N features based on the detresponses
%   Detailed explanation goes here
assert(isfield(feats, 'detresponses'));
if isinf(n), return; end
[~, perm] = sort(abs(feats.detresponses), 'descend');
perm = perm(1:min(n, numel(perm)));
feats.frames = feats.frames(:, perm);
feats.detresponses = feats.detresponses(:, perm);
if isfield(feats, 'descs')
  feats.descs = feats.descs(:, perm);
end
end

