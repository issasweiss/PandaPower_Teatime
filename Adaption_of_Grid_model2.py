import pandapower as pp
import pandapower.plotting as plot
import pandas as pd
import json
from io import StringIO

net = pp.from_json("/Users/admin/Downloads/Excercises/net_exercise_2.json")

# Solving..

net.switch.closed.loc[55] = True
pp.create_line(net,from_bus=51, to_bus=52,length_km=1, std_type="NAYY 4x120 SE", name="LV Line2.2")
net.trafo.hv_bus.loc[1] = 41
net.trafo.lv_bus.loc[1] = 45
net.load["scaling"] = 0.001

pp.runpp(net)

print(net.res_line.loading_percent)
print(net.switch.loc[55])
#pp.runpp(net)
#pp.diagnostic(net)


