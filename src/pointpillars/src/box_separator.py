#!/usr/bin/env python

import rospy



from std_msgs.msg import String
import numpy as np
import math
from visualization_msgs.msg import Marker,MarkerArray
import geometry_msgs.msg

import random


def on_new_point_cloud(data):

    
    topic = '/pointpillars/visualization/marker_box_25m'
    topic2 = '/pointpillars/visualization/marker_box_10m'
    marker_publisher = rospy.Publisher(topic, MarkerArray)
    markerArray = MarkerArray()

    del_marker = Marker()
    del_marker.action = del_marker.DELETEALL
    del_marker.header.frame_id = "visualization"
    del_marker.id = 1
    markerArray.markers.append(del_marker)


    marker2_publisher = rospy.Publisher(topic2, MarkerArray)
    markerArray2 = MarkerArray()

    del_marker2 = Marker()
    del_marker2.action = del_marker2.DELETEALL
    del_marker2.header.frame_id = "visualization"
    del_marker2.id = 1
    markerArray2.markers.append(del_marker2)

    print(len(data.markers))
    
        
    for i in range(len(data.markers)):

        print(data.markers[i].pose.position.x)
        #print(labels[i])
        if 2.5 >math.sqrt(data.markers[i].pose.position.x * data.markers[i].pose.position.x + data.markers[i].pose.position.y* data.markers[i].pose.position.y):

            
            # if labels[i] == 0:
            
            #result_string = str(labels[i])+','+str(scores[i])+','+str(box_preds_lidar[i][0])+ ','+ str(box_preds_lidar[i][1]) + ','+  str(math.sqrt(box_preds_lidar[i][1]*box_preds_lidar[i][1]+ box_preds_lidar[i][0]*box_preds_lidar[i][0])) +','+ str(box_preds_lidar[i][6])+'\n'
            # with open('./20191216xyz16_20m.csv','a') as result_file:
            #     result_file.write(result_string) 
            
                marker = Marker()
                marker.header.frame_id = "visualization"
                marker.type = marker.CUBE
                marker.action = marker.ADD
                marker.scale.x = data.markers[i].scale.x
                marker.scale.y = data.markers[i].scale.y
                marker.scale.z = data.markers[i].scale.z
                marker.color.a = 0.75
                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0
                marker.pose.orientation.x=0
                marker.pose.orientation.y=0
                marker.pose.orientation.z = data.markers[i].pose.orientation.z
                marker.pose.orientation.w= data.markers[i].pose.orientation.w
                marker.pose.position.x = data.markers[i].pose.position.x
                marker.pose.position.y = data.markers[i].pose.position.y
                marker.pose.position.z = data.markers[i].pose.position.z

                marker.id = 10+i

                marker.lifetime = rospy.Duration()
                markerArray.markers.append(marker)

        elif 10 > math.sqrt(data.markers[i].pose.position.x * data.markers[i].pose.position.x +data.markers[i].pose.position.y* data.markers[i].pose.position.y):
                marker2 = Marker()
                marker2.header.frame_id = "visualization"
                marker2.type = marker.CUBE
                marker2.action = marker.ADD
                marker2.scale.x = data.markers[i].scale.x
                marker2.scale.y = data.markers[i].scale.y
                marker2.scale.z = data.markers[i].scale.z
                marker2.color.a = 0.75
                marker2.color.r = 1.0
                marker2.color.g = 1.0
                marker2.color.b = 0.0
                marker2.pose.orientation.x=0
                marker2.pose.orientation.y=0
                marker2.pose.orientation.z = data.markers[i].pose.orientation.z
                marker2.pose.orientation.w= data.markers[i].pose.orientation.w
                marker2.pose.position.x = data.markers[i].pose.position.x
                marker2.pose.position.y = data.markers[i].pose.position.y
                marker2.pose.position.z = data.markers[i].pose.position.z

                marker2.id = 10+i

                marker2.lifetime = rospy.Duration()
                markerArray2.markers.append(marker2)




    marker_publisher.publish(markerArray)
    marker2_publisher.publish(markerArray2)


def on_new_point_cloud2(data):

    
    topic = '/pointpillars/visualization/marker_box2_25m'
    topic2 = '/pointpillars/visualization/marker_box2_10m'
    marker_publisher = rospy.Publisher(topic, MarkerArray)
    markerArray = MarkerArray()

    del_marker = Marker()
    del_marker.action = del_marker.DELETEALL
    del_marker.header.frame_id = "visualization"
    del_marker.id = 1
    markerArray.markers.append(del_marker)


    marker2_publisher = rospy.Publisher(topic2, MarkerArray)
    markerArray2 = MarkerArray()

    del_marker2 = Marker()
    del_marker2.action = del_marker2.DELETEALL
    del_marker2.header.frame_id = "visualization"
    del_marker2.id = 1
    markerArray2.markers.append(del_marker2)


    print(len(data.markers))
    
        
    for i in range(len(data.markers)):
        #print(labels[i])
        if 2.5 >math.sqrt(data.markers[i].pose.position.x * data.markers[i].pose.position.x + data.markers[i].pose.position.y* data.markers[i].pose.position.y):

                
          
                marker = Marker()
                marker.header.frame_id = "visualization"
                marker.type = marker.CUBE
                marker.action = marker.ADD
                marker.scale.x = data.markers[i].scale.x
                marker.scale.y = data.markers[i].scale.y
                marker.scale.z = data.markers[i].scale.z
                marker.color.a = 0.75
                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 1.0
                marker.pose.orientation.x=0
                marker.pose.orientation.y=0
                marker.pose.orientation.z = data.markers[i].pose.orientation.z
                marker.pose.orientation.w= data.markers[i].pose.orientation.w
                marker.pose.position.x = data.markers[i].pose.position.x
                marker.pose.position.y = data.markers[i].pose.position.y
                marker.pose.position.z = data.markers[i].pose.position.z

                marker.id = 10+i

                marker.lifetime = rospy.Duration()
                markerArray.markers.append(marker)

        elif 10 >math.sqrt(data.markers[i].pose.position.x * data.markers[i].pose.position.x + data.markers[i].pose.position.y* data.markers[i].pose.position.y):
                marker2 = Marker()
                marker2.header.frame_id = "visualization"
                marker2.type = marker.CUBE
                marker2.action = marker.ADD
                marker2.scale.x = data.markers[i].scale.x
                marker2.scale.y = data.markers[i].scale.y
                marker2.scale.z = data.markers[i].scale.z
                marker2.color.a = 0.75
                marker2.color.r = 0.0
                marker2.color.g = 1.0
                marker2.color.b = 1.0
                marker2.pose.orientation.x=0
                marker2.pose.orientation.y=0
                marker2.pose.orientation.z = data.markers[i].pose.orientation.z
                marker2.pose.orientation.w= data.markers[i].pose.orientation.w
                marker2.pose.position.x = data.markers[i].pose.position.x
                marker2.pose.position.y = data.markers[i].pose.position.y
                marker2.pose.position.z = data.markers[i].pose.position.z

                marker2.id = 10+i

                marker2.lifetime = rospy.Duration()
                markerArray2.markers.append(marker2)


    marker_publisher.publish(markerArray)
    marker2_publisher.publish(markerArray2)


def main():
    rospy.init_node('separator')
    #net,input_cfg,model_cfg,train_cfg,class_names,voxel_generator,target_assigner=set_model('/home/these/second.pytorch/second/configs/pointpillars/ped_cycle/xyres_16.proto','/home/these/second.pytorch/path/for_ped/model_dir',None,None)
    rospy.Subscriber("/pointpillars/visualization/marker_box", MarkerArray, on_new_point_cloud) 
    rospy.Subscriber("/pointpillars/visualization/marker_box2", MarkerArray, on_new_point_cloud2)
    rospy.spin()

if __name__=='__main__':

    main()