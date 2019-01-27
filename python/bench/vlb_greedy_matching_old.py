#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: vlb_greedy_matching.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Sat Jan 26 22:40:12 2019
#
#  Usage: python vlb_greedy_matching.py -h
#  Description:
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

import numpy as np

def vlb_greedy_matching(numNodesA, numNodesB, edge_array):
    matches = np.zeros((numNodesA,2), dtype = np.int)-1
    second_closest = np.zeros((numNodesA,2), dtype = np.int)-1

    nodeAAvail = [True]*numNodesA
    nodeBAvail = [True]*numNodesB

    matchedNodes = 0;
    maxNumMatches = numNodesA if numNodesA < numNodesB else numNodesB

    for i in range(edge_array.shape[0]):
        aIdx = edge_array[i,0]
        bIdx = edge_array[i,1]
        
        if nodeAAvail[aIdx] and nodeBAvail[bIdx]:
            matches[aIdx,0] = bIdx
            matches[aIdx,1] = i
            nodeAAvail[aIdx] = False
            nodeBAvail[bIdx] = False
            matchedNodes += 1

        if not nodeAAvail[aIdx] and second_closest[aIdx,0]==-1:
            second_closest[aIdx,0] = bIdx
            second_closest[aIdx,1] = i

        if matchedNodes>=maxNumMatches:
            break

    return matches, second_closest


def main():
    edge_array = np.array([[0,1],[0,0],[1,1],[1,0],[2,1]])
    matches, second_closest = vlb_greedy_matching(3, 3, edge_array)
    print(matches, second_closest)


if __name__ == '__main__':
    main()

