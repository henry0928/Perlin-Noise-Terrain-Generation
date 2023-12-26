import numpy as np
import random
import perlin3D
import sys
import matplotlib.pyplot as plt
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader

def get_texture(value) :
    if value <= 5 : 
        return "Texture_3D/rock1.jpg"
    elif value <= 10: 
        return "Texture_3D/dirt.png"
    elif value <= 15 : 
        return "Texture_3D/sand2.jpg"
    elif value <= 20 : 
        return "Texture_3D/grass1.jpg"
    elif value <= 25 :
        return "Texture_3D/grass2.jpg"
    else : 
        return "Texture_3D/grass3.jpg"
def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)
    
if __name__ == '__main__':
    x = 16
    y = 16
    z = 30
    terrain = np.zeros((x,y,z))
    # terrain = terrain.astype('S')
    scale = random.randint(28,40)
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
                if terrain[i][j][k] > -0.2 or terrain[i][j][k] < -0.7 :
                    Entity(model='Cube', scale=(1,1,1), position=Vec3(i,k,j), texture=get_texture(k), shader=basic_lighting_shader) 
    # create skybox and camera
    Sky()
    EditorCamera()

    # run engine
    app.run()