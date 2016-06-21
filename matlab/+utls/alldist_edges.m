function [ edges, dists ] = alldist_edges( data, qdata, varargin )
%ALLDIST_EDGES Match all features
opts.metric = 'L2';
opts = vl_argparse(opts, varargin);

dists = vl_alldist2(single(data), single(qdata), opts.metric);
% Create list of edges in the bipartite graph
[aIdx, bIdx] = ind2sub([size(data, 2), size(qdata, 2)], 1:numel(dists));
edges = [aIdx; bIdx];

end

