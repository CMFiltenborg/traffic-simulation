import pandas as pd
import os
import matplotlib.pyplot as plt


def read_data(type):
    path = "./results/type_{}".format(type)
    if not os.path.isdir(path):
        return

    for file in os.listdir(path):
        if file.endswith(".csv"):
            dataframe = pd.read_csv('{}/{}'.format(path, file))
            yield dataframe

def plot_density_flow(type):
    dataframes = read_data(type)
    base = next(dataframes)
    for df in dataframes:
        base = base.append(df)

    groups = base.groupby(['hour'])
    for group_name,group in groups:
            plt.scatter(group['density'], group['total_average_speed'])
    plt.show()


def calculate_average_values(type):
    dataframes = read_data(type)
    counter = 1
    base = next(dataframes)
    for df in dataframes:
        base += df
        counter += 1

    average = base / counter
    average.to_csv('./results/averages_type_{}.csv'.format(type))


def calculate_difference(path, path_other):
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


# calculate_average_values(0)
# calculate_average_values(2)
# plot_density_flow(0)

calculate_difference('./results/averages_type_2.csv', './results/averages_type_0.csv')