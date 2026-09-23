# Dynamic beam analysis problem

## Problem characteristics
A Euler-Bernoulli beam is clamped at the left end and free at the right 
end. The equation characterizing the phenomenon is M ü + K u = f(t). The 
finite element method is used to solve the problem. Damping is neglected.

## Beam characteristics
    Young's modulus E = 210 GPa 
    Density ρ = 7850 kg/m^3
    Length of beam L = 2 m 
    Radius of beam R = 0.02 m
    Applied load P = 1 kN (on the free end of the beam)

## Part A: Static analysis 
With the load applied as a fixed value, we assemble both the stiffness 
matrix (K) and the mass matrix (M), then compute the deflection and 
rotation at each node. The system solved is K u = f, after the boundary 
conditions are applied.

Analytical solution at the free end:
    w = P*L^3/3EI = 0.10105
    θ = P*L^2/2EI = 0.07578
    
Numerical solution at the free end:
    w = 0.10105
    θ = 0.07578

<img width="700" height="400" alt="image" src="https://github.com/user-attachments/assets/274e1103-ee06-498c-9df7-7b6f96f591ff" />

As shown above, the error is small enough that we can say the numerical 
solution converges to the analytical solution.

## Part B: Free oscillation and natural frequency estimation
Using the Newmark method, we solve M ü + K u = 0 with the beam initially 
bent the same way it was by the static load P (zero initial velocity). 
The method integrates, with a time increment dt = 1e-4 s, the position, 
velocity, and acceleration of each node through time up to t = 2.7 s. 
The beam oscillates at its own natural frequency, which we compute by 
spotting the peaks in the displacement time history of the last (free-end) 
node.

Analytical value of the frequency is given by ω1 = 1.875^2 * sqrt(EI/ρAL^4)

ω1 FEM: 4.541893e+01                                    
 

ω1 ANA: 4.545874e+01

Both values are close to each other, agreeing to within about 0.09% 
relative error.

## Part C: Forced oscillation with time-varying load
Again the load is applied at the free end of the beam, but this time with 
the function P(t) = P0 * sin(Ωt), Ω = 0.95*ω1, and zero initial conditions. 
To solve this problem we again use the Newmark method, but with the load 
changing as in the equation written above.

<img width="700" height="400" alt="image" src="https://github.com/user-attachments/assets/59eb4991-e35e-4f6a-bc2b-3911a9a75494" />
<img width="700" height="400" alt="image" src="https://github.com/user-attachments/assets/b3b8c33a-f6b6-485d-9f21-35f94a91d05a" />

Interesting with the above graphs is the fact that P(t) = P0 * sin(Ωt) with 
Ω = 0.95ω1 causes the beam to gain energy at the beginning, that also 
corresponds to the amplification of the amplitude of the oscillation, and 
after reaching its peak it takes the energy back from the beam. In a way 
we made an oscillation in an oscillation, also known as beating.

