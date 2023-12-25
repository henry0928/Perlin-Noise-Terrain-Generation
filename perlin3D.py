import numpy as np 
import math
import random

def gradient() :
   grad_list = [(1,1,0), (-1,1,0), (1,-1,0), (-1,-1,0), 
                 (1,0,1), (-1,0,1), (1,0,-1), (-1,0,-1), 
                 (0,1,1), (0,-1,1), (0,1,-1), (0,-1,-1)]
   index = random.randint(1,256) % 12 
   return grad_list[index]

def calculate_vector(start, end) :
   return [end[0]-start[0], end[1]-start[1], end[2]-start[2]]

def eval(x, y, z, lacunarity, persistance) :
   #  p4(x_floor, y_floor, z_ceiling)           p3(x_ceiling, y_floor, z_ceiling)
   #
   #       
   #  p1(x_floor, y_ceiling, z_ceiling)         p2(x_ceiling, y_ceiling, z_ceiling)
   #
   #                                   x,y,z 
   #
   #  p8(x_floor, y_floor, z_floor)           p7(x_ceiling, y_floor, z_floor)
   #
   #       
   #  p5(x_floor, y_ceiling, z_floor)         p6(x_ceiling, y_ceiling, z_floor)
   layer = 5 
   pxyz = 0 
   for i in range(layer):
      x = x * math.pow(lacunarity, i)
      y = y * math.pow(lacunarity, i)
      z = z * math.pow(lacunarity, i) 
      x_floor = math.floor(x)
      y_floor = math.floor(y)
      z_floor = math.floor(z)
      x_ceiling = x_floor + 1 
      y_ceiling = y_floor + 1
      z_ceiling = z_floor + 1  

      target_point = [x, y, z]
      # set cube point
      p1 = [x_floor, y_ceiling, z_ceiling]
      p2 = [x_ceiling, y_ceiling, z_ceiling]
      p3 = [x_ceiling, y_floor, z_ceiling]
      p4 = [x_floor, y_floor, z_ceiling]
      p5 = [x_floor, y_ceiling, z_floor]
      p6 = [x_ceiling, y_ceiling, z_floor]
      p7 = [x_ceiling, y_floor, z_floor]
      p8 = [x_floor, y_floor, z_floor] 

      # get diration vector
      p1_dir = np.array(calculate_vector(p1, target_point)) 
      p2_dir = np.array(calculate_vector(p2, target_point)) 
      p3_dir = np.array(calculate_vector(p3, target_point)) 
      p4_dir = np.array(calculate_vector(p4, target_point))
      p5_dir = np.array(calculate_vector(p5, target_point)) 
      p6_dir = np.array(calculate_vector(p6, target_point)) 
      p7_dir = np.array(calculate_vector(p7, target_point)) 
      p8_dir = np.array(calculate_vector(p8, target_point)) 

      # get gradient
      p1_gra = np.array(gradient())
      p2_gra = np.array(gradient())
      p3_gra = np.array(gradient())
      p4_gra = np.array(gradient())
      p5_gra = np.array(gradient())
      p6_gra = np.array(gradient())
      p7_gra = np.array(gradient())
      p8_gra = np.array(gradient())

      # do dot calculation 
      p1_dot = np.dot(p1_dir, p1_gra)
      p2_dot = np.dot(p2_dir, p2_gra)
      p3_dot = np.dot(p3_dir, p3_gra)
      p4_dot = np.dot(p4_dir, p4_gra)
      p5_dot = np.dot(p5_dir, p5_gra)
      p6_dot = np.dot(p6_dir, p6_gra)
      p7_dot = np.dot(p7_dir, p7_gra)
      p8_dot = np.dot(p8_dir, p8_gra)

      # interpolation
      d = x - x_floor 
      smooth_factor = 6.0 * math.pow(d, 5.0) - 15.0 * math.pow(d, 4.0) + 10.0 * math.pow(d, 3.0)
      p12 = p1_dot * (1.0 - smooth_factor) + p2_dot * smooth_factor
      p43 = p4_dot * (1.0 - smooth_factor) + p3_dot * smooth_factor
      p56 = p5_dot * (1.0 - smooth_factor) + p6_dot * smooth_factor
      p87 = p8_dot * (1.0 - smooth_factor) + p7_dot * smooth_factor

      d = z - z_floor
      smooth_factor = 6.0 * math.pow(d, 5.0) - 15.0 * math.pow(d, 4.0) + 10.0 * math.pow(d, 3.0)
      p5612 = p56 * (1.0 - smooth_factor) + p12 * smooth_factor
      p8743 = p87 * (1.0 - smooth_factor) + p43 * smooth_factor

      d = y - y_floor
      smooth_factor = 6.0 * math.pow(d, 5.0) - 15.0 * math.pow(d, 4.0) + 10.0 * math.pow(d, 3.0)
      pxyz = pxyz + (p5612 * (1.0 - smooth_factor) + p8743 * smooth_factor) * math.pow(persistance, i)

   return pxyz
   
   

   