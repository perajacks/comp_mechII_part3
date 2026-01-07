#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:27:17 2026

@author: Jason
"""

import numpy as np

def beam_element_matrices(E, I, rho, A, Le):
        Ke = (E*I/Le**4) * np.array([[12,    6*Le,      -12,    6*LE]
                                     [6*Le,  4*Le**2,   -6*Le,  2*Le**2]
                                     [-12,  -6*Le,       12,   -6*Le]
                                     [6*Le,  2*L2**2,   -6*Le,  4*Le**2]])