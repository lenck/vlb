function [ matches, dists ] = match_greedy_2nn(data, qdata, varargin)
%MATCH_GREEDY_2NN Match data greedily
dsz = [size(data, 2), size(qdata, 2)];
[edges, dists] = utls.alldist_edges(data, qdata, varargin{:});
[dists, perm] = sort(dists(:), 'ascend'); edges = edges(:, perm);

% Find one-to-one best matches
[matches, secondCl] = vlb_greedy_matching(dsz(1), dsz(2), edges');
matches = [1:size(data, 2); matches(1, :)];
% Remove non-matching edges
matches = matches(:, matches(2, :)~=0);
secondCl = secondCl(:, matches(2, :)~=0);

% Remove non-match edges
validMatch = matches(2, :)~=0 & secondCl ~= 0;
matches = matches(:, validMatch);
secondCl = secondCl(:, validMatch);
if nargout > 1
  revind(perm) = 1:numel(dists); % Create reverse index
  distsF = dists(revind(sub2ind(dsz, matches(1, :), matches(2, :))));
  distsSc = dists(revind(sub2ind(dsz, matches(1, :), secondCl(1, :))));
  dists = distsF./distsSc;
end