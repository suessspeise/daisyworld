# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import math
import random

class DaisyModel(Model):
    """ "Daisys" grow, when the temperature is right. But they influence temperature themselves via their ability to block a certain amount of sunlight (albedo, indicated by color). They spread and they mutate (changing albedo) and thus adapt to different conditions."""
    def __init__(self, N, width, height, luminosity, heat_radius, mutation_range, surface_albedo, daisy_lifespan, daisy_tmin, daisy_tmax):
        # Setup parameter
        self.dimensions = (width, height)
        self.running = True # never stop!
        self.num_agents = min([N, (width * height)]) # never more agents than cells
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        # Model parameter
        self.mutation_range = mutation_range # default: 0.05
        self.luminosity = luminosity # default 1.35
        self.heat_radius = heat_radius
        self.surface_albedo = surface_albedo # default: 0.4
        # Daisy parameter
        self.daisy_lifespan = daisy_lifespan
        self.daisy_tmin = daisy_tmin
        self.daisy_tmax = daisy_tmax

        # to inhibit using same postition twice: draw from urn
        position_list = []
        for i in range(width): # put positions in urn
            for j in range(height):
                position_list.append((i,j))
        for i in range(self.num_agents): # draw from urn
            a = DaisyAgent(i, self, 
                            random.uniform(0.1, 0.9), # random starting albedo
                            self.daisy_lifespan, self.daisy_tmin, self.daisy_tmax)
            self.schedule.add(a)
            pos = random.choice(position_list)
            self.grid.place_agent(a, pos)
            position_list.remove(pos)

    def step(self):
        self.schedule.step()
        

    def get_lat(self, pos):
        """ The grid is meant to be a sphere. This gets the latitude. Ranges from 0.0 (equator) to 1.0 (pole).  """
        return (pos[1] / self.dimensions[1])

    def get_GNI(self, pos):
        """ gives solar irradiance, depending on latitude"""
        return self.luminosity * math.sin(self.get_lat(pos)*math.pi)

    def expand_positionlist(self, pos_list):
        """ expands a list of positions, adding neighboring positions  """
        expanded_list = []
        for i in pos_list:
            expanded_list += self.grid.get_neighborhood(i, moore=True, include_center=False)
        return list(set(expanded_list))

    def get_local_heat(self, pos):
        """ Global Horizontal Irradiance (without diffusive irradiance) from pole (lower border) to pole (upper border). model is torus! """
        neighborhood = self.grid.get_neighborhood(pos, moore=True, include_center=True)
        
        if self.heat_radius > 1: # if radius of local temperature is >1, this expand the position list.
            for i in range(self.heat_radius):
                neighborhood = self.expand_positionlist(neighborhood)

        heat = []
        for i in neighborhood:
            if self.grid.is_cell_empty(i): # empty cell: surface albedo
                heat.append(self.get_GNI(pos) * (1 - self.surface_albedo) )
            else:
                inhabitant = self.grid.get_cell_list_contents(i)[0] 
                heat.append(self.get_GNI(pos) * (1 - inhabitant.albedo) ) # cell with daisy
        return sum(heat)/ len(neighborhood)




class DaisyAgent(Agent):
    """ A Daisy. """
    def __init__(self, unique_id, model, albedo, life_span, tmin, tmax):
        super().__init__(unique_id, model)
        self.albedo = albedo
        self.life_span = life_span
        self.age = 0
        self.tmin = tmin
        self.tmax = tmax

    def die_or_live(self):
        # get local temperature
        local_heat =  self.model.get_local_heat(self.pos)
        temperature_stress = (local_heat > self.tmax) | (local_heat < self.tmin)

        if self.age > self.life_span: # too old 
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        elif temperature_stress: # too hot or too cold
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else: # just rigth, reproduce
            for i in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False):
                if self.model.grid.is_cell_empty(i) :
                    offspring = DaisyAgent(i, self.model, 
                                            random.uniform(max([0.1,self.albedo-self.model.mutation_range]), min([0.9, self.albedo+self.model.mutation_range])), # offspring inherits albedo, +- mutation_range, never out of bounds (0.1-0.9)
                                            self.life_span, self.tmin, self.tmax
                                            ) 
                    self.model.grid.place_agent(offspring, i)
                    self.model.schedule.add(offspring)

    def step(self):
        self.age += 1
        self.die_or_live()
