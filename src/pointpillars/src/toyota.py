#!/usr/bin/env python

import rospy

from sensor_msgs.msg import PointCloud2,PointField

from second.pytorch.train import set_model,pointp_based_detection
from std_msgs.msg import String

from ros_numpy.src.ros_numpy.point_cloud2 import array_to_pointcloud2

import sensor_msgs.point_cloud2 as pc2
import numpy as np
import math

from ros_numpy.src.ros_numpy.point_cloud2 import pointcloud2_to_array
from visualization_msgs.msg import Marker,MarkerArray
import geometry_msgs.msg

import random


class Net_Params:
    def __init__(self,net,input_cfg,model_cfg,train_cfg,class_names,voxel_generator,target_assigner):
        self.net = net
        self.input_cfg = input_cfg
        self.model_cfg = model_cfg
        self.train_cfg = train_cfg
        self.class_names = class_names
        self.voxel_generator = voxel_generator
        self.target_assigners = target_assigner


offset = 0.0


params = Net_Params(None,None,None,None,None,None,None)
def on_new_point_cloud(data):
    pc = pointcloud2_to_array(data)

    points = np.zeros((pc.shape[0],4),dtype = np.float32)
    for i in range(pc.shape[0]):
        points[i][0] = pc[i][0]
        points[i][1] = pc[i][1]
        points[i][2] = pc[i][2] - offset
        points[i][3] = pc[i][3]/255

        #points[i][3] = random.random()

    box_preds_lidar,labels,scores =pointp_based_detection('/home/these/second.pytorch/path/for_ped/model_dir',
             params.net,params.input_cfg,params.model_cfg,params.train_cfg,params.class_names,params.voxel_generator,params.target_assigner,
             points,
             None,
             True,
             None,
             None,
             True
             )


    # box_preds_lidar,labels,scores =pointp_based_detection('/home/these/catkin_ws/src/pointpillars/src/path/to/model_dir',
    #          params.net,params.input_cfg,params.model_cfg,params.train_cfg,params.class_names,params.voxel_generator,params.target_assigner,
    #          points,
    #          None,
    #          True,
    #          None,
    #          None,
    #          True
    #          )
    
    #visualization####
    topic = '/pointpillars/visualization/marker_box'
    marker_publisher = rospy.Publisher(topic, MarkerArray)
    markerArray = MarkerArray()

    del_marker = Marker()
    del_marker.action = del_marker.DELETEALL
    del_marker.header.frame_id = "visualization"
    del_marker.id = 1
    markerArray.markers.append(del_marker)
    
        
    for i in range(len(box_preds_lidar)):
        print(scores[i])
        if scores[i]>0.3:
            # result_string = str(labels[i])+','+str(scores[i])+','+str(box_preds_lidar[i][0])+ ','+ str(box_preds_lidar[i][1]) + ','+  str(math.sqrt(box_preds_lidar[i][1]*box_preds_lidar[i][1]+ box_preds_lidar[i][0]*box_preds_lidar[i][0])) +','+ str(box_preds_lidar[i][6])+'\n'
            # with open('20191121result_file.csv',mode ='a') as result_file:
            #     print(result_string)
            #     result_file.write(result_string) 
            
            marker = Marker()
            marker.header.frame_id = "visualization"
            marker.type = marker.CUBE
            marker.action = marker.ADD
            marker.scale.x = box_preds_lidar[i][3]
            marker.scale.y = box_preds_lidar[i][4]
            marker.scale.z = box_preds_lidar[i][5]
            marker.color.a = 0.3
            marker.color.r = 1.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.pose.orientation.x=0
            marker.pose.orientation.y=0
            marker.pose.orientation.z=math.sin(-box_preds_lidar[i][6]/2)
            marker.pose.orientation.w= math.cos(-box_preds_lidar[i][6]/2)
            marker.pose.position.x = box_preds_lidar[i][0]
            marker.pose.position.y = box_preds_lidar[i][1]
            marker.pose.position.z = box_preds_lidar[i][2]+box_preds_lidar[i][5]/2.0 + offset

            marker.id = 10+i

            marker.text = 'Car'

            marker.lifetime = rospy.Duration()
            markerArray.markers.append(marker)
    marker_publisher.publish(markerArray)

    topic = '/pointpillars/visualization/points'
    data.header.frame_id="visualization"
    points_publisher = rospy.Publisher(topic, PointCloud2)
    points_publisher.publish(data)


    boundary = Marker()
    boundary.header.frame_id = "visualization"
    boundary.type = boundary.LINE_STRIP
    boundary.action = boundary.ADD
    boundary.scale.x = 0.5
    boundary.color.a = 1.0
    boundary.color.r = 1.0
    boundary.color.g = 0.0
    boundary.color.b = 0.0
    boundary.pose.orientation.x=0
    boundary.pose.orientation.y=0
    boundary.pose.orientation.z=0
    boundary.pose.orientation.w=1

    corners =[0, -19.84, -2.5, 47.36, 19.84, 0.5]


    p1 = geometry_msgs.msg.Point(corners[0],corners[1],0.)
    boundary.points.append(p1)
    p2 = geometry_msgs.msg.Point(corners[0],corners[4],0.)
    boundary.points.append(p2)
    p3 = geometry_msgs.msg.Point(corners[3],corners[4],0.)
    boundary.points.append(p3)
    p4 = geometry_msgs.msg.Point(corners[3],corners[1],0.)
    boundary.points.append(p4)
    boundary.points.append(p1)
    boundary.id = 0
    boundary.lifetime = rospy.Duration()
    
    topic = '/pointpillars/visualization/boundary'
    boundary_publisher = rospy.Publisher(topic, Marker)
    boundary_publisher.publish(boundary)




def main():
    rospy.init_node('pointpillars')
    rospy.Subscriber("/velodyne_points", PointCloud2, on_new_point_cloud)    
    #rospy.Subscriber("/kitti/velo/pointcloud", PointCloud2, on_new_point_cloud)
    rospy.spin()



if __name__=='__main__':
    params.net,params.input_cfg,params.model_cfg,params.train_cfg,params.class_names,params.voxel_generator,params.target_assigner=set_model('/home/these/catkin_ws/src/pointpillars/src/second/configs/pointpillars/ped_cycle/xyres_16.proto','/home/these/catkin_ws/src/pointpillars/src/path/for_ped/model_dir',None,None)
    #params.net,params.input_cfg,params.model_cfg,params.train_cfg,params.class_names,params.voxel_generator,params.target_assigner=set_model('/home/these/catkin_ws/src/pointpillars/src/second/configs/pointpillars/car/xyres_16.proto','/home/these/catkin_ws/src/pointpillars/src/path/to/model_dir',None,None)
    print(params.input_cfg)
    main()
