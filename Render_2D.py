import numpy as np
import random
import perlin2D
import sys
import matplotlib.pyplot as plt
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
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

def more_curve(value):
    if value > 0 and value < 0.75:
        return value+0.25
    elif value < 0 and value > -0.75:
        return value-0.25
    else:
        return value
    
def smooth(x,coef):
    if x < 0:
        return -x**coef
    return x**coef

def heightCurve(x, coef):
    if x < 0:
        return 0
    elif x > 1:
        return 1
    else:
        return x ** coef

def falloff(x, coef1, coef2):
    if x < 0:
        return 0
    elif x > 1:
        return 1
    else:
        return (x ** coef1) / ((x ** coef1) + (coef2 - coef2 * x) ** coef1)

def island_mode(value):
    if value < 100 :
        value = value - 30
        if value < 0:
            return 0
        else:
            return value
    elif value >= 100 and value < 175:
        return value + 30
    else:
        return value

def perlin():
    x = 512
    y = 512
    space = create_inputspace(x,y)
    # scale = random.randint(28,40)
    scale = 100
    debug_info = "Scale: " + str(scale)
    print(debug_info)
    mode = sys.argv[1]
    debug_info = "Mode: " + mode
    print(debug_info)
    for i in range(x):
        for j in range(y):
            perlin_value = perlin2D.eval(i/scale,j/scale, 2, 0.5)
            if mode != 'island':
                # perlin_value = map_to_0_255(smooth(more_curve(perlin_value),2))
                perlin_value = map_to_0_255(perlin_value)
            else:
                perlin_value = heightCurve(perlin_value+0.4,2)
                perlin_value = perlin_value * falloff(min(i, j, 512 - i, 512 - j) / 512, 3, 0.1)
                perlin_value = int(perlin_value * 180.0)
                # check value validation
                if perlin_value < 0:
                    perlin_value = 0
                elif perlin_value > 255:
                    perlin_value = 255
                # perlin_value = island_mode(perlin_value)
            space[i][j] = perlin_value
    space_map = map(space,x,y)
    
    return space_map

def texture_index_island(value):
    if value < 8 : # water22
        return 0
    elif value < 16: # rock11
        return 1
    elif value < 39 : # grass2
        return 2
    elif value < 50 : # Grass1
        return 3
    elif value < 60 : # Grass1
        return 4
    elif value < 90 : # Grass5
        return 5
    elif value < 125 : # rock2
        return 6
    else : # snow2
        return 7

def texture_index(value):
    if value < 70 : # water
        return 0
    elif value < 79: # Sand1
        return 1
    elif value < 90 : # Sand2
        return 2
    elif value < 110 : # Grass1
        return 3
    elif value < 123 : # Grass1
        return 4
    elif value < 150 : # Grass5
        return 5
    elif value < 170 : # rock2
        return 6
    else : # snow2
        return 7

def generate_height_map(_map):
    space_height = imgWrapper(_map.getMdata().tolist())
    space_height.save_img('render/height.png')

def generate_texture_map(_map):
    texture_range = []
    colordata = [[_map.getMdata()[i, j] for j in range(_map.gety())] for i in range(_map.getx())]
    # colordata = _map.getMdata()
    normal_texture_file = [imgWrapper('Texture/water2.jpg'), imgWrapper('Texture/Sand1.jpg'), imgWrapper('Texture/Sand2.jpg'), 
                    imgWrapper('Texture/Grass1.jpg'), imgWrapper('Texture/Grass1.jpg'),
                    imgWrapper('Texture/Grass5.jpg'), imgWrapper('Texture/rock2.png'), imgWrapper('Texture/snow2.jpg')]
    island_texture_file = [imgWrapper('Texture/water22.png'), imgWrapper('Texture/water11.png'), imgWrapper('Texture/Grass2.jpg'), 
                    imgWrapper('Texture/Grass1.jpg'), imgWrapper('Texture/Grass1.jpg'),
                    imgWrapper('Texture/Grass5.jpg'), imgWrapper('Texture/rock2.png'), imgWrapper('Texture/snow2.jpg')]
    
    # for i in range(5):
    #     temp_range = []
    #     for j in range(52):
    #         temp_range.append(i)
    #     texture_range = texture_range + temp_range
    # texture_range.append(4) # last one

    for i in range(_map.getx()):
        for j in range(_map.gety()):
            if sys.argv[1] == 'island':
                temp = island_texture_file[texture_index_island(int(_map.getvalue(i,j)))]
            else:
                temp = normal_texture_file[texture_index(int(_map.getvalue(i,j)))]
            colordata[i][j] = temp.getpixel(i,j)
    space_color = imgWrapper(colordata)
    space_color.save_img('render/color.png')

# def update():
#     player_height = player.y  # 保存玩家的当前高度

#     # 将玩家的 y 坐标设置到地形表面
#     hit_info = raycast(player.world_position, player.down, distance=2, ignore=[player, ])
#     if hit_info.hit:
#         player.y = hit_info.world_point.y + 1  # 适当调整高度

#     # 避免在穿越地形时突然下降
#     if player.y < player_height:
#         player.y = player_height

def input(key):
    if key == 'escape':
        application.quit()

space_map = perlin()
generate_height_map(space_map)
print("Height_map Pass")
generate_texture_map(space_map)
print("Color_map Pass")
# create window
app = Ursina(title='Procedural Terrain Generation', borderless=False)

# create first person view
player = FirstPersonController()

# create terrain entity
terrain = Terrain(heightmap='render/height.png', skip=1)
terrainEntity = Entity(model=terrain, scale=(100, 22, 100), texture='render/color.png', shader=basic_lighting_shader)

# create skybox and camera
Sky()
EditorCamera()

# run engine
app.run()

