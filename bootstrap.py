import pandas as pd
import os
import matplotlib.pyplot as plt
from process_statistics import read_data
import numpy as np, scipy.stats as st


def bootstrap(type):
    dataframes = read_data(type)
    base = next(dataframes)
    for df in dataframes:
        base = base.append(df)

    groups = base.groupby(['hour'])    
    return groups


# calculates the CI per hour / sim = 0 or 1
def samples(sim):
    lijst_ci = {}
    samples = {}
    g0 = bootstrap(sim)
    for hour, group in g0:
        samples[hour] = group.sample(10**5,replace = True)
    for hour in samples: 
        speeds = samples[hour]['total_average_speed']
        conf = st.t.interval(0.95, len(speeds)-1, loc=np.mean(speeds), scale=st.sem(speeds))
        lijst_ci[hour] = conf
    return lijst_ci

#def overlap():
#    samples(0)


#print(samples(0)[0][0])
#samples(0)

# def dependant():
#     ci_0 = samples(0)
#     ci_2 = samples(2)
#     for hours in range():
#         if (ci_0[hours][0] > ci_2[hours][0] and ci_0[hours][0] < ci_2[hours][1]) or (ci_0[hours][1] > ci_2[hours][0] and ci_0[hours][1] < ci_2[hours][1]):
#             print("de datasets op", hour ,"zijn onafhankelijk")
#         else:
#             print("de datasets op", hour ,"zijn afhankelijk")
    
