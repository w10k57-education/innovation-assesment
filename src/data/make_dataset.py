"""
Module used to generate synthetic data for Innovation Assesment
"""
import numpy as np
import pandas as pd

def assign_quality(dictionary):
    """
    Assign random quality values to dictionary keys.

    Parameters:
    - dictionary (dict): Input dictionary.

    Returns:
    - result (dict): Dictionary with assigned quality values.
    """

    result = {}
    for key in dictionary.keys():
        if key not in ['ProductID', 'Name']:
            quality = np.random.choice(['LQ', 'MB', 'A'])
            result[key] = quality
        else:
            result[key] = "NA"

    return result

def generate_bicycle_data(n_products=50, seed=None):
    """
    Generate synthetic bicycle data.

    Parameters:
    - n_products (int): Number of products to generate data for. Default is 50.
    - seed (int): Seed for random number generation. Default is None.

    Returns:
    - dataframe (pandas.DataFrame): DataFrame containing synthetic bicycle data.
    """

    if seed is not None:
        np.random.seed(seed)

    # Generating synthetic data
    data = {
        'ProductID': np.arange(1, n_products + 1),  # Unique product ID
        'Name': ['Bicycle ' + str(i) for i in range(1, n_products + 1)],  # Unique product name
        'Weight': np.random.normal(loc=15, scale=2, size=n_products),  # Normally distributed
        'AeroEff': np.random.normal(loc=7, scale=1.5, size=n_products),  # Normally distributed
        'WheelSize': np.random.normal(loc=26, scale=1.5, size=n_products),  # Normally distributed
        'FrameSize': np.random.normal(loc=55, scale=5, size=n_products),  # Normally distributed
        'GearCount': np.random.lognormal(mean=2, sigma=0.25, size=n_products),  # Skewed
        'MaxSpeed': np.random.normal(loc=30, scale=5, size=n_products),  # Normally distributed
        'BrakeEff': np.random.lognormal(mean=0.9, sigma=0.1, size=n_products),  # Skewed
        'Comfort': np.random.lognormal(mean=1.5, sigma=0.2, size=n_products),  # Skewed
        'Durability': np.random.lognormal(mean=3, sigma=0.3, size=n_products),  # Skewed
        'RideSmooth': np.random.lognormal(mean=2, sigma=0.2, size=n_products)  # Skewed
    }

    # Convert to DataFrame
    dataframe = pd.DataFrame(data)

    attributes = assign_quality(data)

    return dataframe, pd.DataFrame([attributes])

def generate_smartphones_data(n_products=50, seed=None):
    """
    Generate synthetic smartphone data.

    Parameters:
    - n (int): Number of products to generate data for. Default is 50.
    - seed (int): Seed for random number generation. Default is None.

    Returns:
    - dataframe (pandas.DataFrame): DataFrame containing synthetic smartphone data.
    """

    if seed is not None:
        np.random.seed(seed)
    # Generating synthetic data for smartphones
    smartphones_data = {
        'ProductID': np.arange(1, n_products + 1),  # Unique product ID
        'Name': ['Smartphone ' + str(i) for i in range(1, n_products + 1)],  # Unique product name
        'BatteryLife': np.random.normal(loc=24, scale=4, size=n_products),  # Normally distributed
        'ScreenSize': np.random.normal(loc=6, scale=0.5, size=n_products),  # Normally distributed
        'ProcessorClock': np.random.normal(loc=2.5, scale=0.5, size=n_products),  # Normally distributed
        'CameraRes': np.random.lognormal(mean=2.5, sigma=0.3, size=n_products),  # Skewed
        'Memory': np.random.lognormal(mean=6, sigma=0.4, size=n_products),  # Skewed
        'Weight': np.random.normal(loc=200, scale=20, size=n_products),  # Normally distributed
        'Thickness': np.random.normal(loc=8, scale=1, size=n_products),  # Normally distributed
        'ChargingTime': np.random.lognormal(mean=0.5, sigma=0.2, size=n_products),  # Skewed
        'SignalQual': np.random.lognormal(mean=1.8, sigma=0.1, size=n_products),  # Skewed
        'Durability': np.random.lognormal(mean=2, sigma=0.2, size=n_products)  # Skewed
    }

    # Convert to DataFrame
    dataframe = pd.DataFrame(smartphones_data)

    attributes = assign_quality(smartphones_data)

    return dataframe, pd.DataFrame([attributes])

def generate_cars_data(n_products=50, seed=None):
    """
    Generate synthetic data for cars.

    Parameters:
    - n_products (int): Number of car products to generate (default: 50)
    - seed (int): Seed for random number generation (default: None)

    Returns:
    - dataframe (pd.DataFrame): DataFrame containing the generated car data
    """
    if seed is not None:
        np.random.seed(seed)

    # Generating synthetic data for cars
    cars_data = {
        'ProductID': np.arange(1, n_products + 1),  # Unique product ID
        'Name': ['Car ' + str(i) for i in range(1, n_products + 1)],  # Unique product name
        'EnginePower': np.random.normal(loc=200, scale=50, size=n_products),  # Normally distributed
        'FuelEff': np.random.normal(loc=30, scale=5, size=n_products),  # Normally distributed
        'Acceleration': np.random.lognormal(mean=2.5, sigma=0.25, size=n_products),  # Skewed
        'CargoSpace': np.random.lognormal(mean=2, sigma=0.5, size=n_products),  # Skewed
        'Weight': np.random.normal(loc=1500, scale=300, size=n_products),  # Normally distributed
        'Length': np.random.normal(loc=4.5, scale=0.5, size=n_products),  # Normally distributed
        'Safety': np.random.lognormal(mean=2, sigma=0.2, size=n_products),  # Skewed
        'RideSmooth': np.random.lognormal(mean=2, sigma=0.2, size=n_products),  # Skewed
        'MaintenanceFreq': np.random.lognormal(mean=0.5, sigma=0.3, size=n_products),  # Skewed
        'Durability': np.random.normal(loc=10, scale=3, size=n_products)  # Normally distributed
    }

    # Convert to DataFrame
    dataframe = pd.DataFrame(cars_data)

    attributes = assign_quality(cars_data)

    return dataframe, pd.DataFrame([attributes])

if __name__ == '__main__':
    # Generate synthetic data for bikes and save to CSV
    bicycle, bicycle_attr = generate_bicycle_data(n_products=50, seed=42)
    bicycle.to_csv('data/raw/bicycle.csv', index=False)
    bicycle_attr.to_csv('data/raw/bicycle_attributes.csv', index=False)

    # Generate synthetic data for smartphones and save to CSV
    smartphone, smartphone_attr = generate_smartphones_data(n_products=50, seed=42)
    smartphone.to_csv('data/raw/smartphones.csv', index=False)
    smartphone_attr.to_csv('data/raw/smartphone_attributes.csv', index=False)

    # Generate synthetic data for cars and save to CSV
    cars, cars_attr = generate_cars_data(n_products=50, seed=42)
    cars.to_csv('data/raw/cars.csv', index=False)
    cars_attr.to_csv('data/raw/cars_attributes.csv', index=False)
