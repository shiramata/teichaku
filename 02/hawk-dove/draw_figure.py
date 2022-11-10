import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

def main():
    params = pd.read_csv('result/parameters.csv', index_col=0)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(0,1.1)
    hawks_ratio = []
    doves_ratio = []
    for i in range(100):
        df = pd.read_csv(f'result/episode_{i}.csv')
        ax.scatter(df.index, df['Hawk'], c='blue', s=.1, marker='*')
        ax.scatter(df.index, df['Dove'], c='orange', s=.1, marker='*')
        hawks_ratio.append(np.mean(df['Hawk'][20:]))
        doves_ratio.append(np.mean(df['Dove'][20:]))
    plt.savefig('tmp.png', dpi=600)

    print(f'avg_hawk: {np.mean(hawks_ratio)}')
    print(f'avg_dove: {np.mean(doves_ratio)}')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    x, y = np.meshgrid(np.unique(params['V']), np.unique(params['C']))
    z = griddata((params['V'], params['C']), hawks_ratio, (x, y))
    cont = ax.contourf(x, y, z)
    fig.colorbar(cont)
    ax.set_title('Ratio of Hawks')
    ax.set_xlabel('V')
    ax.set_ylabel('C')
    # ax.set_zlabel('hawks_ratio')
    fig.savefig('tmp2.png', dpi=600)


if __name__ == '__main__':
    main()









