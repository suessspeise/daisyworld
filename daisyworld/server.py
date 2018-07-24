# server.py
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import DaisyModel
import matplotlib.pyplot as plt
import matplotlib.colors as col
cmap = plt.cm.get_cmap("viridis")

def agent_portrayal(agent):
    portrayal = {}
    portrayal["Shape"] = "rect"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["w"] = .9
    portrayal["h"] = .9
    portrayal["Color"] = col.rgb2hex(cmap(agent.albedo)[:3]) # color by albedo 
    return portrayal

# parameter
cell_size = 10
default_agent_number =  100
width = 30
height = width *3

grid = CanvasGrid(agent_portrayal, width, height, width*cell_size, height*cell_size)

# (type, name, default, min, max, stepsize)
n_slider = UserSettableParameter('slider', "Number of agents", default_agent_number, 1, int(width*height/1), 1) 
lum_slider = UserSettableParameter('slider', "Solar irradiance", 1.35, 0.0, 2.0, 0.05) 
mutation_slider = UserSettableParameter('slider', "Range of mutation", 0.05, 0.0, 0.5, 0.01)
albedo_slider = UserSettableParameter('slider', "Surface albedo", 0.4, 0.0, 1.0, 0.1)
tmin_slider = UserSettableParameter('slider', "Daisy: minimum temperature", 0.2, 0.0, 1.0, 0.1)
tmax_slider = UserSettableParameter('slider', "Daisy: maximum temperature", 0.4, 0.0, 1.0, 0.1)
lifespan_slider = UserSettableParameter('slider', "Daisy: lifespan", 10, 1, 100, 1)
range_slider = UserSettableParameter('slider', "Radius of Heat Integration", 2, 1, 10, 1)

server = ModularServer(DaisyModel,
                       [grid],
                       "DaisyWorld",
                       {"N": n_slider, 
                       "width": width, 
                       "height": height, 
                       "luminosity": lum_slider,
                       "heat_radius": range_slider, 
                       "mutation_range": mutation_slider, 
                       "surface_albedo": albedo_slider, 
                       "daisy_lifespan": lifespan_slider,
                       "daisy_tmin": tmin_slider,
                       "daisy_tmax": tmax_slider
                       })