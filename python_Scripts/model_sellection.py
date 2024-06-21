import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Define the testosterone injection rate function
def testosterone_injection_rate(t, period=5):
    return 1.0 if (t // period) % 2 == 0 else 0.0

# Define the defeat stress exposure rate function
def defeat_stress_exposure_rate(t, period=5):
    return 1.0 if (t // period) % 2 == 0 else 0.0

# Define the dynamical systems model using ODEs
def ode_system(t, state, alpha, beta, gamma, delta, epsilon, theta, phi, xi, eta):
    S, A, R, C, T, E, D = state[:7]
    dSdt = beta * A + xi * E - eta * D - epsilon * (S - np.mean(S))
    dAdt = gamma * C + phi * T - epsilon * (A - np.mean(A))
    dRdt = alpha * S - epsilon * (R - np.mean(R))
    dCdt = 1 / (1 + np.exp(-theta * (R - S))) - delta * C
    dTdt = testosterone_injection_rate(t) - delta * T
    dEdt = 0.05 - delta * E
    dDdt = defeat_stress_exposure_rate(t) - delta * D
    return [dSdt, dAdt, dRdt, dCdt, dTdt, dEdt, dDdt]

# Example function to generate synthetic data
def generate_data(params, num_rats=50, t_points=100):
    initial_conditions = [0.5] * 7
    t = np.linspace(0, 50, t_points)
    sol = solve_ivp(ode_system, [t[0], t[-1]], initial_conditions, t_eval=t, args=params, method='RK45')
    S, A, R, C, T, E, D = sol.y
    return t, S, A, R, C, T, E, D

# Example function for model fitting using optimization
def fit_model(data, initial_conditions, params_guess):
    def objective_function(params):
        t, S_obs, A_obs, R_obs, C_obs, T_obs, E_obs, D_obs = data
        sol = solve_ivp(ode_system, [t[0], t[-1]], initial_conditions, t_eval=t, args=params, method='RK45')
        S_pred, A_pred, R_pred, C_pred, T_pred, E_pred, D_pred = sol.y
        mse = mean_squared_error(S_obs, S_pred) # Update this line to ensure correct shape
        return mse

    result = minimize(objective_function, params_guess, method='L-BFGS-B')
    return result.x

# Example function for model selection using cross-validation
def model_selection(data, models, scoring):
    kf = KFold(n_splits=5)
    best_model = None
    best_score = float('inf')

    for model in models:
        scores = []
        for train_index, test_index in kf.split(data):
            train_data, test_data = data[train_index], data[test_index]
            model.fit(train_data[:, :-1], train_data[:, -1])
            predictions = model.predict(test_data[:, :-1])
            score = scoring(test_data[:, -1], predictions)
            scores.append(score)

        avg_score = np.mean(scores)
        if avg_score < best_score:
            best_score = avg_score
            best_model = model

    return best_model

# Define candidate models
models = [
    LinearRegression()
]

# Example experimental data
params = (1.0, 0.5, 0.1, 0.1, 0.05, 2.0, 0.3, 0.2, 0.4)
t, S, A, R, C, T, E, D = generate_data(params=params, num_rats=50, t_points=100)

# Define initial conditions
initial_conditions = [0.5] * 7

# Flatten the data for model selection
data = np.hstack([S[:, np.newaxis], A[:, np.newaxis], R[:, np.newaxis],
                  C[:, np.newaxis], T[:, np.newaxis], E[:, np.newaxis], 
                  D[:, np.newaxis]])

# Model selection using mean squared error
best_model = model_selection(data, models, scoring=mean_squared_error)

# Fit the selected model to the data
params_guess = [1.0, 0.5, 0.1, 0.1, 0.05, 2.0, 0.3, 0.2, 0.4]
best_params = fit_model((t, S, A, R, C, T, E, D), initial_conditions, params_guess)

print("Best Model Parameters:", best_params)
