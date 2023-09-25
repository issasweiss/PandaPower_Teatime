import tempfile
import pandapower as pp
import pandapower.plotting as plot
import pandapower.networks as nw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL.Image import item
from pandapower.timeseries.output_writer import OutputWriter
import pandapower.topology as top
from pandapower.plotting.plotly import simple_plotly
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl
from pandapower.timeseries import DFData
import os.path
from openpyxl.workbook import Workbook

def time_series(output_dir):
    profiles, ds = create_data_source()
    time_steps = len(profiles.index)
    area_x_buses, area_x_lines, net_area1 = get_network_area()
    profiles, ds = create_data_source()
    create_controllers(net_area1, ds)

    create_output_writer(net_area1, output_dir=output_dir, profiles = profiles)
    run_timeseries(net_area1, time_steps)

    return print(profiles), print(net_area1)

def create_data_source():
    profiles = pd.read_csv("/Users/admin/Downloads/timeseries_exercise_5.csv", delimiter=";", index_col=0)

    ds = DFData(profiles)

    return profiles, ds

def create_controllers(net, ds):
    area_x_buses, area_x_lines , net_area1 = get_network_area()

    ConstControl(net, "load", variable='p_mw', element_index=net_area1.load.index,
                 data_source=ds, profile_name=["loads"])
    ConstControl(net,  "sgen" ,variable='p_mw' ,element_index=net_area1.sgen.index,
                 data_source=ds, profile_name=["sgens"])

def create_output_writer(net_area1, output_dir, profiles):

    time_steps = len(profiles.index)
    area_x_buses, area_x_lines , net_area1 = get_network_area()
    ow = OutputWriter(net_area1, time_steps = time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list())

    ow.log_variable('res_bus_max', 'vm_pu', index=area_x_buses, eval_function=np.max, eval_name="bus_max_vm_pu")
    ow.log_variable('res_bus_min', 'vm_pu', index=area_x_buses, eval_function=np.min, eval_name="bus_min_vm_pu")
    ow.log_variable('res_line', 'p_mw', index=area_x_lines, eval_function=np.max, eval_name="line_max_loading")
    return ow
def load_network():
    return pp.from_json("/Users/admin/Downloads/Excercises/net_exercise_5.json")

def get_network_area():
    net = load_network()
    mg = top.create_nxgraph(net, nogobuses={80}, include_lines=True, respect_switches=True)
    area_x_buses = list(top.connected_component(mg, bus=86))
    area_x_lines = list()
    for line in net.line.index:
        if net.line.from_bus.loc[line] in area_x_buses:
            area_x_lines.append(line)

    net_area1 = pp.select_subnet(net, area_x_buses)

    return area_x_buses, area_x_lines, net_area1

def plotting_area():
    net = load_network()
    area_x_buses, area_x_lines, net_area1 = get_network_area()

    bc = plot.create_bus_collection(net, net.bus.index, size=80, color="grey", zorder=3)
    bch = plot.create_bus_collection(net, area_x_buses, size=80, color="green", zorder=3)
    lcl = plot.create_line_collection(net, net.line.index, zorder=1, color="grey")
    sh = plot.create_bus_collection(net, [net.ext_grid.bus.loc[0]], patch_type="rect", size=200, color="green",zorder=11)
    lc = plot.create_line_collection(net, area_x_lines, zorder=2, color="green")

    plot.draw_collections([bc, bch, lc, lcl, sh], figsize=(8, 6))

    return plt.show()


def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() >= 100:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() >= 100:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.05 or net.res_bus.vm_pu.min() < 0.95:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)


def plot_timeseries(output_dir):
    # voltage results
    area_x_buses, area_x_lines , net_area1 = get_network_area()
    profiles = pd.read_csv("/Users/admin/Downloads/timeseries_exercise_5.csv", delimiter=";", index_col=0)
    create_output_writer(net_area1,"/Users/admin/Downloads/Excercises", profiles )
    vm_pu_file = os.path.join(output_dir, "res_bus_max", "vm_pu.xlsx")
    vm_pu = pd.read_excel(vm_pu_file, index_col=0)
    vm_pu.plot(label="vm_pu_max")
    plt.xlabel("time step")
    plt.ylabel("voltage mag. [p.u.]")
    plt.title("Maximum Voltage Magnitude")
    plt.grid()
    plt.show()

    # line loading results
    ll_file = os.path.join(output_dir, "res_line_min", "loading_percent.xlsx")
    line_loading = pd.read_excel(ll_file, index_col=0)
    line_loading.plot(label="vm_pu_min")
    plt.xlabel("time step")
    plt.ylabel("voltage mag. [p.u.]")
    plt.title("Minimum Voltage Magnitude")
    plt.grid()
    plt.show()

    # load results
    load_file = os.path.join(output_dir, "res_line", "p_mw.xlsx")
    load = pd.read_excel(load_file, index_col=0)
    load.plot(label="load")
    plt.xlabel("time step")
    plt.ylabel("P [MW]")
    plt.grid()
    plt.show()

    return

output_dir = os.path.join(tempfile.gettempdir(), "/Users/admin/Downloads/Excercises")
print("Results can be found in your local temp folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
#time_series(output_dir)
#plot_timeseries("/Users/admin/Downloads/Excercises")
#get_network_area()
#plotting_area()

#create_data_source()


plot_timeseries("/Users/admin/Downloads/timeseries_exercise_5.csv")