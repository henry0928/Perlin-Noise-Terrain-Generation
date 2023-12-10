import numpy as np 
import math

def gradient(x, y) :
   _array = np.zeros(2)
   _array[0] = x * 127.1 + y * 311.7
   _array[1] = x * 269.5 + y * 183.3

   sin0 = math.sin(_array[0]) * 43758.5453123
   sin1 = math.sin(_array[1]) * 43758.5453123
   _array[0] = (sin0 - math.floor(sin0)) * 2.0 - 1.0
   _array[1] = (sin1 - math.floor(sin1)) * 2.0 - 1.0

   len = math.sqrt(_array[0] * _array[0] + _array[1] * _array[1])
   _array[0] /= len
   _array[1] /= len

   return _array

def eval(x, y, lacunarity, persistance) :
   #  p4(x_floor, y_ceiling)   p43     p3(x_ceiling, y_ceiling)
   #
   #                           pxy(x,y)  
   #       
   #  p1(x_floor, y_floor)     p12     p2(x_ceiling, y_floor)
   #       
   # first do p12 and then p43
   # final do pxy
   pxy = 0 
   for i in range(4):
      x = x * math.pow(lacunarity, i)
      y = y * math.pow(lacunarity, i)
      x_floor = math.floor(x)
      y_floor = math.floor(y)
      x_ceiling = x_floor + 1 
      y_ceiling = y_floor + 1 
      p1_dir = np.array([x-x_floor, y-y_floor]) 
      p2_dir = np.array([x-x_ceiling, y-y_floor])
      p3_dir = np.array([x-x_ceiling, y-y_ceiling])
      p4_dir = np.array([x-x_floor, y-y_ceiling]) 


      # get gradient
      p1_gra = gradient(x_floor, y_floor)
      p2_gra = gradient(x_ceiling, y_floor)
      p3_gra = gradient(x_ceiling, y_ceiling)
      p4_gra = gradient(x_floor, y_ceiling)

      # do dot calculation 
      p1_dot = np.dot(p1_dir, p1_gra)
      p2_dot = np.dot(p2_dir, p2_gra)
      p3_dot = np.dot(p3_dir, p3_gra)
      p4_dot = np.dot(p4_dir, p4_gra)

      #interpolation
      d = x - x_floor 
      smooth_factor = 6.0 * math.pow(d, 5.0) - 15.0 * math.pow(d, 4.0) + 10.0 * math.pow(d, 3.0)
      p12 = p1_dot * (1.0 - smooth_factor) + p2_dot * smooth_factor
      p43 = p4_dot * (1.0 - smooth_factor) + p3_dot * smooth_factor

      d = y - y_floor
      smooth_factor = 6.0 * math.pow(d, 5.0) - 15.0 * math.pow(d, 4.0) + 10.0 * math.pow(d, 3.0)
      pxy = pxy + (p12 * (1.0 - smooth_factor) + p43 * smooth_factor) * math.pow(persistance, i)

   return pxy
   
   

   