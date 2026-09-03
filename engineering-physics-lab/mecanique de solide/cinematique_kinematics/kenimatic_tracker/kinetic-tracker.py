import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt


# 1. SYMBOLIC SETUP & PARAMETER DEFINITIONS
# Define symbolic variables for analytical calculus using SymPy.
# Inputs are strictly defined as real and positive to streamline algebraic expansion.
t = sp.symbols('t', real=True, positive=True)
omega, v_r = sp.symbols('omega v_r', real=True, positive=True)

# Render output math in LaTeX format
sp.init_printing(use_latex='mathjax')

def validate_inputs(omega, v_r):
    """
    Sanity check to prevent division by zero or non-physical negative velocity states.
    """
    if omega <= 0 or v_r <= 0:
        raise ValueError("Inputs must be positive real numbers.")


# 2. VECTOR KINEMATICS & ROTATION MATRICES
# Set up relative position vectors and project them into the fixed global frame.
# Position vector inside the rotating frame (R'), moving purely along the local X-axis
r_rel = sp.Matrix([
    [v_r * t],
    [0],
    [0]
])

# Standard 2D Rotation Matrix around the Z-axis: maps Frame R' -> Frame R
R_z = sp.Matrix([
    [sp.cos(omega * t), -sp.sin(omega * t), 0],
    [sp.sin(omega * t), sp.cos(omega * t), 0],
    [0, 0, 1]
])

# Compute absolute position in ground frame: r_abs = R_z * r_rel
r_abs = R_z * r_rel
x_t = r_abs[0]
y_t = r_abs[1]

# Differentiate analytical position with respect to time to extract true velocity vector
v_abs_vect = r_abs.diff(t)

# Angular velocity vector and relative linear speed vector for cross-product calculus
Omega = sp.Matrix([[0], [0], [omega]])
V_r = sp.Matrix([[v_r], [0], [0]])

# Relative frame accelerations (Coriolis and Centrifugal components)
a_c_rel = 2 * Omega.cross(V_r)                         # Coriolis: 2 * (Omega x V_r)
a_e_rel = Omega.cross(Omega.cross(r_rel))              # Centrifugal: Omega x (Omega x r')

# Project fictitious acceleration vectors back into the fixed global frame
a_c_vect = R_z * a_c_rel
a_e_vect = R_z * a_e_rel

# Sum components to derive total absolute acceleration vector
a_abs_vect = sp.simplify(a_c_vect + a_e_vect)


# 3. SYMBOLIC-TO-NUMERICAL CONVERSION (LAMBDIFY)
# Convert SymPy analytical expressions into high-speed vectorized NumPy functions.
x_func = sp.lambdify((t, omega, v_r), x_t, 'numpy')
y_func = sp.lambdify((t, omega, v_r), y_t, 'numpy')

v_x_func = sp.lambdify((t, omega, v_r), v_abs_vect[0], 'numpy')
v_y_func = sp.lambdify((t, omega, v_r), v_abs_vect[1], 'numpy')


# 4. USER INTERACTIVE INPUTS
# Capture initial physical constraints and time-stepping specs from terminal.
omega_val = float(input('Enter The Angular Vector Value (omega): '))
v_r_val = float(input('Enter The Relative Vector Value (v_r): '))
t_max = float(input('Enter The Total Time Value (t_max): '))
dt = float(input('Enter The Time Step Value (dt): '))

validate_inputs(omega_val, v_r_val)


# 5. NUMERICAL COMPUTATION & FINITE DIFFERENCE SCHEME
# Evaluate spatial positions and compare discrete numeric derivative vs exact symbolic calculus.
# Discretize continuous time domain
t_array = np.arange(0, t_max, dt)

# Generate positional trajectories over time
x_array = x_func(t_array, omega_val, v_r_val)
y_array = y_func(t_array, omega_val, v_r_val)

# Compute velocity using Forward Finite Difference scheme: v = delta_x / delta_t
# Reduces array size by 1 (hence alignment using t_array[:-1] below)
v_x_num = np.diff(x_array) / dt
v_y_num = np.diff(y_array) / dt

# Extract exact analytical velocity values at matching discrete time steps
v_x_theo = v_x_func(t_array[:-1], omega_val, v_r_val)
v_y_theo = v_y_func(t_array[:-1], omega_val, v_r_val)


# 6. DATA LOGGING & DISCRETIZATION ERROR ANALYSIS
# Store results in a Pandas DataFrame to quantify numerical approximation drift.
df = pd.DataFrame({
    'Time (s)': t_array[:-1],
    'X (m)': x_array[:-1],
    'Y (m)': y_array[:-1],
    'Vx Theoretical': v_x_theo,
    'Vx Numerical': v_x_num,
    'Absolute Error Vx': np.abs(v_x_theo - v_x_num)
})

print("\n--- Summary Table (First 10 Rows) ---")
print(df.head(10))


# 7. DATA VISUALIZATION & DIAGNOSTIC PLOTS
# Render 2D spatial motion, numerical convergence, and error boundaries.
plt.figure(figsize=(14, 5))

# Plot 1: 2D Spatial Trajectory (Archimedean Spiral in fixed ground frame)
plt.subplot(1, 3, 1)
plt.plot(x_array, y_array, label='Trajectory (Y vs X)', color='blue', linewidth=2)
plt.grid(True, linestyle='--')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.title('2D Spiral Trajectory')
plt.axis('equal')  # Maintains 1:1 aspect ratio to preserve geometric truth
plt.legend()

# Plot 2: Theoretical Calculus vs Discrete Numerical Approximation
plt.subplot(1, 3, 2)
plt.plot(df['Time (s)'], df['Vx Theoretical'], label='Theoretical', color='green', linewidth=2)
plt.plot(df['Time (s)'], df['Vx Numerical'], label='Numerical', color='orange', linestyle='--')
plt.grid(True, linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Vx (m/s)')
plt.title('Velocity Comparison')
plt.legend()

# Plot 3: Discretization Error Margin |V_theo - V_num| over time
plt.subplot(1, 3, 3)
plt.plot(df['Time (s)'], df['Absolute Error Vx'], label='Absolute Error', color='red')
plt.grid(True, linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Error Margin (m/s)')
plt.title('Calculus Drift')
plt.legend()

plt.tight_layout()
plt.show()
