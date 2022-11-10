from simulation import Simulation
import itertools
import numpy as np
import pandas as pd
import os

def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(cwd, 'result'), exist_ok=True)

    population = 1000
    V_array = np.linspace(1, 5, 10)
    C_array = np.linspace(1, 10, 10)

    with open('result/parameters.csv', 'a') as f:
        f.write('episode,V,C\n')
        for i, (V, C) in enumerate(itertools.product(V_array, C_array)):
            print(f'episode: {i}, V: {V}, C: {C}')
            simulation = Simulation(population=population)
            simulation.run_one_episode(episode=i, V=V, C=C)
            f.write(f'{i},{V},{C}\n')

if __name__ == '__main__':
    main()
