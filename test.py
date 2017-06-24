import numpy as np

with open('ratios.pickle', 'rb') as f:
    t = np.load(f)
    print(t.shape)
