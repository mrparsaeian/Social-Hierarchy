import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Differential equations for the updated dynamical systems model
def model(state, t, alpha, beta, gamma, delta, epsilon, theta, phi, xi, eta, injection_rate, interaction_rate, defeat_rate):
    S, A, R, C, T, E, D = state
    
    dSdt = beta * A + xi * E - eta * D - epsilon * (S - np.mean(S))
    dAdt = gamma * C + phi * T - epsilon * (A - np.mean(A))
    dRdt = alpha * S - epsilon * (R - np.mean(R))
    dCdt = 1 / (1 + np.exp(-theta * (R - S))) - delta * C
    dTdt = injection_rate - delta * T
    dEdt = interaction_rate - delta * E
    dDdt = defeat_rate - delta * D
    
    return [dSdt, dAdt, dRdt, dCdt, dTdt, dEdt, dDdt]

# Initial conditions and parameters for various scenarios
scenarios = [
    {'initial': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 'alpha': 1.0, 'beta': 0.5, 'gamma': 0.1, 'delta': 0.1, 'epsilon': 0.05, 'theta': 2.0, 'phi': 0.3, 'xi': 0.2, 'eta': 0.4, 'injection_rate': 0.1, 'interaction_rate': 0.05, 'defeat_rate': 0.1, 'label': 'Scenario 1'},
    {'initial': [0.2, 0.7, 0.4, 0.6, 0.3, 0.4, 0.3], 'alpha': 1.2, 'beta': 0.6, 'gamma': 0.2, 'delta': 0.2, 'epsilon': 0.05, 'theta': 2.5, 'phi': 0.4, 'xi': 0.3, 'eta': 0.5, 'injection_rate': 0.15, 'interaction_rate': 0.1, 'defeat_rate': 0.15, 'label': 'Scenario 2'},
    {'initial': [0.8, 0.3, 0.6, 0.4, 0.7, 0.2, 0.5], 'alpha': 1.5, 'beta': 0.4, 'gamma': 0.3, 'delta': 0.3, 'epsilon': 0.1, 'theta': 1.5, 'phi': 0.2, 'xi': 0.4, 'eta': 0.6, 'injection_rate': 0.2, 'interaction_rate': 0.15, 'defeat_rate': 0.2, 'label': 'Scenario 3'}
]

# Time points
t = np.linspace(0, 50, 500)

# Plotting
plt.figure(figsize=(12, 8))

for scenario in scenarios:
    state = odeint(model, scenario['initial'], t, args=(scenario['alpha'], scenario['beta'], scenario['gamma'], scenario['delta'], scenario['epsilon'], scenario['theta'], scenario['phi'], scenario['xi'], scenario['eta'], scenario['injection_rate'], scenario['interaction_rate'], scenario['defeat_rate']))
    S, A, R, C, T, E, D = state.T
    plt.plot(t, S, label=f"{scenario['label']} - Social Status")
    plt.plot(t, A, label=f"{scenario['label']} - Aggressiveness", linestyle='--')
    plt.plot(t, R, label=f"{scenario['label']} - Resource Access", linestyle='-.')
    plt.plot(t, C, label=f"{scenario['label']} - Stress", linestyle=':')
    plt.plot(t, T, label=f"{scenario['label']} - Testosterone", linestyle='-')
    plt.plot(t, E, label=f"{scenario['label']} - Experience", linestyle='-.')
    plt.plot(t, D, label=f"{scenario['label']} - Defeat Stress", linestyle=':')

plt.xlabel('Time')
plt.ylabel('State Variables')
plt.legend()
plt.title('Dynamical Systems Simulation for Various Scenarios')
plt.show()