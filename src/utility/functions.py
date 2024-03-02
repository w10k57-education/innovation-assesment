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
    normalized_values = 2 * (values - mean) / std

    # Clip values to be within the range of -6 to 6
    rescaled = np.clip(normalized_values, -6, 6)

    if inversed:
        rescaled = -rescaled

    return rescaled


def calculate_results(product_no, df_value, df_attr):
    """
    Calculate the results for a given product number.

    Args:
        product_no (int): The product number.
        df_value (pandas.DataFrame): The dataframe containing the values.
        df_attr (dict): The dictionary containing the attributes.

    Returns:
        pandas.DataFrame: The calculated results.

    Raises:
        TypeError: If the product number is not an integer.
        ValueError: If the product number is out of range or a feature is not found in the attributes file.
    """

    if type(product_no) != int:
        raise TypeError('Product number must be an integer')
    if product_no not in range(len(df_value)):
        raise ValueError(f'Product number out of range. Please select an integer from 0 to {len(df_value)}]')

    features = []
    attributes = []
    qualities = []
    novelties = []
    areas = []
    quarter = []

    product = df_value.iloc[product_no]

    for col in df_value.columns:
        feature_name = col.split('_')[0]
        if feature_name in df_attr.keys():
            quality = product[col]
            attribute = df_attr[feature_name][0]
            novelty, area = calculate_area(quality, attribute)
            features.append(feature_name)
            attributes.append(attribute)
            qualities.append(round(quality, 3))
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
        else:
            raise ValueError(f'Feature {feature_name} not found in the attributes file')

    results = {'feature_name': features, 'attribute': attributes,
               'quality': qualities, 'novelty': novelties, 'area': areas, 'quarter': quarter}
    return pd.DataFrame(results)
