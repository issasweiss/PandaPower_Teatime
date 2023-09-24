import pandapower as pp
import pandapower.plotting as plot
import pandas as pd

#create an empty network
net = pp.create_empty_network()

# create buses
bus0 = pp.create_bus(net, vn_kv=10, name="Bus0",type="b")
bus1 = pp.create_bus(net, vn_kv=0.4, name="Bus1",type="b")
bus2 = pp.create_bus(net, vn_kv=0.4, name="Bus2",type="b")
bus3 = pp.create_bus(net, vn_kv=0.4, name="Bus3",type="b")
bus4 = pp.create_bus(net, vn_kv=0.4, name="Bus4",type="b")
bus5 = pp.create_bus(net, vn_kv=0.4, name="Bus5",type="b")
bus6 = pp.create_bus(net, vn_kv=0.4, name="Bus6",type="b")

# create high-level elements
ex_grid = pp.create_ext_grid(net, bus=bus0, vm_pu=1, va_degree=0,name="Grid Connection")
trafo = pp.create_transformer(net, hv_bus=bus0, lv_bus=bus1, std_type="0.63 MVA 10/0.4 kV", name="Transformer")

# create lines
line1 = pp.create_line(net,from_bus=bus1, to_bus=bus2, length_km=0.72, std_type="NAYY 4x50 SE" )
line2 = pp.create_line(net,from_bus=bus2, to_bus=bus3, length_km=1.50, std_type="NAYY 4x50 SE" )
line3 = pp.create_line(net,from_bus=bus3, to_bus=bus4, length_km=0.30, std_type="NAYY 4x50 SE" )
line4 = pp.create_line(net,from_bus=bus1, to_bus=bus5, length_km=0.14, std_type="NAYY 4x50 SE" )
line5 = pp.create_line(net,from_bus=bus5, to_bus=bus6, length_km=0.17, std_type="NAYY 4x50 SE" )
line6 = pp.create_line(net,from_bus=bus6, to_bus=bus4, length_km=0.50, std_type="NAYY 4x50 SE" )

# create low-level elements
WKA1 = pp.create_sgen(net, bus=bus1,p_mw=.035, q_mvar=-.005, name="WKA", scaling=0.9 )
PV_B2 = pp.create_sgen(net, bus=bus2,p_mw=.002, q_mvar=-.0002, name="PV_B2", scaling=0.9 )
PV_B3 = pp.create_sgen(net, bus=bus3,p_mw=.010, q_mvar=0, name="PV_B3", scaling=0.9)
Load_B4 = pp.create_load(net, bus=bus4, p_mw=0.025, q_mvar=-0.005, name="Load_B4", scaling=0.5)
Load_B2 = pp.create_load(net, bus=bus2, p_mw=0.015, q_mvar=-0.010, name="Load_B4", scaling=0.8)
Load_B3 = pp.create_load(net, bus=bus3, p_mw=0.005, q_mvar=0.0001, name="Load_B4", scaling=0.8)
Load_B6 = pp.create_load(net, bus=bus6, p_mw=0.01378, q_mvar=0.00453, name="Load_B4")

Gen_Sync = pp.create_gen(net, bus=bus5, p_mw=0.1, vm_pu=1, name="Gen_Sync", scaling=0.43)
PV_B6 = pp.create_sgen(net, bus=bus6, p_mw=0.007, q_mvar=.001, name="PV_B6", scaling=0.9)
Switch = pp.create_switch(net, bus=bus4, element=line3, et="l", type="LBS", closed=False   , name="Switch")


data = { "x": [1.5, 1.5, 0.0, 0.0, 1.5, 3.0, 3.0],
         "y" : [0.0, -1.0, -2.0, -3.0, -4.0, -2.0, -3.0]
}

net.bus_geodata = pd.DataFrame(data)

plot.simple_plot(net)
pp.runpp(net)

print(net.res_bus.vm_pu.loc[4])
print(net.res_line.loading_percent.loc[3])
#print(net.bus_geodata)

