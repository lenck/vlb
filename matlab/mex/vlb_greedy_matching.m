function vlb_greedy_matching()
% VLB_GREEDY_MATCHING Compute greedy bipartite matching
%   M = VLB_GREEDY_MATCHING(NUM_A_NODES,NUM_B_NODES,EDGES)
%   Calculates bipartite matching between two sets of nodes 
%   A = {1,...,NUM_A_NODES} and B = {1,...,NUM_B_NODES} based on 
%   the sorted list of edges EDGES.   
%
%   EDGES array has got two columns where each row [a b] defines
%   edge between node a \in A and b \in B. 
%
%   Algorithm basically goes sequentially through the EDGES and 
%   matches all vertices which has not been matched yet. Therefore
%   the ranked list of EDGES represents edge weighting.
%
%   M is of size [2, NUM_A_NODES]. The first row contains the index of a
%   matched B node (\int [1, NUM_B_NODES]) and the second row contains the
%   index of the edge from EDGES which was used to create this match.
%
%   [M, SC] = VLB_GREEDY_MATCHING(NUM_A_NODES,NUM_B_NODES,EDGES) returns
%   the array SC of same size as M. First row of SC contains the index of
%   second closest B_NODE and second row the edge used to create the second
%   closest match.

% Copyright (C) 2011-16 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

error('Mex files not compiled. Please run `vlb_compile`.');
