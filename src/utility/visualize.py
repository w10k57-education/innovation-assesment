"""
This module provides visualization utilities for analyzing and displaying innovation assessment data.

The module contains functions for creating different types of plots and visualizations:
- Relationship graphs between novelty and quality
- Normal distribution analysis plots
- Results visualization with scatter plots and area indicators
- Detailed results printing with quadrant analysis

Functions:
    plot_graph(n_points=100): Creates a base graph showing novelty-quality relationships
    plot_normal(series): Visualizes distribution analysis of a data series
    plot_results(results, legend=False): Plots assessment results with points and areas
    print_results(data): Prints detailed analysis of assessment results by quadrants

The visualizations are primarily focused on innovation assessment analysis, showing
relationships between novelty and quality across different attribute categories (Must Be,
Linear Quality, and Attractiveness) and helping identify effective and ineffective
innovations across different quadrants.

Dependencies:
    - matplotlib
    - numpy
    - pandas
    - seaborn
    - scipy.stats
"""
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


def plot_graph(n_points=100):
    """
    Plots a graph showing the relationship between novelty and quality, and returns the figure
    and axes for further customization.

    Parameters:
    - n_points (int): The number of points to generate on the x-axis.

    Returns:
    - fig (matplotlib.figure.Figure): The generated figure.
    - ax (matplotlib.axes.Axes): The axes of the plot.
    """
    # Generate x values and corresponding y values for the relationships
    x = np.linspace(-6, 6, n_points)
    y_mb = [i - 1 / i if i < 0 else np.nan for i in x]  # Must-be relationship
    y_lq = x  # Linear quality relationship
    y_att = [i - 1 / i if i > 0 else np.nan for i in x]  # Attractiveness relationship

    # Create a DataFrame for easy plotting
    graph = pd.DataFrame({'x': x, 'must-be': y_mb, 'linear-quality': y_lq, 'attractiveness': y_att})

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(16 / 2.54, 16 / 2.54))  # Size in inches

    # Plot data
    sns.lineplot(x='x', y='must-be', data=graph, label='Must Be', color='red', ax=ax)
    sns.lineplot(x='x', y='linear-quality', data=graph, label='Linear Quality', color='orange', ax=ax)
    sns.lineplot(x='x', y='attractiveness', data=graph, label='Attractiveness', color='green', ax=ax)

    # Draw x and y axes lines at 0
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')

    # Set axes limits and ticks
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_xticks(np.arange(-6, 7, 1))
    ax.set_yticks(np.arange(-6, 7, 1))

    # Label axes
    ax.set_xlabel('Novelty')
    ax.set_ylabel('Quality')

    # Enhance grid and spines
    ax.grid(True)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(2)

    return fig, ax


def plot_normal(series):
    """
    Plots the data distribution of a series along with a normal distribution fit and a probability plot.

    Parameters:
    series (array-like): The input series to be visualized.

    Returns:
    None
    """

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Plot histogram with normal distribution fit
    sns.histplot(series, kde=True, stat="density", ax=axes[0])
    mu, std = stats.norm.fit(series)
    xmin, xmax = np.min(series), np.max(series)
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    axes[0].plot(x, p, 'k', linewidth=2)
    axes[0].set_title("Data distribution with normal fit")

    # Plot probability plot
    stats.probplot(series, plot=axes[1])
    axes[1].grid(True)
    axes[1].set_title("Probability Plot")

    plt.tight_layout()

    return fig, axes


def plot_results(results, legend=False):
    """
    Plot the results of a data analysis.

    Parameters:
    results (DataFrame): The results of the analysis.
    legend (bool, optional): Whether to display a legend. Defaults to True.
    """

    _, ax = plot_graph()
    for _, row in results.iterrows():
        quality = row['quality']
        attribute = row['attribute']
        novelty = row['novelty']
        area = row['area']
        feature_name = row['feature_name']
        color = 'orange' if attribute == 'LQ' else 'red' if attribute == 'MB' else 'green'
        hatch = '+' if attribute == 'LQ' else '\\'

        # Correctly plot each point using the ax object, without reassigning ax
        label = f'{feature_name}: N={novelty:.2f}, Q={quality:.2f}, A={area:.2f}' if legend else None
        ax.scatter(novelty, quality, color=color, label=label)

        # Create a rectangle patch and add it to the ax object
        square = patches.Rectangle((0, 0), width=novelty, height=quality,
                                hatch=hatch, fill=False, color=color, linewidth=0.5)
        ax.add_patch(square)

    # Configure legend if needed
    if legend:
        ax.legend()

    plt.show()


def print_results(data):
    """
    Prints the results of the assessment for a given product.

    Parameters:
    data (dict): A dictionary containing the assessment data for a product.

    Returns:
    None
    """
    print('-' * 80 + '\n')
    print(pd.DataFrame(data))
    print('\n' + '-' * 80 + '\n')
    plot_results(data)
    print('\n' + '-' * 80 + '\n')

    # Find the biggest areas in each quadrant
    quadrant1 = data[data['quarter'] == 'Q1']
    quadrant2 = data[data['quarter'] == 'Q2']
    quadrant3 = data[data['quarter'] == 'Q3']
    quadrant4 = data[data['quarter'] == 'Q4']

    # Find the feature name and quality of the biggest areas in each quadrant
    max_area1 = quadrant1[quadrant1['area'] == quadrant1['area'].max()]
    max_area2 = quadrant2[quadrant2['area'] == quadrant2['area'].max()]
    max_area3 = quadrant3[quadrant3['area'] == quadrant3['area'].max()]
    max_area4 = quadrant4[quadrant4['area'] == quadrant4['area'].max()]

    # Print the feature name and quality of the biggest areas in each quadrant
    print(
        "Effective innovation:\nFeature Name =", max_area1['feature_name'].values[0],
        ", Quality =", max_area1['quality'].values[0])
    print('Features in Q1: ', quadrant1['feature_name'].values)
    print('*' * 80)
    print("Standard solutions area:\nFeature Name =",
          max_area2['feature_name'].values[0], ", Quality =", max_area2['quality'].values[0])
    print('Features in Q2: ', quadrant2['feature_name'].values)
    print('*' * 80)
    print(
        "Design error field:\nFeature Name =", max_area3['feature_name'].values[0],
        ", Quality =", max_area3['quality'].values[0])
    print('Features in Q3: ', quadrant3['feature_name'].values)
    print('*' * 80)
    print("Ineffective innovation:\nFeature Name =",
          max_area4['feature_name'].values[0], ", Quality =", max_area4['quality'].values[0])
    print('Features in Q4: ', quadrant4['feature_name'].values)
