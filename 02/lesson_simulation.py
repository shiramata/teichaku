import random
import numpy as np
from agent import Agent
import pandas as pd
import os

class Simulation:
    def __init__(self, population):
        self.agents = self.__generate_agents(population)
        self.population = population
        self.hawks_ratios = [(1/population)]
        self.doves_ratios = [(population-1)/population]
        self.cwd = os.path.dirname(os.path.abspath(__file__))

    def __generate_agents(self, population):
        initial_strategies = ['Hawk']
        initial_strategies.extend(['Dove'] * (population-1))
        random.shuffle(initial_strategies)
        return [Agent(index=i, strategy=initial_strategies[i]) for i in range(population)]

    def __battle(self, V, C):

        for i in range(0, self.population, 2):
            focal1 = self.agents[i]
            focal2 = self.agents[i+1]
            if focal1.strategy == 'Hawk' and focal2.strategy == 'Hawk':
                focal1.points = V
                focal2.points = -C
            elif focal1.strategy == 'Hawk' and focal2.strategy == 'Dove':
                focal1.points = V
                focal2.points = 0
            elif focal1.strategy == 'Dove' and focal2.strategy == 'Hawk':
                focal1.points = 0
                focal2.points = V
            elif focal1.strategy == 'Dove' and focal2.strategy == 'Dove':
                focal1.points = V
                focal2.points = 0

    def __calculate_fitness(self):
        avg = np.mean([x.points for x in self.agents])

        for focal in self.agents:
            focal.judge_reproductive(avg=avg)

        reproducers = [x for x in self.agents if x.reproductive == True]
        hawks_ratio = len([x for x in reproducers if x.strategy == 'Hawk']) / len(reproducers)
        print(len(reproducers))

        self.hawks_ratios.append(hawks_ratio)
        self.doves_ratios.append(1-hawks_ratio)

        return hawks_ratio

    def __make_next_generation(self, hawks_ratio):
        strategies = ['Hawk'] * int(self.population*hawks_ratio)
        strategies.extend(['Dove'] * (self.population - int(self.population*hawks_ratio)))
        random.shuffle(strategies)
        self.agents = [Agent(index=i, strategy=strategies[i]) for i in range(self.population)]


    def run_one_episode(self, episode, V, C):
        for _ in range(100):
            self.__battle(V, C)
            hawks_ratio = self.__calculate_fitness()
            self.__make_next_generation(hawks_ratio=hawks_ratio)

        pd.DataFrame({
            'Hawk': self.hawks_ratios,
            'Dove': self.doves_ratios
        }).to_csv(os.path.join(self.cwd, 'result', f'episode_{episode}.csv'))

















