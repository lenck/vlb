#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: vlb_greedy_matching.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Sat Jan 26 22:40:12 2019
#
#  Description: A cython implementation of vlb_greedy_matching
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

import numpy as np
cimport numpy as np

def vlb_greedy_matching(int numNodesA, int numNodesB, np.ndarray[np.int_t, ndim=2] edge_array):
    cdef np.ndarray[np.int_t, ndim=2] matches = np.zeros((numNodesA,2), dtype = np.int)-1
    cdef np.ndarray[np.int_t, ndim=2] second_closest = np.zeros((numNodesA,2), dtype = np.int)-1

    cdef np.ndarray[np.int_t, ndim=1] nodeAAvail = np.ones((numNodesA,), dtype = np.int)
    cdef np.ndarray[np.int_t, ndim=1] nodeBAvail = np.ones((numNodesB,), dtype = np.int)

    cdef int matchedNodes
    cdef int maxNumMatches
    cdef int i, aIdx, bIdx
    maxNumMatches = numNodesA if numNodesA < numNodesB else numNodesB
    matchedNodes = 0

    for i in range(edge_array.shape[0]):
        aIdx = edge_array[i,0]
        bIdx = edge_array[i,1]
        
        if nodeAAvail[aIdx] and nodeBAvail[bIdx]:
            matches[aIdx,0] = bIdx
            matches[aIdx,1] = i
            nodeAAvail[aIdx] = 0
            nodeBAvail[bIdx] = 0
            matchedNodes += 1

        if not nodeAAvail[aIdx] and second_closest[aIdx,0]==-1:
            second_closest[aIdx,0] = bIdx
            second_closest[aIdx,1] = i

        if matchedNodes>=maxNumMatches:
            break

    return matches, second_closest

