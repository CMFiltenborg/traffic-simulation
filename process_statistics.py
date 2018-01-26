import pandas as pd
import os


def read_data(type):
    path = "./results/type_{}".format(type)
    if not os.path.isdir(path):
        return

    for file in os.listdir(path):
        if file.endswith(".csv"):
            dataframe = pd.read_csv('{}/{}'.format(path, file))
            yield dataframe

def plot_density_flow(dataframes, type):
    dataframes = read_data(0)
    base = next(dataframes)
    for df in dataframes:
        base = base.append(df)

    group = base.groupby(['hour'])
    print(group['density'][:10])


def calculate_average_values(type):
    dataframes = read_data(type)
    counter = 1
    base = next(dataframes)
    for df in dataframes:
        base += df
        counter += 1

    average = base / counter

    print(average)
    base.to_csv('./results/averages_type_{}.csv')


def calculate_difference(path, path_other):
    if not os.path.isdir(path) or not os.path.isdir(path_other):
        raise Exception('Invalid paths provided...')

    df = pd.read_csv(path)
    df_other = pd.read_csv(path_other)

    difference = df - df_other
    print(difference)




calculate_average_values(0)