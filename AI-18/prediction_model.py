import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Dummy data
times = np.arange(10)  # Minutes
# Simulating a steadily increasing crowd count (e.g., more people arriving over time)
crowd = 5 + times + np.random.randint(0, 2, 10)  # Adds random noise

model = LinearRegression()
model.fit(times.reshape(-1,1), crowd)

def predict_crowd(next_minutes=5):
    future_times = np.arange(10, 10 + next_minutes)
    predictions = model.predict(future_times.reshape(-1,1))
    print("Predicted crowd for next moments:", predictions)
    return predictions

def plot_prediction():
    plt.plot(times, crowd, 'bo-', label='Actual Crowd')
    future_times = np.arange(10, 15)
    future_crowd = model.predict(future_times.reshape(-1,1))
    plt.plot(future_times, future_crowd, 'ro--', label='Predicted Crowd')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Crowd Count")
    plt.legend()
    plt.grid()
    plt.savefig("templates/prediction_graph.png")
    plt.close()

# Call the functions for prediction and plotting
predict_crowd()
plot_prediction()
