import pandapower as pp
import pandapower.plotting as plot
import pandas as pd
import pandapower.networks as nw
import matplotlib.pyplot as plt

net = nw.mv_oberrhein(scenario="generation")

# Scaling

def scaling(net):
    net.sgen["scaling"] = 2
    pp.runpp(net)
    return net

def checking_overload(net):
    overloaded_lines = net.res_line[net.res_line.loading_percent >= 100].index
    for i in overloaded_lines:
        g = pp.find_std_type_by_parameter(net, data={"max_i_ka": net.res_line.i_ka.loc[i]}, epsilon=0.05)
        if len(g) == 0:
            print("no cable found")
        else:
            pp.change_std_type(net, i, g[0], element="line")
    pp.runpp(net)
    return net

def plotting(net):
    lines_list = [(0, "green"), (100, "yellow"), (101, "red")]
    cmap_line, norm_line = plot.cmap_continuous(lines_list)
    lc_line = plot.create_line_collection(net, net.line.index, zorder=1, cmap=cmap_line, norm=norm_line, linewidths=2)

    buses_list = [(0.95, "blue"), (1, "green"), (1.05, "purple")]
    cmap_bus, norm_bus = plot.cmap_continuous(buses_list)
    lc_bus = plot.create_bus_collection(net, net.bus.index, zorder=2, cmap=cmap_bus, norm=norm_bus)

    plot.draw_collections([lc_line,lc_bus], figsize=(8, 6))

    return plt.show()



net = scaling(net)
net = checking_overload(net)
plotting(net)
