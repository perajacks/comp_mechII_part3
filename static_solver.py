#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:26:21 2026

@author: Jason
"""
import numpy as np


def tip_load_vector(n_elem,P):
    dof = 2*(n_elem + 1)
    f = np.zeros(dof)
    f[-2] = P
    
    return f


def static_solver(K,f):
    
    return np.linalg.solve(K,f)


def analytical_solution(P,L,E,I):
    wL = P*L**3/(3*E*I)
    thetal = P*L**2/(2*E*I)
    
    return wL, thetal
    