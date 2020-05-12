import numpy as np
import sys
import random
import pandas as pd
from pandas import Series, DataFrame



def make_list(N):
    file_list = []
    for num in range(N):

        number_len = len(str(num))

        
        name = ''

        for i in range(6 -number_len):
            name = name + '0'

        name = name + str(num)

        file_list.append(name)

        #infilename ='/home/these/data/KITTI_for_PP/training/label_2/'+ name + '.txt'

        #df = pd.read_csv(infilename,sep = ' ', names = ('class','oculusion','dificulty','alpha','image1','image2','image3','image4','h','w','l','x','y','z','angle'))

        # if len(df.index) == 1:
        #     if df.iloc[0,0] != 'DontCare':
        #         file_list.append(name)
        #         #print(infilename)

        
        # else:
        #     file_list.append(name)
        #     #print(infilename)

        print(name)

        
    return file_list

    



def generate():

    


    train_data = np.loadtxt('train3682.txt',dtype="str",delimiter='\n')
    val_data = np.loadtxt('test3799.txt',dtype="str",delimiter='\n')

    train_names = []
    val_names = []

    for i in range(len(train_data)):
        number_len = len(train_data[i])
        name = ''
        for j in range(6 -number_len):
             name = name + '0'

        name = name +train_data[i]
        train_names.append(name)


    for i in range(len(val_data)):
        number_len = len(val_data[i])
        name = ''
        for j in range(6 -number_len):
             name = name + '0'

        name = name + val_data[i]
        val_names.append(name)
    

    train_outfile = open('AD.txt','a')

    val_outfile = open('CB.txt','a')

    for i in range(len(train_names)):
        
         train_outfile.write(train_names[i] + '\n')

    

    for i in range(len(val_names)):
        
         val_outfile.write(val_names[i] + '\n')


def make_ABCD():
    ABs = np.loadtxt('AB.txt',dtype="str",delimiter='\n')
    ADs = np.loadtxt('AD.txt',dtype="str",delimiter='\n')
    CDs = np.loadtxt('CD.txt',dtype="str",delimiter='\n')
    CBs = np.loadtxt('CB.txt',dtype="str",delimiter='\n')


    As = []
    Bs = []
    Cs = []
    Ds = []

    for ab in ABs:
        for ad in ADs:
            if ab == ad:
                As.append(ab)
                break
    

    for cd in CDs:
        for cb in CBs:
            if cd == cb:
                Cs.append(cd)
                break

    
    for ab in ABs:
        for cb in CBs:
            if ab == cb:
                Bs.append(ab)
                break
    

    for cd in CDs:
        for ad in ADs:
            if cd == ad:
                Ds.append(cd)
                break

    
    print(len(As))
    print(len(Bs))
    print(len(Cs))
    print(len(Ds))


    train_outfile = open('AC.txt','a')

    val_outfile = open('BD.txt','a')

    for i in range(len(As)):
        
        train_outfile.write(As[i] + '\n')

    for i in range(len(Cs)):
        
        train_outfile.write(Cs[i] + '\n')

    

    for i in range(len(Bs)):
        
        val_outfile.write(Bs[i] + '\n')

    for i in range(len(Ds)):
        
        val_outfile.write(Ds[i] + '\n')
    

    
        



  
    


if __name__ == '__main__':

    
    make_ABCD()
