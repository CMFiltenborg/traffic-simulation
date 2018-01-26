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


dataframes = read_data(0)
#print([d for d in dataframes][0])
