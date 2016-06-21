function [ matches, dists ] = match_greedy(data, qdata, varargin)
%MATCH_1TO1 Match data greedily
[edges, dists] = utls.alldist_edges(data, qdata, varargin{:});
[dists, perm] = sort(dists(:), 'ascend'); edges = edges(:, perm);

% Find one-to-one best matches
matches = vlb_greedy_matching(size(data, 2), size(qdata, 2), edges');
matches = [1:size(data, 2); matches];
% Remove non-matching edges
matches = matches(:, matches(2, :)~=0);
if nargout > 1
  revind(perm) = 1:numel(dists); % Create reverse index
  dists = dists(revind(sub2ind([size(data, 2), size(qdata, 2)],...
    matches(1, :), matches(2, :))));
end
