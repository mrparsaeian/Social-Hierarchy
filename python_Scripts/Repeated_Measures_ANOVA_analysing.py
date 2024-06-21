import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

# Simulation parameters
num_rats = 10
t_points = 50
np.random.seed(42)

# Simulate time series data
def simulate_data(num_rats, t_points):
    time = np.arange(t_points)
    data = {
        'Time': np.tile(time, num_rats),
        'Rat': np.repeat(np.arange(num_rats), t_points),
        'Social_Status': np.random.rand(num_rats * t_points),
        'Aggressiveness': np.random.rand(num_rats * t_points),
        'Resource_Access': np.random.rand(num_rats * t_points),
        'Corticosterone': np.random.rand(num_rats * t_points),
        'Testosterone': np.random.rand(num_rats * t_points),
        'Food_Access': np.random.rand(num_rats * t_points)
    }
    return pd.DataFrame(data)

# Generate the data
df = simulate_data(num_rats, t_points)

# Perform Repeated Measures ANOVA for each attribute
attributes = ['Social_Status', 'Aggressiveness', 'Resource_Access', 'Corticosterone', 'Testosterone', 'Food_Access']

for attribute in attributes:
    print(f'\nRepeated Measures ANOVA for {attribute}')
    aovrm = AnovaRM(df, attribute, 'Rat', within=['Time'])
    res = aovrm.fit()
    print(res)

    # Example of post-hoc analysis (if needed)
    posthoc = pairwise_tukeyhsd(df[attribute], df['Time'])
    print(posthoc)

# Visualizing the simulated data (optional)
for attribute in attributes:
    plt.figure(figsize=(10, 6))
    for rat in range(num_rats):
        plt.plot(df['Time'][df['Rat'] == rat], df[attribute][df['Rat'] == rat], label=f'Rat {rat}')
    plt.title(f'{attribute} Over Time')
    plt.xlabel('Time')
    plt.ylabel(attribute)
    plt.legend(loc='upper right')
    plt.show()
