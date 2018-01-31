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


# calculates the CI per hour / sim = 0 or 2
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

# Makes a plot of the average speed over all sections per hour with errorbar.
def plot_speed_averages_errorbar(path, rest_paths=None, yrange=[0,100], plot_labels=["Original", "New"]*10, labelheight=0.3, scalefactor=[1]*100,
                        sections=['total_average_speed', 'total_average_speed']*10, colors=['blue', 'red']*10, image=None, yerr1=None, yerr2 = None):
    df = pd.read_csv(path)
    # Plot the total average speed.
    if image != None:
        f, (left, right) = plt.subplots(1,2, figsize=(20,7))
    else:
        f, left = plt.subplots(1,1)
    i = 1
    if rest_paths != None:
        for path2 in rest_paths:
            print(path2)
            df2 = pd.read_csv(path2)
            if yerr2 == None:
                yerr2 = [0]*(len(df2[sections[i]]))
            print(len(df2['total_average_speed']), len(yerr2))
            left.errorbar(range(24), df2[sections[i]]*20*scalefactor[i], yerr=yerr2, color=colors[i], label=plot_labels[i], linestyle='--', marker='o')
            i += 1
    if yerr1 == None:
        yerr1 = [0]*(len(df[sections[0]]))
    left.errorbar(range(24), df[sections[0]]*20*scalefactor[0], yerr=yerr1, color=colors[0], label=plot_labels[0], linestyle='--', marker='o')
    left.plot(range(25), [0]*25, color='black', linestyle=':')
    left.set_xlim(0,24)
    left.set_ylim(yrange[0],yrange[1])
    left.set_xlabel("hours")
    left.set_ylabel("speed")
    left.legend(bbox_to_anchor=(0, labelheight), loc=2, borderaxespad=0.)
    if image != None:
        image = mpimg.imread(image[0])
        right.imshow(image)
        right.set_xticks([])
        right.set_yticks([])
    plt.show()

#def overlap():
#    samples(0)

variantie1 = samples(0)
variantie1 = list(variantie1.values())
variantie2 = samples(2)
variantie2 = list(variantie2.values())
variantie1low = []
variantie1high = []
variantie2low = []
variantie2high = []
for i in range(24):
    variantie1low.append(variantie1[i][0])
    variantie1high.append(variantie1[i][1])
    variantie2low.append(variantie2[i][0])
    variantie2high.append(variantie2[i][1])
plot_speed_averages_errorbar('./results/averages_type_2.csv', ['./results/averages_type_0.csv'], colors=['red', 'blue'], plot_labels=["New simulated","Original simulated"], yerr1=[variantie1low, variantie1high], yerr2=[variantie2low, variantie2high])

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
    
