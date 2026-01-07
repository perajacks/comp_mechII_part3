#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:12:07 2026

@author: Jason
"""

import numpy as np
from assembly import assemble_global_matrices, apply_boundary_conditions
from static_solver import tip_load_vector, static_solver, analytical_solution


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

K, M = assemble_global_matrices(n_elem, E, I, rho, A, L)

f = tip_load_vector(n_elem, P)

fixed_dofs = [0, 1]

K_r, M_r, f_r , free = apply_boundary_conditions(K, M, f, fixed_dofs)

u = static_solver(K_r, f_r)

wL_num = u[-2]
wL_ana, _ = analytical_solution(P, L, E, I)

print(f"Static Tip Displasment FEM: {wL_num:.6e}") 
print(f"Static Tip Displasment ANA: {wL_ana:.6e}") 
