import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import stats


def plot_graph(n_points=100):
    """
    Plots a graph showing the relationship between novelty and quality.

    Parameters:
    - n_points (int): The number of points to generate on the x-axis.

    Returns:
    - fig (matplotlib.figure.Figure): The generated figure.
    - ax (matplotlib.axes.Axes): The generated axes.
    """

    # Create background graph
    x = np.linspace(-6, 6, n_points)
    y_mb = [i - 1 / i if i < 0 else np.nan for i in x]
    y_lq = x
    y_att = [i - 1 / i if i > 0 else np.nan for i in x]
    graph = pd.DataFrame({'x': x, 'must-be': y_mb, 'linear-quality': y_lq, 'attractiveness': y_att})

    plt.figure(figsize=(16 / 2.54, 16 / 2.54))
    sns.lineplot(x='x', y='must-be', data=graph, label='Must Be', color='red')
    sns.lineplot(x='x', y='linear-quality', data=graph, label='Linear Quality', color='orange')
    sns.lineplot(x='x', y='attractiveness', data=graph, label='Attractiveness', color='green')

    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

    plt.xlim(-6, 6)
    plt.ylim(-6, 6)

    plt.xticks(np.arange(-6, 7, 1))
    plt.yticks(np.arange(-6, 7, 1))

    plt.xlabel('Novelty')
    plt.ylabel('Quality')
    plt.legend()
    plt.grid(True)

    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(2)

    return plt.gcf(), ax


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

    plot_graph()
    for index, row in results.iterrows():
        quality = row['quality']
        attribute = row['attribute']
        novelty = row['novelty']
        area = row['area']
        quarter = row['quarter']
        feature_name = row['feature_name']
        color = 'orange' if attribute == 'LQ' else 'red' if attribute == 'MB' else 'green'
        hatch = '+' if attribute == 'LQ' else '\\'

        # Plot each point
        if legend == True:
            plt.scatter(novelty, quality, color=color,
                        label=f'{feature_name}\nN = {novelty:.2f}\nQ = {quality:.2f}\nA = {area:.2f}')
            plt.legend()
        else:
            plt.scatter(novelty, quality, color=color)
        square = patches.Rectangle((0, 0), novelty, quality, hatch=hatch, fill=False, color=color, linewidth=0.5)
        plt.gca().add_patch(square)

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
