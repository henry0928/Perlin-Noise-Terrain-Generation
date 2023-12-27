import numpy as np
import random
import time
import perlin3D
from multiprocessing import Process, Pipe, Queue
import matplotlib.pyplot as plt
import matplotlib.animation as pltanim

def map_to_0_255(value):
    new_value = (value + 1) * 255 / 2
    return int(new_value)

def update(idx):
    ax.clear()
    ax.imshow(terrain_list[idx], cmap='gray', vmin=0, vmax=255)
    time.sleep(0.1)
    ax.set_title(f"size =128*128*40, scale = 10, octave = (3, 2.0, 0.5), frame {idx}")

def run(x, y, z, scale, pipe_fd):
    # terrain = np.zeros((x,y))
    terrain = []
    row_terrain = []
    k = z/scale 
    for i in range(x):
        row_terrain = []
        for j in range(y):
            row_terrain.append(map_to_0_255(perlin3D.eval(i/scale, j/scale, k, 2, 0.5)))
            # terrain[i][j] = map_to_0_255(perlin3D.eval(i/scale, j/scale, k, 2, 0.5))
        terrain.append(row_terrain)
    pipe_fd.send(terrain)
    pipe_fd.close()            

if __name__ == '__main__':
    print("start normal run")
    x = 128
    y = 128
    z = 40
    terrain_list = []
    scale = random.randint(28,40)
    start_time = time.time()
    for k in range(z):
        terrain = np.zeros((x,y))
        for i in range(x):
            for j in range(y):
                terrain[i][j] = map_to_0_255(perlin3D.eval(i, j, k, 2, 0.5, scale))
        terrain_list.append(terrain)
    print("--- %s seconds for normal ---" % (time.time() - start_time))
    fig, ax = plt.subplots()
    anim = pltanim.FuncAnimation(fig, update, frames = 40, interval = 100)
    anim.save('render/noise3d.gif')
    plt.show()
    # print("start multi-process run")
    # x = 64
    # y = 32
    # z = 60
    # scale = random.randint(28,40)
    # terrain_list = []
    # fd_list = []
    # process_list = []
    # start_time = time.time()
    # for k in range(z):
    #     parent_conn, child_conn = Pipe()
    #     fd_list.append(parent_conn)
    #     p = Process(target=run, args=(x, y, k, scale, child_conn,))    
    #     process_list.append(p)
    #     p.start()
    # print("start waiting process....")
    # for process in process_list :
    #     process.join()
    #     print("finish process!")

    # for fd in fd_list:
    #     terrain_list.append(np.array(fd.recv()))

    # print("--- %s seconds for multi-process ---" % (time.time() - start_time))
    # # display animation
    # fig, ax = plt.subplots()
    # anim = pltanim.FuncAnimation(fig, update, frames = 60, interval = 100)
    # anim.save('render/noise3d.gif')
    # plt.show()