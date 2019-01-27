#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: vgg_compute_ellipse_overlap.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Sat Jan 26 15:28:47 2019
#
#  Usage: python vgg_compute_ellipse_overlap.py -h
#  Description:
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================
import numpy as np
import math

def vgg_compute_ellipse_overlap(feat1, feat2, common_part):
    tdesc_out = np.zeros((feat1.shape[0],feat2.shape[0]), dtype = np.double)
    tover_out = np.zeros((feat1.shape[0],feat2.shape[0]), dtype = np.double)
    over_out = np.zeros((feat1.shape[0],feat2.shape[0]), dtype = np.double)+100.0
    mover_out = np.zeros((feat1.shape[0],feat2.shape[0]), dtype = np.double)
    desc_out = np.zeros((feat1.shape[0],feat2.shape[0]), dtype = np.double)+1000000.0
    mdesc_out = np.zeros((feat1.shape[0],feat2.shape[0]), dtype = np.double)
    
    feat1a = np.zeros((feat1.shape[1],), dtype = np.double)
    feat2a = np.zeros((feat2.shape[1],), dtype = np.double)
    for j in range(feat1.shape[0]):
        max_dist=math.sqrt(feat1[j,5]*feat1[j,6])
        if common_part>0:
            fac=30/max_dist
        elif common_part==0:
            fac=3
        else: 
            fac=1

        max_dist=max_dist*4
        fac=1.0/(fac*fac)
        feat1a[2]=fac*feat1[j,2]
        feat1a[3]=fac*feat1[j,3]
        feat1a[4]=fac*feat1[j,4]
        feat1a[7] = math.sqrt(feat1a[4]/(feat1a[2]*feat1a[4] - feat1a[3]*feat1a[3]))
        feat1a[8] = math.sqrt(feat1a[2]/(feat1a[2]*feat1a[4] - feat1a[3]*feat1a[3]))

        for i in range(feat2.shape[0]):
            dx=feat2[i,0]-feat1[j,0]
            dy=feat2[i,1]-feat1[j,1]
            dist=math.sqrt(dx*dx+dy*dy)

            if dist<max_dist:
                feat2a[2]=fac*feat2[i,2]
                feat2a[3]=fac*feat2[i,3]
                feat2a[4]=fac*feat2[i,4]
                feat2a[7] = math.sqrt(feat2a[4]/(feat2a[2]*feat2a[4] - feat2a[3]*feat2a[3]))
                feat2a[8] = math.sqrt(feat2a[2]/(feat2a[2]*feat2a[4] - feat2a[3]*feat2a[3]))
                
                maxx=math.ceil(feat1a[7] if (feat1a[7]>(dx+feat2a[7])) else (dx+feat2a[7]))
                minx=math.floor(-feat1a[7] if (-feat1a[7]<(dx-feat2a[7])) else (dx-feat2a[7]))
                maxy=math.ceil(feat1a[8] if (feat1a[8]>(dy+feat2a[8])) else (dy+feat2a[8]))
                miny=math.floor(-feat1a[8] if (-feat1a[8]<(dy-feat2a[8])) else (dy-feat2a[8]))

                mina=(maxx-minx) if (maxx-minx)<(maxy-miny) else (maxy-miny)
                dr=mina/50.0
                bua=0
                bna=0
                t1=0
                t2=0
                rx=minx
                while rx<=maxx:
                    rx2=rx-dx
                    t1+=1
                    ry = miny
                    while ry<=maxy:
                        ry2=ry-dy
                        a=feat1a[2]*rx*rx+2*feat1a[3]*rx*ry+feat1a[4]*ry*ry
                        b=feat2a[2]*rx2*rx2+2*feat2a[3]*rx2*ry2+feat2a[4]*ry2*ry2
                        if a<1 and b<1:
                            bna+=1
                        if a<1 or b<1:
                            bua+=1
                        ry += dr
                    rx += dr
                ov=100.0*(1-bna/float(bua))
                tover_out[j,i]=ov
                mover_out[j,i]=ov
            else:
                tover_out[j,i]=100.0
                mover_out[j,i]=100.0
                ov=100.0

            descd=0
            for v in range(9, feat1.shape[0]):
              descd+=((feat1[j,v]-feat2[i,v])*(feat1[j,v]-feat2[i,v]))

            descd=math.sqrt(descd)
            tdesc_out[j,i]=descd
            mdesc_out[j,i]=descd

    minr=0
    mini=0
    minj=0
    while minr<70:
        minr=100
        for j in range(feat1.shape[0]):
            for i in range(feat2.shape[0]):
                if minr>tover_out[j,i]:
                    minr=tover_out[j,i]
                    mini=i
                    minj=j
        if minr<100:
            for j in range(feat1.shape[0]):
                tover_out[j,mini]=100
            for i in range(feat2.shape[0]):
                tover_out[minj,i]=100
            over_out[minj,mini]=minr

    dnbr=0
    minr=0
    while(minr<1000000):
        minr=1000000
        for j in range(feat1.shape[0]):
            for i in range(feat2.shape[0]):
                if minr>tdesc_out[j,i]:
                    minr=tdesc_out[j,i]
                    mini=i
                    minj=j
        if minr<1000000:
            for j in range(feat1.shape[0]):
                tdesc_out[j,mini]=1000000
            for i in range(feat2.shape[0]):
                tdesc_out[minj,+i]=1000000
            desc_out[minj,mini]=dnbr
            dnbr+=1
    return over_out, mover_out, desc_out, mdesc_out
