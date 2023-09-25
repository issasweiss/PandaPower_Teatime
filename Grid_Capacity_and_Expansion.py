import pandapower as pp
import pandapower.plotting as plot
import pandas as pd
import pandapower.networks as nw
import matplotlib.pyplot as plt
from numpy.random import choice
from numpy.random import normal
import seaborn as sns
import copy
from pandapower.plotting.plotly import simple_plotly


def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() >= 100:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() >= 100:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.04:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)

def chose_bus(net):
    return choice(net.sgen.bus.values)


def get_plant_size_mw():
    return normal(loc=0.5, scale= 0.05)

def load_network():
    return nw.mv_oberrhein(scenario="generation")

iterations = 10
results = pd.DataFrame(columns=["installed", "violation"])

def get_max_expansion():
    for i in range(iterations):
        net = load_network()
        net_copy = copy.deepcopy(net)
        installed_mw = 0
        total_cost = 0
        while 1:
            violated, violation_type = violations(net_copy)
            if violated or total_cost >= 3e6:
                results.loc[i] = [installed_mw, violation_type]
                break
            else:
                plant_size = .050  # MW
                pp.create_load(net_copy, chose_bus(net_copy), p_mw=plant_size, controllable=False)
                installed_mw += plant_size
                total_cost = installed_mw * 6e6

    return total_cost, installed_mw

def static_generation_capacity():
    for i in range(iterations):
        net = load_network()
        net_copy = copy.deepcopy(net)
        installed_mw = 0
        while 1:
            violated, violation_type = violations(net_copy)
            if violated:
                results.loc[i] = [installed_mw, violation_type]
                break
            else:
                plant_size = get_plant_size_mw()
                pp.create_sgen(net_copy, chose_bus(net_copy), p_mw=plant_size, q_mvar=0)
                installed_mw += plant_size

    plt.rc('xtick', labelsize=18)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)  # fontsize of the tick labels
    plt.rc('legend', fontsize=18)  # fontsize of the tick labels
    plt.rc('axes', labelsize=20)  # fontsize of the tick labels
    plt.rcParams['font.size'] = 20

    sns.set_style("whitegrid", {'axes.grid': False})
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    ax = axes[0]
    sns.boxplot(results.installed, width=.1, ax=ax, orient="v")
    ax.set_xticklabels([""])
    ax.set_ylabel("Installed Capacity [MW]")

    ax = axes[1]
    ax.axis("equal")
    results.violation.value_counts().plot(kind="pie", ax=ax, autopct=lambda x: "%.0f %%" % x)
    ax.set_ylabel("")
    ax.set_xlabel("")
    sns.despine()
    plt.tight_layout()

    return plt.show(), print(results.installed.mean())


def plotting():
    net = load_network()
    return simple_plotly(net)

#static_generation_capacity()

#result was 10.64 MW for static generation capacity expansion

plotting()

static_generation_capacity()

# randomly choosing a line replacement and power2gas because of the limited time.