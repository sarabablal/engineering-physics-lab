"""
PROJECT: Telescopic Robotic Arm Kinematics Engine
PROBLEM STATEMENT (L'ÉNONCÉ):
Consider a single-link Telescopic Robotic Arm rotating in a 2D plane with 
simultaneous rotational and translational movements:
  - Extension: Radial expansion r(t) = r_0 + v_r * t
  - Rotation : Angular position theta(t) = omega * t

OBJECTIVES:
  1. Perform symbolic derivation of position, velocity, and acceleration 
     vectors using SymPy.
  2. Perform numerical discretization, derive finite difference velocities, 
     and evaluate absolute error using NumPy & Pandas.
  3. Validate mechanical error tolerance (< 0.01 m/s) and plot kinematic 
     profiles using Matplotlib.

"""

import sympy as sp
import numpy as np
import pandas as pd
import plotly.express as px

#  PART 1: Symbolic Derivations (SymPy)
t = sp.Symbol('t', real=True, positive=True)
omega, v_r, r_0 = sp.symbols('omega v_r r_0', real=True, positive=True)

r_t = r_0 + v_r * t
theta_t = omega * t

x_abs = (r_0 + v_r * t) * sp.cos(omega * t)
y_abs = (r_0 + v_r * t) * sp.sin(omega * t)

vx_abs = sp.diff(x_abs, t)
vy_abs = sp.diff(y_abs, t)
v_mag_abs = sp.sqrt(vx_abs**2 + vy_abs**2)

a_coriolis_sym = 2 * omega * v_r

#  PART 2: Numerical Setup (NumPy & Pandas)
x_func = sp.lambdify((t, omega, v_r, r_0), x_abs, 'numpy')
y_func = sp.lambdify((t, omega, v_r, r_0), y_abs, 'numpy')
v_analytical_func = sp.lambdify((t, omega, v_r, r_0), sp.simplify(v_mag_abs), 'numpy')

# Handle dynamic values securely
omega_val = float(input("Enter angular vector value (omega) in rad/s: "))
v_r_val = float(input("Enter extension vector value (v_r) in m/s: "))
r_0_val = float(input("Enter initial length (r_0) in m: "))
t_max = float(input("Enter totaltime in s: "))
dt = float(input("Enter time step in s: "))

t_array = np.arange(0, t_max + dt, dt)

x_num = x_func(t_array, omega_val, v_r_val, r_0_val)
y_num = y_func(t_array, omega_val, v_r_val, r_0_val)
v_analytical = v_analytical_func(t_array, omega_val, v_r_val, r_0_val)

#  FIX: Evaluate scalar multiplication directly to create a clean NumPy array
a_cor_scalar = 2 * omega_val * v_r_val
a_coriolis_num = np.full_like(t_array, a_cor_scalar)

# Calculate numerical velocity using finite differences
vx_num = np.gradient(x_num, dt)
vy_num = np.gradient(y_num, dt)
v_numerical = np.sqrt(vx_num**2 + vy_num**2)

df = pd.DataFrame({
    'Time (s)': t_array,
    'X Position (m)': x_num,
    'Y Position (m)': y_num,
    'Analytical Velocity (m/s)': v_analytical,
    'Numerical Velocity (m/s)': v_numerical,
    'Coriolis Acceleration (m/s^2)': a_coriolis_num
})
df['Absolute Error (m/s)'] = np.abs(df['Analytical Velocity (m/s)'] - df['Numerical Velocity (m/s)'])


#  PART 3: Plotly Express Only Visualization
print(f"Max Absolute Error: {df['Absolute Error (m/s)'].max():.4f} m/s")

plot_df_list = []

# Subplot 1 Data: Trajectory
df_traj = pd.DataFrame({
    'X_Axis': df['X Position (m)'],
    'Value': df['Y Position (m)'],
    'Metric': 'Y Position (m)',
    'Chart': 'Trajectory (X vs Y)'
})
plot_df_list.append(df_traj)

# Subplot 2 Data: Velocity Profiles
df_v_ana = pd.DataFrame({
    'X_Axis': df['Time (s)'],
    'Value': df['Analytical Velocity (m/s)'],
    'Metric': 'Analytical Velocity',
    'Chart': 'Velocity Profiles'
})
df_v_num = pd.DataFrame({
    'X_Axis': df['Time (s)'],
    'Value': df['Numerical Velocity (m/s)'],
    'Metric': 'Numerical Velocity',
    'Chart': 'Velocity Profiles'
})
plot_df_list.extend([df_v_ana, df_v_num])

# Subplot 3 Data: Coriolis Acceleration
df_cor = pd.DataFrame({
    'X_Axis': df['Time (s)'],
    'Value': df['Coriolis Acceleration (m/s^2)'],
    'Metric': 'Coriolis Accel.',
    'Chart': 'Coriolis Acceleration'
})
plot_df_list.append(df_cor)

facet_df = pd.concat(plot_df_list, ignore_index=True)

fig = px.line(
    facet_df, 
    x="X_Axis", 
    y="Value", 
    color="Metric", 
    facet_col="Chart",
    category_orders={"Chart": ["Trajectory (X vs Y)", "Velocity Profiles", "Coriolis Acceleration"]},
    labels={"X_Axis": "X / Time", "Value": "Value (m / m/s / m/s²)"},
    title="Telescopic Robotic Arm Kinematics Analysis (Plotly Express Only)"
)

# Unlink axes so scales match individual data types
fig.update_yaxes(matches=None, showticklabels=True)
fig.update_xaxes(matches=None)

fig.update_layout(
    height=500,
    width=1400,
    template="plotly_white",
    legend_title_text="Variables"
)

# Export and Show
fig.write_html('kinematics_simple.html')
df.to_csv('kinematics_results.csv', index=False)
fig.show()