import numpy as np
import random
import perlin3D
import matplotlib.pyplot as plt
import matplotlib.animation as pltanim

def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)

def update(idx):
    ax.clear()
    ax.imshow(terrain_list[idx], cmap='gray', vmin=0, vmax=255)
    ax.set_title(f"seed = 1277, size = 40, scale = 10, octave = (3, 2.0, 0.5), frame {idx}")

x = 64
y = 64
z = 20
terrain = np.zeros((x,y))
scale = random.randint(28,40)
terrain_list = []
for k in range(z):
    terrain = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            terrain[i][j] = map_to_0_255(perlin3D.eval(i/scale, j/scale, k/scale, 2, 0.5))
    terrain_list.append(terrain)

# display animation
fig, ax = plt.subplots()
anim = pltanim.FuncAnimation(fig, update, frames = 20, interval = 100)
anim.save('render/noise3d.gif')
plt.show()