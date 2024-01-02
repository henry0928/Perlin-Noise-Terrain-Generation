import numpy as np
import random
import perlin3D
import sys
import matplotlib.pyplot as plt
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader

def get_texture(value) :
    if value <= 1 : 
        return "Texture_3D/rock1.jpg"
    elif value <= 3: 
        return "Texture_3D/dirt.png"
    elif value <= 4 : 
        return "Texture_3D/sand2.jpg"
    elif value <= 6 : 
        return "Texture_3D/grass1.jpg"
    elif value <= 8 :
        return "Texture_3D/grass2.jpg"
    else : 
        return "Texture_3D/grass3.jpg"

def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)

def input(key):
    if key == 'escape':
        application.quit()
    if key == 'tab':
            ec.enabled = not ec.enabled
            player.enabled = not player.enabled
    
if __name__ == '__main__':
    x = 16
    y = 16
    z = 10
    terrain = np.zeros((x,y,z))
    # terrain = terrain.astype('S')
    # scale = random.randint(28,40)
    scale = 40
    for k in range(z):
        for i in range(x):
            for j in range(y):
                perlin_value = perlin3D.eval(i, j, k, 2, 0.5, scale)
                terrain[i][j][k] = perlin_value 
                # e = Entity(model=Cube, position=Vec3(i,j,k), texture=file_name, shader=basic_lighting_shader)
    app = Ursina(title='Procedural Terrain Generation', borderless=False)
    # e = Entity(model='Cube', position=Vec3(0,0,0), texture="Texture_3D/dirt.png", shader=basic_lighting_shader) 
    for i in range (x):
        for j in range(y):
            for k in range(z):
                # if terrain[i][j][k] < -0.2 :
                #     p_x = i 
                #     p_y = k
                #     p_z = j 
                #     Entity(model='Cube', scale=(1,1,1), position=Vec3(i,k,j), texture=get_texture(k), shader=basic_lighting_shader, collider='box')
                if (terrain[i][j][k] < -0.1 and terrain[i][j][k] > -0.2) \
                    or (terrain[i][j][k] < 0.5 and terrain[i][j][k] > 0.1) \
                    or (terrain[i][j][k] < -0.3 and terrain[i][j][k] > -0.4):
                    p_x = i
                    p_y = k 
                    p_z = j
                    Entity(model='Cube', scale=(1,1,1), position=Vec3(i,k,j), texture=get_texture(k), shader=basic_lighting_shader, collider='box')
    floor = Entity(model='plane', scale=(100, 1, 100), texture='Texture/water1.jpg', collider='box')             
    # create skybox and camera
    Sky()
    ec = EditorCamera()
    ec.enabled = False
    player = FirstPersonController(x=p_x, y=p_y+1, z=p_z, collider='box', enabled=True)
    # run engine
    app.run()