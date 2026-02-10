#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 22:55:12 2026

@author: Jason
"""

import numpy as np

def tip_load_function(t,dynamic):
    f = np.zeros_like(u0_dynamic)
    f[-2] = P * np.sin(Omega * t)
    return f

