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
import os
import imageio

# material & Geometry
E = 210e9
rho = 7850
L =2.0
R = 0.02
n_elem = 9 #should be odd
dl = np.linspace(0,L,n_elem)  
A = np.pi * R**2
I = np.pi * R**4/4.0

P = 1000.0


#------------------------------------------------------------------
#Part A: Static Analisis
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


omega_1 = freq_estimation(t,uh[:,-2], min_height=0.0,min_distance=0.08)
omega_ana = (1.875**2) * np.sqrt((E*I/(rho*A*L**4)))

print(f"ω1 FEM: {omega_1:.6e}") 
print(f"ω1 ANA: {omega_ana:.6e}") 

#-------------------------------------------------------------------
#part C Dynamic Analisis
#-------------------------------------------------------------------
Omega = 0.95 * omega_1

u0_dynamic = np.zeros_like(u0)
v0_dynamic = np.zeros_like(u0)


def tip_load_function(ti):
    f = np.zeros_like(u0_dynamic)
    f[-2] = P * np.sin(Omega * ti)
    return f

t2, uh2, vh2, ah2 = newmark(M_r, K_r, tip_load_function, u0_dynamic, v0_dynamic, dt, t_end)


plt.figure(figsize=(9, 4))
plt.plot(t2, uh2[:, -2])
plt.xlabel("t [s]")
plt.ylabel("w(L,t) [m]")
plt.title("Forced vibration response at tip: P(t)=P0 sin(Ω t), Ω=0.95 ω1")
plt.show()

plt.figure(figsize=(9, 4))
plt.plot(t2, uh2[:, n_elem])
plt.xlabel("t [s]")
plt.ylabel("w [m]")
plt.title("Forced vibration response at half length: P(t)=P0 sin(Ω t), Ω=0.95 ω1")
plt.show()

plt.figure(figsize=(9, 4))
plt.plot(vh2[:, -2], uh2[:, -2])
plt.xlabel("w [m]")
plt.ylabel("v [m/s^2]")
plt.title("Phase at tip: P(t)=P0 sin(Ω t), Ω=0.95 ω1")
plt.show()

plt.figure(figsize=(9, 4))
plt.plot(vh2[:, 6], uh2[:, n_elem])
plt.xlabel("w [m]")
plt.ylabel("v [m/s^2]")
plt.title("Phase at half length: P(t)=P0 sin(Ω t), Ω=0.95 ω1")
plt.show()

T = []
U = []
E = []

for i in range(len(t2)):
    u_i = uh2[i]
    v_i = vh2[i]
    
    T_i = 0.5 * v_i @ M_r @ v_i
    U_i = 0.5 * u_i @ K_r @ u_i
    E_i = T_i + U_i
    
    T.append(T_i)
    U.append(U_i)
    E.append(E_i)

T = np.array(T)
U = np.array(U)
E = np.array(E)


plt.figure(figsize=(9,4))

plt.plot(t2, T, label="Kinetic")
plt.plot(t2, U, label="Elastic")
plt.plot(t2, E, label="Total")

plt.xlabel("t [s]")
plt.ylabel("Energy [J]")
plt.title("Energy vs time")
plt.legend()
plt.grid(True)
plt.show()


print("stop")


filenames = []

for i in range(0, len(t), 20):   
    plt.figure(figsize=(6,4))


    w_snapshot = uh2[i, 0::2]   

    plt.plot(dl, w_snapshot)
    plt.ylim(-2, 2)        
    plt.xlabel("x [m]")
    plt.ylabel("w [m]")
    plt.title(f"t = {t[i]:.3f} s")

    fname = f"frame_{i}.png"
    filenames.append(fname)
    plt.savefig(fname)
    plt.close()


images = []
for filename in filenames:
    images.append(imageio.imread(filename))

imageio.mimsave('beam_motion.gif', images, duration=0.03)


for f in filenames:
    os.remove(f)
    
    