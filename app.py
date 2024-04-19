import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import time
import threading

# Load your Excel data into a pandas DataFrame and preprocess it
df = pd.read_excel('urban heat.xlsx')

# Select relevant features and handle missing values if any
features = ['t2m', 'd2m', 'u10', 'v10', 'cape', 'cin', 'tcc']  # Adjust based on your data
target = 'ubh'  # Define your target variable

df = df[features + [target]].dropna()

# Split data into features and target variable
X = df[features]
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the ANN model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(features)]),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)  # For regression tasks, use linear activation in the output layer
])

model.compile(optimizer='adam', loss='mean_squared_error')  # Compile the model with appropriate optimizer and loss function

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Create Flask app
app = Flask(__name__)

# Global variables for data and time
global_data = None
global_time = None

# Function to update data and time every 10 minutes
def update_data_time():
    global global_data, global_time
    while True:
        global_data = generate_random_data()
        global_time = time.strftime('%H:%M:%S')
        time.sleep(600)  # Sleep for 10 minutes

# Function to generate random data based on Excel sheet
def generate_random_data():
    random_data = {}
    for feature in features:
        # Assuming your data ranges are known
        min_value = df[feature].min()
        max_value = df[feature].max()
        random_data[feature] = np.random.uniform(min_value, max_value)
    return random_data

# Thread to update data and time
update_thread = threading.Thread(target=update_data_time)
update_thread.daemon = True
update_thread.start()

# Define route for dashboard
@app.route('/')
def dashboard():
    global global_data, global_time

    # Make predictions based on new data
    new_data_scaled = scaler.transform([list(global_data.values())])
    prediction = model.predict(new_data_scaled)
    prediction_value = prediction[0][0]

    # Create plots for all variables in a 3x3 grid with different colors
    fig, axs = plt.subplots(3, 3, figsize=(16, 12))
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink']
    for i, (feature, color) in enumerate(zip(features, colors)):
        row = i // 3
        col = i % 3
        axs[row, col].plot(df[feature], label=feature, color=color)
        axs[row, col].set_xlabel('Time')
        axs[row, col].set_ylabel(feature)
        axs[row, col].set_title(f'{feature} over Time')
        axs[row, col].legend()
    plt.tight_layout()
    plt.savefig('static/all_variables_plots.png')  # Save the plot as a static file

    # Create a pie chart for a suitable data variable
    suitable_data = df['t2m']  # Example variable for pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(suitable_data.value_counts(), labels=suitable_data.unique(), colors=colors, autopct='%1.1f%%')
    plt.title('Distribution of Suitable Data')
    plt.savefig('static/pie_chart.png')  # Save the pie chart as a static file

    # Render the dashboard template with prediction, plots, time, and pie chart
    return render_template('dashboard.html', prediction=prediction_value, plots=['static/all_variables_plots.png', 'static/pie_chart.png'], time=global_time)

if __name__ == '__main__':
    app.run(debug=True)
