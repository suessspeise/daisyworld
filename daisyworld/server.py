# server.py
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter
from .model import DaisyModel
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
height = 100
width = 100

# Grid
grid = CanvasGrid(agent_portrayal, width, height, width*cell_size, height*cell_size)

# Chart
chart = ChartModule([{"Label": "Solar irradiance",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
chart2 = ChartModule([{"Label": "Population",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
chart3 = ChartModule([{"Label": "Mean albedo",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
chart4 = ChartModule([{"Label": "Population: North - South",
                      "Color": "Black"}],
                    data_collector_name='datacollector')


# (type, name, default, min, max, stepsize)
n_slider = UserSettableParameter('number', "global: Number of initial agents", default_agent_number, 1, int(width*height/1), 1) 
lum_slider = UserSettableParameter('number', "global: Solar irradiance", 1.35, 0.0, 2.0, 0.05) 
mutation_slider = UserSettableParameter('number', "Daisy: Range of mutation", 0.05, 0.0, 0.5, 0.01)
albedo_slider = UserSettableParameter('number', "global: surface albedo", 0.4, 0.0, 1.0, 0.1)
tmin_slider = UserSettableParameter('number', "Daisy: minimum temperature", 0.2, 0.0, 1.0, 0.1)
tmax_slider = UserSettableParameter('number', "Daisy: maximum temperature", 0.4, 0.0, 1.0, 0.1)
lifespan_slider = UserSettableParameter('number', "Daisy: lifespan", 10, 1, 100, 1)
range_slider = UserSettableParameter('slider', "global: Radius of Heat Integration", 2, 1, 10, 1)
lum_model = UserSettableParameter('choice', 'global: luminosity model', value='linear increase', choices=['stable', 'linear increase'])
lum_increase = UserSettableParameter('number', 'global: increment on luminosity', value=0.001)

server = ModularServer(DaisyModel,
                       [grid, chart, chart2, chart3, chart4],
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
                       "daisy_tmax": tmax_slider,
                       "lum_model" : lum_model,
                       "lum_increase" : lum_increase
                       })
