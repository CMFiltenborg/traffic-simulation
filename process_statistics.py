import pandas as pd
import os


def read_data(type):
    path = "./results/type_{}".format(type)
    if not os.path.isdir(path):
        return

    for file in os.listdir(path):
        if file.endswith(".csv"):
            data = pd.read_csv('{}/{}'.format(path, file))
            yield data


data = read_data(0)
print([d for d in data])
