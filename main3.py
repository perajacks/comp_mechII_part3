#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:12:07 2026

@author: Jason
"""

import numpy as np

# material & Geometry
E = 210e9
rho = 7850
L =2.0
R = 0.02

A = np.pi * R**2
I = np.pi * R**4/4.0

P = 1000.0
n_elem = 8

#------------------------------------------------------------------
#Part A: Static Analisuis
#------------------------------------------------------------------