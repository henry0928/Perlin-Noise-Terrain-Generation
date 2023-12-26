import numpy as np 
import math
import random

perm = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,
 69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,
 203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,
 165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,
 92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,
 89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,
 226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,
 182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,
 43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,
 228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,
 49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,
 205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180,
 151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,
 10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,
 33,88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
 77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
 102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
 135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
 5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
 223,183,170,213,119,248,152, 2,44,154,163,70,221,153,101,155,167, 43,172,9,
 129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
 251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
 49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
 138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

def gradient(point) :
   grad_list = [(1,1,0), (-1,1,0), (1,-1,0), (-1,-1,0), 
                 (1,0,1), (-1,0,1), (1,0,-1), (-1,0,-1), 
                 (0,1,1), (0,-1,1), (0,1,-1), (0,-1,-1)]
   # index = random.randint(1,256) % 12 
   assert point[0] + perm[point[1]] < 512
   index = perm[point[0] + perm[point[1]]] % 12
   return grad_list[index]

def calculate_vector(start, end) :
   return [end[0]-start[0], end[1]-start[1], end[2]-start[2]]

def eval(x, y, z, lacunarity, persistance, scale) :
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
   layer = 4
   pxyz = 0 
   x = x/scale
   y = y/scale
   z = z/scale
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
      p1_gra = np.array(gradient(p1))
      p2_gra = np.array(gradient(p2))
      p3_gra = np.array(gradient(p3))
      p4_gra = np.array(gradient(p4))
      p5_gra = np.array(gradient(p5))
      p6_gra = np.array(gradient(p6))
      p7_gra = np.array(gradient(p7))
      p8_gra = np.array(gradient(p8))

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
      pxyz = pxyz + (p8743 * (1.0 - smooth_factor) + p5612 * smooth_factor) * math.pow(persistance, i)
      # scale = scale + 1

   return pxyz
   
   

   