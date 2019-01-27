#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: parse_arg.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Fri Jan 25 15:28:03 2019
#
#  Usage: python parse_arg.py -h
#  Description:
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

def parse_arg(opts, option):
    for key in option:
        opts[key] = option[key]
