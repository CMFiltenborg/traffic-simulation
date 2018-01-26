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
    dataframes = read_data(0)
    base = next(dataframes)
    for df in dataframes:
        base = base.append(df)

    groups = base.groupby(['hour'])
    for group_name,group in groups:
            plt.scatter(group['density'], group['total_average_speed'])
    plt.show()


plot_density_flow(0)
dataframes = read_data(0)
#print([d for d in dataframes][0])
