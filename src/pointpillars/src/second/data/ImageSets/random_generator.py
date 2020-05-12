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

    



def generate(N,num):

    numbers = make_list(N)


    print(numbers)





    # for num in range(N):

    #     number_len = len(str(num))

    #     name = ''

    #     for i in range(6 -number_len):
    #         name = name + '0'

    #     name = name + str(num)

    #     numbers.append(name)
    #     print(name)

    numbers = random.sample(numbers,len(numbers))

    val_num = len(numbers) // 2
    
    #print(len(numbers))
    train_files = numbers[3739:]
    
    val_files = numbers[:3739]
    print(train_files)

    train_outfile = open('file_' + str(num) + '/train.txt','a')

    val_outfile = open('file_' + str(num) + '/val.txt','a')

    train2_outfile = open('file_' + str(num) + '/train2.txt','a')

    val2_outfile = open('file_' + str(num) + '/val2.txt','a')



    for i in range(len(train_files)):
        
        train_outfile.write(train_files[i] + '\n')

    train_outfile.close()

    for i in range(len(val_files)):
        
        val_outfile.write(val_files[i] + '\n')

    val_outfile.close()



    for i in range(len(train_files)):
        
        train2_outfile.write(train_files[i] + '\n')

    train2_outfile.close()

    for i in range(len(val_files)):
        
        val2_outfile.write(val_files[i] + '\n')

    val2_outfile.close()


    


if __name__ == '__main__':

        print(int(sys.argv[1]))
        generate(int(sys.argv[1]),int(sys.argv[2]))
