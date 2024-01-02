import numpy as np
import perlin2D
from img_Wrapper import imgWrapper
import matplotlib.pyplot as plt

def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)

x = 512 
y = 512
scale = 100
k = 1 
file_name = 'render/height_layer'
while k < 5 :
    terrain = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            terrain[i][j] = map_to_0_255(perlin2D.eval(i/scale, j/scale, 2, 0.5, k))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.imshow(terrain, cmap = 'gray', vmin = 0, vmax = 255)
    plt.show()
    terrain_height = imgWrapper(terrain.tolist())
    file = file_name + str(k) + '.png'
    terrain_height.save_img(file) 
    k = k + 1 