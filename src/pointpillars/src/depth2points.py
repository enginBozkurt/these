#!/usr/bin/env python


from cv_bridge import CvBridge
import numpy as np
import math
import json

import cv2

# import matplotlib 
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


import rospy
from sensor_msgs.msg import PointCloud2,PointField,Image
import std_msgs.msg

def np2pc(points):
    """ Creates a point cloud message.
    Args:
        points: Nx7 array of xyz positions (m) and rgba colors (0..1)
        parent_frame: frame in which the point cloud is defined
    Returns:
        sensor_msgs/PointCloud2 message
    """
    ros_dtype = PointField.FLOAT32
    dtype = np.float32
    itemsize = np.dtype(dtype).itemsize
    data = points.astype(dtype).tobytes()

    params = ['x','y','z','intensity']

    fields = [PointField(
        name=n, offset=i*itemsize, datatype=ros_dtype, count=1)
        for i, n in enumerate(params)]

    header = std_msgs.msg.Header(frame_id='velodyne', stamp=rospy.Time.now())

    return PointCloud2(
        header=header,
        height=1,
        width=points.shape[0],
        is_dense=False,
        is_bigendian=False,
        fields=fields,
        point_step=(itemsize*4),
        row_step=(itemsize*4*points.shape[0]),
        data=data
    )


def pub_kitti_points(path):

    rospy.init_node('depth_points_publisher', anonymous=True)

    points = np.fromfile(path, np.float32)

    points= np.reshape(points,(-1,3))

    zero_points = np.zeros([points.shape[0],1])

    points = np.concatenate([points, zero_points],axis = 1)

    #points[:,3] = 255.0*points[:,3]



    pub = rospy.Publisher('/velodyne_points', PointCloud2,queue_size=10)
    point_data = np2pc(points)

    while not rospy.is_shutdown():       
        r = rospy.Rate(0.5) # 10hz
        pub.publish(point_data)
        r.sleep()



def pub_points(path):

    rospy.init_node('depth_points_publisher', anonymous=True)

    count = 0
    print(count)

    pose_x = 0.
    pose_y = 0.
    flag = 0



    while(1):

        number = str(count)
        
        try:
            depth = cv2.imread(path+'depth/'+number+'_depth.png',-1)
            intensity = cv2.imread(path+'intensity/'+number+'_intensity.png',-1)
            print(depth.shape[0])
            f = open(path+'pose/'+number+'_pose.json','r')
            pose = json.load(f)
            flag = 1
            
                

        except:
            count = 0
            flag = 0
            break


        if (flag  == 1):


      


            distance = 0.0
            if count!=0:
                tmp_pose_x = float(pose['Pose']['translation']['x'])
                tmp_pose_y = float(pose['Pose']['translation']['y'])
                distance = math.sqrt((pose_x - tmp_pose_x)*(pose_x - tmp_pose_x)+(pose_y - tmp_pose_y)*(pose_y - tmp_pose_y))
                pose_x = tmp_pose_x
                pose_y = tmp_pose_y

            else:
                f2 = open(path+'pose/1_pose.json','r')
                pose2 = json.load(f2)
                pose_x = float(pose['Pose']['translation']['x'])
                pose_y = float(pose['Pose']['translation']['y'])
                tmp_pose_x = float(pose2['Pose']['translation']['x'])
                tmp_pose_y = float(pose2['Pose']['translation']['y'])
                distance = math.sqrt((pose_x - tmp_pose_x)*(pose_x - tmp_pose_x)+(pose_y - tmp_pose_y)*(pose_y - tmp_pose_y))
                
            print(distance)
            count= 1+ count
            distance = 0.0
            

            points = np.zeros((depth.shape[1]*depth.shape[0],4),dtype = np.float32)

            for i in range(0,32):
                for j in range(depth.shape[1]):
                    angle = (2.-(1./3.)*i)/180*np.pi
                    theta = np.pi-np.pi*j/1024.
                    points[i*depth.shape[1]+j,0]= 100.0*depth[i,j]/65535.0*math.cos(angle)*math.cos(theta) -distance/2047*j
                    points[i*depth.shape[1]+j,1]= 100.0*depth[i,j]/65535.0*math.cos(angle)*math.sin(theta)
                    points[i*depth.shape[1]+j,2]= 100.0*depth[i,j]/65535.0*math.sin(angle)

                    points[i*depth.shape[1]+j,3] = intensity[i,j]

            for i in range(32,64):
                for j in range(depth.shape[1]):
                    angle = (-8.53-(1./2.)*(i-32))/180*np.pi
                    theta = np.pi-np.pi*j/1024.
                    points[i*depth.shape[1]+j,0]= 100.0*depth[i,j]/65535.0*math.cos(angle)*math.cos(theta) - distance/2047*j
                    points[i*depth.shape[1]+j,1]= 100.0*depth[i,j]/65535.0*math.cos(angle)*math.sin(theta)
                    points[i*depth.shape[1]+j,2]= 100.9*depth[i,j]/65535.0*math.sin(angle)

                    points[i*depth.shape[1]+j,3] = intensity[i,j]




            
    #image
            image_publisher = rospy.Publisher('image_data', Image, queue_size=10)
            #read image
            img_vision = cv2.imread(path+'vision/'+number+'_camera.png',-1)
                # make bridge
            bridge = CvBridge()
            img_msg = bridge.cv2_to_imgmsg(img_vision, encoding="bgr8")
            image_publisher.publish(img_msg)

            


            

            pub = rospy.Publisher('/velodyne_points', PointCloud2)
            point_data = np2pc(points)
            
            r = rospy.Rate(0.5) # 10hz
            pub.publish(point_data)
            r.sleep()



    


    # fig = plt.figure(figsize=(100,100))
    # ax = Axes3D(fig)

    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    # ax.set_zlabel("Z")

    # ax.set_xlim(0, 30)
    # ax.set_ylim(-15, 15)
    # ax.set_zlim(-15, 15)


    # ax.plot(points[:,0],points[:,1],points[:,2],marker=".",linestyle='None')

    # plt.show()

if __name__=='__main__':

    #pub_points('/home/these/data/toyota/bike_bicycle/2/')

    pub_kitti_points('/home/these/27.bin')

    
