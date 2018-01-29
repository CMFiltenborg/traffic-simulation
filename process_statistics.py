"""
Processes the files output by the statistics script.
Comment in/out the stats that you want to run (average, difference, etc)
"""

import pandas as pd
import os
import matplotlib.pyplot as plt


def read_data(road_type):
    """
    Reads the results from several simulation runs into a list of dataframes
    :param road_type: Type of road
    :return: List of panda dataframes
    """
    path = "./results/type_{}".format(road_type)
    if not os.path.isdir(path):
        return

    for file in os.listdir(path):
        if file.endswith(".csv"):
            dataframe = pd.read_csv('{}/{}'.format(path, file))
            yield dataframe


def plot_density_flow(road_type):
    """
    Plots the density flow of the road
    :param road_type: Road Type
    """
    dataframes = read_data(road_type)
    base = next(dataframes)
    for df in dataframes:
        base = base.append(df)

    groups = base.groupby(['hour'])
    for group_name,group in groups:
            plt.scatter(group['density'], group['total_average_speed'])
    plt.show()

# Makes a bar plot of the average speed over all sections per hour.
def plot_speed_averages(type):
    dataframes = read_data(type)
    combined = pd.concat(dataframes, axis=1, keys=range(4))
    combined = combined.swaplevel(0,1,axis=1).sortlevel(axis=1)
    combined = combined.groupby(level=0,axis=1).mean()
    plt.bar(range(24), combined['total_average_speed']*20, width=0.9, color='blue')
    plt.xlim(0,24)
    plt.ylim(0,100)
    plt.show()

# Makes a bar plot of the percentage of cars that goes in the direction of Utrecht compared to
# the cars who stay on the beltway.
# Only works with type = 2
def plot_percentage_to_Utrecht(type):
    dataframes = read_data(type)
    combined = pd.concat(dataframes, axis=1, keys=range(2))
    combined = combined.swaplevel(0,1,axis=1).sortlevel(axis=1)
    combined = combined.groupby(level=0,axis=1).mean()
    plt.bar(range(24), combined['%_to_Utrecht']*100, width=0.9, color='blue')
    real_data = pd.read_csv('%_to_Utrecht_real.csv')
    y = real_data['%_to_Utrecht'].astype(float)
    plt.plot(range(24), y, color='red')
    plt.xlim(0,24)
    plt.ylim(0,100)
    plt.show()


def calculate_average_values(road_type):
    """
    Creates a dataframe of the average values from the list of dataframes of multiple simulations
    """
    dataframes = read_data(road_type)
    counter = 1
    base = next(dataframes)
    for df in dataframes:
        base += df
        counter += 1

    average = base / counter
    average.to_csv('./results/averages_type_{}.csv'.format(road_type))


def calculate_difference(path, path_other):
    """
    Calculate difference between two result tables
    :param path: string file path
    :param path_other: string file path
    """
    if not os.path.exists(path) or not os.path.exists(path_other):
        raise Exception('Invalid paths provided...')

    df = pd.read_csv(path)
    df_other = pd.read_csv(path_other)

    common_columns = list(set(df.columns).intersection(set(df_other)))
    df = df[common_columns]
    df_other = df_other[common_columns]

    difference = df.subtract(df_other, fill_value=0)
    difference.to_csv('./results/difference.csv')

    summed_difference = difference.sum()
    summed_difference.to_csv('./results/summed_difference.csv')

    print(difference)
    print(difference.sum())


calculate_average_values(0)
calculate_average_values(2)
plot_density_flow(2)
plot_speed_averages(2)
plot_percentage_to_Utrecht(2)

# calculate_difference('./results/averages_type_2.csv', './results/averages_type_0.csv')