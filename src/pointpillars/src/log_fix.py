import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import math
import sys
import struct
import glob
import matplotlib 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def checker():
    file1 = '/home/these/data/KITTI_for_PP4/training/velodyne_reduced/'
    file2 = '/home/these/data/KITTI_for_PP3/training/velodyne_reduced/'
    for i in range(7481):
        name1 = ''
        for j in range(6 - len(str(i))):

            name1 = name1 +'0'


        name1 = name1 + str(i)


        kasu1 = np.fromfile(file1+name1+ '.bin',dtype = np.float32)
        kasu2 = np.fromfile(file2+name1+ '.bin',dtype = np.float32)

        kasu1 =np.reshape(kasu1,(-1 ,4))
        kasu2 =np.reshape(kasu2,(-1,4))

        


        #kasu1  = np.loadtxt(file1+name1+ '.txt',dtype=str,delimiter=' ')
        #kasu2  = np.loadtxt(file2+name1+ '.txt',dtype=str,delimiter=' ')

        #kasu1 =np.reshape(kasu1,(15 ,-1))
        #kasu2 =np.reshape(kasu2,(15 ,-1))

        defe = kasu1.shape[0] - kasu2.shape[0]

        if kasu1[0][3] ==kasu2[0][3]:
            a  = 10
        else:
             print(kasu2[2][3])
            

        if np.abs(defe) > 0:
            print(name1)
    

def run(a, b, plus):

    file = './path/for_ped/16/xyz_10m_1'
    #file = './path/for_ped/16/xyzcospred_10m_6_kai'
    #file = './path/for_ped/xyzr10m_5'

    nums = []

    for i in range(int(a),int(b)+1):
        nums.append(i)



        #file = './path/for_ped/xyzr10m_' + str(i)
        #file = '/media/these/HDD/結果一覧/64/xyzcos10m_' +str(i)
        #file = '/media/these/HDD/結果一覧/64/xyz10m_' +str(i)

        kasu  = np.loadtxt(file+ '/log.txt',dtype=str,delimiter='\n')
        bev_list = list(np.where(kasu[:]=='Pedestrian AP@0.50, 0.50, 0.50:')) 
        for i in range(len(bev_list)):
            bev_list[i] = bev_list[i] + int(plus)
        bev_tp = tuple(bev_list)

        print(kasu[bev_tp])

def run1(a, plus, kind, kasu = ''):
    #file = './path/experiment/xyz' + str(a) 
    #file = './path/experiment/xyzpred' + str(a) 
    file = './path/sim_experiment/' + str(kind) + str(a) +str(kasu)
    #file = '/media/these/HDD/generated_models/experiment/' +str(kind)
        
    kasu  = np.loadtxt(file+ '/log.txt',dtype=str,delimiter='\n')
    bev_list = list(np.where(kasu[:]=='Pedestrian AP@0.50, 0.50, 0.50:')) 
    for i in range(len(bev_list)):
        bev_list[i] = bev_list[i] + int(plus)
    bev_tp = tuple(bev_list)

    print(kasu[bev_tp])

        
        
if __name__ == '__main__':
    
    #run(sys.argv[1] , sys.argv[2], sys.argv[3])
    run1(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    #checker()