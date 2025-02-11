import numpy as np
import pandas as pd


def calculate_area(q, attr, precision=3):
    """
    Calculate the area based on the quality value and attribute.

    Parameters:
    q (float): The quality value.
    attr (str): The attribute. Choose from 'LQ', 'MB', or 'A'.
    precision (int, optional): The number of decimal places to round the area to. Default is 2.

    Returns:
    tuple: A tuple containing the novelty value and the calculated area.
    """

    if attr not in ['LQ', 'MB', 'A']:
        raise ValueError("Invalid attribute. Please choose 'LQ', 'MB', or 'A'.")

    if not -6 <= q <= 6:
        raise ValueError("Quality value out of range. Please choose a value between -6 and 6.")

    # Calculate novelty based on the attribute
    if attr == 'LQ':
        n = q
    elif attr == 'MB':
        n = 0.5 * (q - np.sqrt(q**2 + 4))
    else:  # 'A'
        n = 0.5 * (q + np.sqrt(q**2 + 4))

    area = round(abs(n * q), precision)

    return round(n, precision), round(area, precision)


def rescale_values(values, inversed=False):
    """
    Rescale values so that:
    - The mean is 0.
    - -3 standard deviations is rescaled to -6.
    - +3 standard deviations is rescaled to +6.
    Values outside the range [-6, 6] are clipped.

    Parameters:
    - values (list or np.ndarray): The input values to rescale.

    Returns:
    - np.ndarray: The rescaled and clipped values.
    """
    # Convert values to a numpy array for convenience
    values = np.array(values)

    # Calculate the mean and standard deviation
    mean = np.mean(values)
    std = np.std(values)

    # Normalize the values to have mean 0
    normalized_values = (values - mean) / std

    # Clip values to be within the range of -6 to 6
    rescaled = np.clip(normalized_values, -6, 6)

    if inversed:
        rescaled = -rescaled

    return rescaled


def calculate_results(features, qualities, attributes):
    """
    Calculate the results based on the given features, qualities, and attributes.

    Parameters:
    - features (list): A list of feature names.
    - qualities (list): A list of quality values.
    - attributes (list): A list of attribute values.

    Returns:
    - pandas.DataFrame: A DataFrame containing the calculated results with columns:
        - feature_name: The feature names.
        - attribute: The attribute values.
        - quality: The quality values.
        - novelty: The calculated novelty values.
        - area: The calculated area values.
        - quarter: The calculated quarter values.

    Raises:
    - ValueError: If the number of features, qualities, and attributes is not the same.
    """

    if len(features) != len(qualities) or len(features) != len(attributes):
        raise ValueError("The number of features, qualities, and attributes must be the same.")

    novelties = []
    areas = []
    quarter = []

    for quality, attribute in zip(qualities, attributes):
        novelty, area = calculate_area(quality, attribute)
        novelties.append(novelty)
        areas.append(area)

        if quality > 0:
            if novelty > 0:
                quarter.append('Q1')
            else:
                quarter.append('Q2')
        else:
            if novelty > 0:
                quarter.append('Q4')
            else:
                quarter.append('Q3')

    results = {'feature_name': features, 'attribute': attributes,
               'quality': qualities, 'novelty': novelties, 'area': areas, 'quarter': quarter}
    return pd.DataFrame(results)