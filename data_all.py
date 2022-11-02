import json
import os
import os.path
import numpy as np
from pprint import pformat
import statistics
import click
from matplotlib import pyplot as plt
from igor.binarywave import load as loadibw
import ibw


def extract_data(path):
    data = loadibw(path)
    wave = data['wave']
    values = np.nan_to_num(wave['wData']).tolist()
    del data['wave']['wData']
    return data, values


def plot_data_mod(values, values_, total_time, list2=None, subplot=False):
    if not subplot:

        if values is not None:
            listxachs = np.linspace(0, total_time, len(values))
            plt.plot(listxachs, values, linewidth=0.3, color="blue", label='Baseline')
        if values_ is not None:
            listxachs = np.linspace(0, total_time, len(values_))
            plt.plot(listxachs, values_, linewidth=0.3, color="red", label='LSD')
        if list2 is not None:
            plt.plot(listxachs, list2, linewidth=0.3, color="blue", label="last")
        plt.xlabel("Time [min]",
                   family='serif',
                   color='black',
                   weight='normal',
                   size=10,
                   labelpad=5)
        plt.ylabel("Voltage [mV]",
                   family='serif',
                   color='black',
                   weight='normal',
                   size=10,
                   labelpad=5)
        plt.legend()
        # x = np.array([listxachs])
        # plt.xticks(np.arange(min(listxachs), max(listxachs)+1), 1)
        # plt.xlim(0, 15600040)
        # scale_factor = 1/20
        # xmin, xmax = plt.xlim()
        # plt.xlim(xmin * scale_factor, xmax * scale_factor)
        # plt.savefig('graph.png', dpi=300, bbox_inches='tight')
        # path = path.replace('ibw', 'png')
        # path = path.replace('input', 'output')  # input, ouput = foldernames
        # plt.savefig(f'{path}')  # only if you want to safe it
    else:
        plt.rcParams['figure.figsize'] = (10,7)
        fig, axs = plt.subplots(1, 2)
        # Subplots only make sense if both are present
        listxachs = np.linspace(0, total_time, len(values))
        axs[0].plot(listxachs, values, linewidth=0.3, color="blue", label='Baseline')
        axs[0].legend()
        axs[1].plot(listxachs, values_, linewidth=0.3, color="red", label='LSD')
        axs[1].legend()
        axs[0].set_xlabel("Time [min]",
                          family='serif',
                          color='black',
                          weight='normal',
                          size=10,
                          labelpad=5)
        axs[1].set_xlabel("Time [min]",
                          family='serif',
                          color='black',
                          weight='normal',
                          size=10,
                          labelpad=5)

        axs[0].set_ylabel("Voltage [mV]",
                          family='serif',
                          color='black',
                          weight='normal',
                          size=10,
                          labelpad=5)

    plt.suptitle('L5 Recording')
    plt.show()


def run(path, joined, plot=True, store=False):
    # Extract complete data and values
    data, values = extract_data(path)

    print("joined: ", joined)

    stacks = len(values[0])
    lists = len(values)
    DT = 5 * 10 ** -5

    seconds = lists * DT
    time = seconds / 60

    print(f"Elements in list: {stacks} \nNumber of lists: {lists}")

    flat_lists = [list() for x in range(stacks)]
    for l in values:
        for i in range(stacks):
            flat_lists[i].append(l[i])
    joined_lists = []
    total_time = 0
    listsofaverage = []
    for i in range(len(flat_lists)):
        joined_lists += flat_lists[i]
        total_time += time
        listsofaverage.append(sum(flat_lists[i]) / len(flat_lists[i]))

    print("Recording time :", total_time)

    np_flat_lists = np.array(flat_lists)
    for i in range(len(np_flat_lists)):
        np_flat_lists[i] = np.array(np_flat_lists[i])
    averages = np.mean(np_flat_lists, axis=0)

    return averages, time


lsd = False
layer_1 = False

baseline_data_files = {"Data/input/l5_baseline_1207_t15Soma.ibw", "Data/input/l5_baseline_1207_t7Soma.ibw",
                       "Data/input/l5_baseline_2207_t24Soma.ibw",
                       "Data/input/l5_baseline_2207_t10Soma.ibw"}
# L5 baseline

baseline_data_files = {"Data/input/l5_baseline_2505_t6Soma.ibw"}

baseline_data_files={"Data/input/l1_baseline_2705_t7Soma.ibw", "Data/input/l1_baseline_2705_t8Soma.ibw"
                                                               ,"Data/input/l1_baseline_2705_t9Soma.ibw"}

l5_baseline_agg = np.zeros(40001)
baseline_counter = len(baseline_data_files)
for path_ in baseline_data_files:
    averages_, time_ = run(path=path_, joined='average')
    l5_baseline_agg += averages_

#averages_, time_ = run(path="Data/input/l5_baseline_1207_t7Soma.ibw", joined='average')
#l5_baseline_agg += averages_

#averages_, time_ = run(path="Data/input/l5_baseline_2207_t24Soma.ibw", joined='average')
#l5_baseline_agg += averages_

#averages_, time_ = run(path="Data/input/l5_baseline_2207_t10Soma.ibw", joined='average')
#l5_baseline_agg += averages_

# averages_, time_ = run(path="Data/input/l5_baseline_2906_t14Soma.ibw", joined='average')
# l5_baseline_agg += averages_

# averages_, time_ = run(path="Data/input/l5_baseline_2906_t12Soma.ibw", joined='average')
# l5_baseline_agg += averages_


# LSD  L5

lsd = True

lsd_data_files = {"Data/input/l5_lsd_1207_t23Soma.ibw", "Data/input/l5_lsd_2207_t11Soma.ibw",
                  "Data/input/l5_lsd_2906_t16Soma.ibw"}

lsd_counter = len(lsd_data_files)

l5_lsd_agg = np.zeros(40001)

averages_, time_ = run(path="Data/input/l5_lsd_1207_t23Soma.ibw", joined='average')
l5_lsd_agg += averages_

averages_, time_ = run(path="Data/input/l5_lsd_2207_t11Soma.ibw", joined='average')
l5_lsd_agg += averages_

averages_, time_ = run(path="Data/input/l5_lsd_2906_t16Soma.ibw", joined='average')
l5_lsd_agg += averages_

# Plot everything at the end

#plot_data_mod(l5_baseline_agg / 4, l5_lsd_agg / 3, time_, subplot=False)

plot_data_mod(l5_baseline_agg/baseline_counter,  None, time_, subplot=False)

