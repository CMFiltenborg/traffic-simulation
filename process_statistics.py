"""
Processes the files output by the statistics script.
Comment in/out the stats that you want to run (average, difference, etc)
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import matplotlib.colors as mcolors


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


def plot_density_flow():
    """
    Plots the density flow of the road
    """
    _, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
    #ax1.set_cmap(mpl.cm.rainbow)
    ax1.set_title("Original road")
    ax1.set_ylabel("Average speed")
    ax2.set_title("New road")
    ax2.set_xlabel("Average Density (cars/surface)")
    ax1.set_xlabel("Average Density (cars/surface)")

    norm = mcolors.Normalize(vmin=0, vmax=23)
    cmap = cm.jet

    '''
    cmap = mpl.cm.rainbow
    norm = mpl.colors.Normalize(vmin=0, vmax=23)
    cb1 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation="vertical")
    cb1.set_label("Hours")
    '''

    for i in [0, 2]:
        dataframes = read_data(i)
        base = next(dataframes)
        for df in dataframes:
            base = base.append(df)

        groups = base.groupby(['hour'])
        index =0
        for group_name,group in groups:
            if i == 0:
                ax1.scatter(group['density'], group['total_average_speed'], color=cmap(norm(index)))
            elif i == 2:
                ax2.scatter(group['density'], group['total_average_speed'], color=cmap(norm(index)))
            index += 1
    
    scalarmappaple = cm.ScalarMappable(norm=norm, cmap=cmap)
    scalarmappaple.set_array(index)
    l = plt.colorbar(scalarmappaple)
    l.set_label("Hour")
    plt.show()

# Makes a bar plot of the average speed over all sections per hour.
def plot_speed_averages(path, rest_paths=None, yrange=[0,100], plot_labels=["Original", "New"],
                        sections=['total_average_speed', 'total_average_speed'], colors=['blue', 'red'], image=None):
    df = pd.read_csv(path)
    # Plot the total average speed.
    if image != None:
        f, (left, right) = plt.subplots(1,2, figsize=(20,7))
    else:
        f, left = plt.subplots(1,1)
    i = 1

    if rest_paths != None:
        for path2 in rest_paths:
            df2 = pd.read_csv(path2)
            left.plot(range(24), df2[sections[i]]*20, color=colors[i], label=plot_labels[i], linestyle='--', marker='o')
            i += 1

    left.plot(range(24), df[sections[0]]*20, color=colors[0], label=plot_labels[0], linestyle='--', marker='o')
    left.plot(range(25), [0]*25, color='black', linestyle=':')
    left.set_xlim(0,24)
    left.set_ylim(yrange[0],yrange[1])
    left.set_xlabel("hours")
    left.set_ylabel("speed")
    left.legend(bbox_to_anchor=(0, 0.3), loc=2, borderaxespad=0.)
    if image != None:
        image = mpimg.imread(image[0])
        right.imshow(image)
        right.set_xticks([])
        right.set_yticks([])
    plt.show()

# Makes a bar plot of the percentage of cars that goes in the direction of Utrecht compared to
# the cars who stay on the beltway.
# Only works with type = 2
def plot_percentage_to_Utrecht(type):
    dataframes = read_data(type)
    combined = pd.concat(dataframes, axis=1, keys=range(101))
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


paths = [
    './results/averages_type_2.csv',
    './results/averages_type_2.csv',
    './results/averages_type_2.csv',
    './results/averages_type_2.csv',
    './results/averages_type_2.csv',
    './results/averages_type_2.csv',
    './results/averages_type_2.csv',
    './results/averages_type_2.csv'
]

sections = [
    'total_average_speed',
    'average_speed:R1',
    'average_speed:R2',
    'average_speed:R5',
    'average_speed:R6',
    'average_speed:R7',
    'average_speed:R8',
    'average_speed:R9',
    'average_speed:R10',
]

labels = [
    "Average",
    "R1",
    "R2",
    "R5",
    "R6",
    "R7",
    "R8",
    "R9",
    "R10"
]

colors = [
    'red',
    'blue',
    'black',
    'yellow',
    'cyan',
    'yellow',
    'cyan',
    'cyan',
    'green'
]

calculate_average_values(0)
calculate_average_values(2)AD
#plot_density_flow()
#plot_speed_averages(0)
#plot_density_flow(2)
plot_speed_averages('./results/averages_type_2.csv', paths, sections=sections, plot_labels=labels, colors=colors, image=['./new_road_with_names.png'])
plot_speed_averages('./results/difference.csv', yrange=[-50,50], plot_labels=["Difference"])
<<<<<<< HEAD
plot_speed_averages('./results/averages_type_0.csv', ['./results/averages_type_2.csv'])
=======
>>>>>>> cfb9d06b0bb4cea9ab33f595a2c25836c8e2fd2e
>>>>>>> 9acb2542b34613aa3578e2edcbe034d2122525fa
#plot_percentage_to_Utrecht(2)

calculate_difference('./results/averages_type_2.csv', './results/averages_type_0.csv')