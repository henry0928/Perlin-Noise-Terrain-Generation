import numpy as np
import random
import perlin2D
import matplotlib.pyplot as plt
from ursina import *
from ursina.shaders import basic_lighting_shader
from img_Wrapper import imgWrapper

class map:
    def __init__(self, space_map, _x, _y):
        self.map = space_map
        self.x = _x
        self.y = _y

    def getx(self):
        return self.x
    
    def gety(self):
        return self.y

    def getvalue(self,x,y):
        return self.map[x][y]
    
    def getMdata(self):
        return self.map

def create_inputspace(x,y):
    _array = np.zeros((x,y))
    return _array

def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)

def perlin():
    x = 256
    y = 256
    space = create_inputspace(x,y)
    scale = random.randint(20,40)
    print(scale)
    for i in range(x):
        for j in range(y):
            space[i][j] = map_to_0_255(perlin2D.eval(i/scale,j/scale))
    space_map = map(space,x,y)
    
    return space_map
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.imshow(space, cmap = 'gray', vmin = 0, vmax = 255)
    # plt.show()

def texture_index(value):
    if value < 90 :
        return 0
    elif value < 103 :
        return 1
    elif value < 127 :
        return 2
    elif value < 140 :
        return 3
    elif value < 180 :
        return 4
    else :
        return 5

def generate_height_map(_map):
    space_height = imgWrapper(_map.getMdata().tolist())
    space_height.save_img('render/height.png')

def generate_texture_map(_map):
    texture_range = []
    colordata = [[_map.getMdata()[i, j] for j in range(_map.gety())] for i in range(_map.getx())]
    # colordata = _map.getMdata()
    texture_file = [imgWrapper('Texture/water.png'), imgWrapper('Texture/sand.png'), imgWrapper('Texture/rock1.png'), imgWrapper('Texture/rock3.png')
                    , imgWrapper('Texture/grass.png'), imgWrapper('Texture/snow.png')]
    
    # for i in range(5):
    #     temp_range = []
    #     for j in range(52):
    #         temp_range.append(i)
    #     texture_range = texture_range + temp_range
    # texture_range.append(4) # last one

    for i in range(_map.getx()):
        for j in range(_map.gety()):
            temp = texture_file[texture_index(int(_map.getvalue(i,j)))]
            colordata[i][j] = temp.getpixel(i,j)
        print("still running")
    space_color = imgWrapper(colordata)
    space_color.save_img('render/color.png')
    
    

space_map = perlin()
generate_height_map(space_map)
print("height_map pass")
generate_texture_map(space_map)
print("color_map pass")
# create window
app = Ursina(title='Procedural Terrain Generation', borderless=False)

# create terrain entity
terrain = Terrain(heightmap='render/height.png', skip=8)
terrainEntity = Entity(model=terrain, scale=(100, 15,100), texture='render/color.png', shader=basic_lighting_shader)

# create skybox and camera
Sky()
EditorCamera()

# run engine
app.run()

