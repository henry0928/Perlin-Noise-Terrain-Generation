import numpy as np
import random
import perlin2D
import matplotlib.pyplot as plt

def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)

x = 256 
y = 256
terrain = np.zeros((x,y))
scale = random.randint(20,40)
for i in range(x):
    for j in range(y):
        terrain[i][j] = map_to_0_255(perlin2D.eval(i/scale, j/scale, 2, 0.5))

plt.xlabel('x')
plt.ylabel('y')
plt.imshow(terrain, cmap = 'gray', vmin = 0, vmax = 255)
plt.show()