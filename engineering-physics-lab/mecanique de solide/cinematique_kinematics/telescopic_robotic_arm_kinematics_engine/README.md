# 🤖 Telescopic Robotic Arm Kinematics Engine

An engineering-grade numerical analysis and physics simulation engine designed to model, compute, and validate the planar kinematics of a single-link telescopic robotic manipulator undergoing simultaneous rotational and translational expansion.

This tool bridges **symbolic calculus** with **discrete numerical methods**, validating theoretical analytical derivations against finite difference approximations to ensure structural simulation precision and zero-defect data pipelines.

---

## 📌 Overview

The engine addresses a fundamental 2D multibody dynamics problem where a robotic link extends radially at speed $v_r$ while rotating about a fixed base at angular velocity $\omega$:

* **Radial Position:** $r(t) = r_0 + v_r \cdot t$
* **Angular Position:** $\theta(t) = \omega \cdot t$

The system calculates exact spatial trajectories, absolute/component velocities, and total acceleration profiles—including the non-inertial **Coriolis Acceleration** component ($a_{\text{coriolis}} = 2\omega v_r$).

---

## ✨ Key Features

* **Symbolic Calculus Engine (`SymPy`):** Automatically derives exact analytical equations for continuous positions ($x, y$), velocity vectors ($v_x, v_y$), absolute velocity magnitudes, and Coriolis acceleration.
* **Numerical Discretization (`NumPy`):** Transforms continuous equations into discrete time series and computes numerical derivatives using central finite differences (`np.gradient`).
* **Error Quantification (`Pandas`):** Performs continuous error analysis between analytical ground truth and numerical solvers to validate simulation accuracy.
* **Interactive Data Visualization (`Plotly Express`):** Generates multi-panel interactive charts with decoupled axes to easily isolate kinematic trends.
* **Automated Asset Export:** Automatically saves clean data pipelines, exporting interactive web visualizations (`.html`) and structured numerical datasets (`.csv`).

---

## 📊 Example Output

### 1. Terminal Execution Log
When running `kinematics_engine.py` with standard physical test inputs ($\omega = 1.5\text{ rad/s}$, $v_r = 0.4\text{ m/s}$, $r_0 = 0.5\text{ m}$, $t_{\text{max}} = 6.0\text{ s}$, $dt = 0.005\text{ s}$):

```text
Enter angular vector value (omega) in rad/s: 1.5
Enter extension vector value (v_r) in m/s: 0.4
Enter initial length (r_0) in m: 0.5
Enter totaltime in s: 6.0
Enter time step in s: 0.005

Max Absolute Error: 0.0015 m/s
```