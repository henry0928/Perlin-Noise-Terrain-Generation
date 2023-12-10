import numpy as np
import random
import perlin2D
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

def perlin():
    x = 256
    y = 256
    space = create_inputspace(x,y)
    scale = random.randint(20,40)
    debug_info = "Scale: " + str(scale)
    print(debug_info)
    for i in range(x):
        for j in range(y):
            space[i][j] = map_to_0_255(perlin2D.eval(i/scale,j/scale, 2, 0.5))
    space_map = map(space,x,y)
    
    return space_map

def texture_index(value):
    if value < 90 :
        return 0
    elif value < 96 :
        return 1
    elif value < 104 :
        return 2
    elif value < 130 :
        return 3
    elif value < 155 :
        return 4
    elif value < 180 :
        return 5
    else :
        return 6

def generate_height_map(_map):
    space_height = imgWrapper(_map.getMdata().tolist())
    space_height.save_img('render/height.png')

def generate_texture_map(_map):
    texture_range = []
    colordata = [[_map.getMdata()[i, j] for j in range(_map.gety())] for i in range(_map.getx())]
    # colordata = _map.getMdata()
    texture_file = [imgWrapper('Texture/water1.jpg'), imgWrapper('Texture/Sand1.jpg'), imgWrapper('Texture/Sand.png'), imgWrapper('Texture/Grass1.jpg') 
                    , imgWrapper('Texture/Grass2.jpg'), imgWrapper('Texture/grass.png'), imgWrapper('Texture/snow2.jpg')]
    
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
    space_color = imgWrapper(colordata)
    space_color.save_img('render/color.png')

def update():
    player_height = player.y  # 保存玩家的当前高度

    # 将玩家的 y 坐标设置到地形表面
    hit_info = raycast(player.world_position, player.down, distance=2, ignore=[player, ])
    if hit_info.hit:
        player.y = hit_info.world_point.y + 1  # 适当调整高度

    # 避免在穿越地形时突然下降
    if player.y < player_height:
        player.y = player_height

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
terrain = Terrain(heightmap='render/height.png', skip=8)
terrainEntity = Entity(model=terrain, scale=(100, 15,100), texture='render/color.png', shader=basic_lighting_shader)

# set player origin position
player.origin = terrainEntity.origin

# create skybox and camera
Sky()
EditorCamera()

# run engine
app.run()

