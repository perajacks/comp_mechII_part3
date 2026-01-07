#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:12:07 2026

@author: Jason
"""

import numpy as np
from assembly import assemble_global_matrices, apply_boundary_conditions
from static_solver import tip_load_vector, static_solver, analytical_solution
from newmark import newmark, freq_estimation
import matplotlib.pyplot as plt


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

#-------------------------------------------------------------------
#part B: Free Vipration
#-------------------------------------------------------------------

u0 = u
v0  = np.zeros_like(u0)

zero_force = lambda t: np.zeros_like(u0)

dt = 1e-4
t_end = 2.0

t, uh, vh, ah = newmark(M_r, K_r, zero_force, u0, v0, dt, t_end)

omega_1 = freq_estimation(t,uh[:-2], min_height=0.0,min_distance=0.08)
omega_ana = (1.875**2) * np.sqrt((E*I*rho*A*L**4))

print(f"ω1 FEM: {omega_1:.6e}") 
print(f"ω1 ANA: {omega_ana:.6e}") 


print("stop")