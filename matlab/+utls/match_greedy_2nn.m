function [ matches, dists ] = match_greedy_2nn(data, qdata, varargin)
%MATCH_GREEDY_2NN Match data greedily using the second nearest criterion
dsz = [size(data, 2), size(qdata, 2)];
[edges, dists] = utls.alldist_edges(data, qdata, varargin{:});
[dists, perm] = sort(dists(:), 'ascend'); edges = edges(:, perm);

% Find one-to-one best matches
[matches, secondCl] = vlb_greedy_matching(dsz(1), dsz(2), edges');
matches = [1:size(data, 2); matches];
secondCl = [1:size(data, 2); secondCl];

% Remove non-matching edges
validMatch = matches(2, :)~=0 & secondCl(2, :) ~= 0;
matches = matches(:, validMatch);
secondCl = secondCl(:, validMatch);

dists = dists(matches(3, :)) ./ dists(secondCl(3, :));