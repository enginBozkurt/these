#include <ros/ros.h>
#include <iostream>

#include <sensor_msgs/PointCloud2.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl_ros/transforms.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/features/normal_3d.h>
#include <pcl/features/normal_3d_omp.h>
#include <pcl/filters/voxel_grid.h>
#include <Eigen/Geometry> 

const double PI=3.14159265358979323846;

const Eigen::Vector4f subsampling_leaf_size (0.2f, 0.2f, 0.2f, 0.0);

Eigen::Vector4f centroid (0.0,0.0,0.0,0.0);

ros::Publisher pub_cloud;
ros::Publisher pub_distance;
ros::Subscriber sub_cloud;


//間引いてやるよ////////////////////////////////////////
pcl::PointCloud<pcl::PointXYZ>::Ptr Subsample_cloud (const pcl::PointCloud<pcl::PointXYZ>::Ptr& cloud)
{

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_subsampled (new pcl::PointCloud<pcl::PointXYZ> ());
  pcl::VoxelGrid<pcl::PointXYZ> subsampling_filter;
  subsampling_filter.setInputCloud (cloud);
  subsampling_filter.setLeafSize (subsampling_leaf_size);
  subsampling_filter.filter (*cloud_subsampled);

  return cloud_subsampled;
}




//法線検出//////////////////////////////
pcl::PointCloud<pcl::PointNormal>::Ptr Calculate_Normals (const pcl::PointCloud<pcl::PointXYZ>::Ptr& cloud)
{
  float normal_estimation_search_radius = 0.2;

  pcl::PointCloud<pcl::Normal>::Ptr cloud_normals (new pcl::PointCloud<pcl::Normal> ());
  pcl::NormalEstimationOMP<pcl::PointXYZ, pcl::Normal> normal_estimation_filter;
  normal_estimation_filter.setInputCloud (cloud);
  pcl::search::KdTree<pcl::PointXYZ>::Ptr search_tree (new pcl::search::KdTree<pcl::PointXYZ>);
  normal_estimation_filter.setSearchMethod (search_tree);
  normal_estimation_filter.setRadiusSearch (normal_estimation_search_radius);
  normal_estimation_filter.compute (*cloud_normals);

  pcl::PointCloud<pcl::PointNormal>::Ptr cloud_with_normals (new pcl::PointCloud<pcl::PointNormal> ());
  pcl::concatenateFields (*cloud, *cloud_normals, *cloud_with_normals);
  return cloud_with_normals;
}
/////////////////////////////////////////////////////////




//平面検出//////////////////////////////////////////////////////////////////
std::vector<float> plane_detector(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){

    if (cloud->points.size() == 0){
		std::cout << "no cloud data" << std::endl;
        std::vector<float> plane_params(4,0.);
		return plane_params;
	}
	//　平面検出
	pcl::SACSegmentation<pcl::PointXYZ> seg;
    float threshold = 0.1;
	seg.setOptimizeCoefficients(true);
	pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);
	pcl::PointIndices::Ptr inliers(new pcl::PointIndices);

	seg.setInputCloud(cloud);
	seg.setModelType(pcl::SACMODEL_PLANE); //モデル
	seg.setMethodType(pcl::SAC_RANSAC);	//検出手法
	seg.setMaxIterations(200);
	seg.setDistanceThreshold(threshold); //閾値
	seg.segment(*inliers, *coefficients);
    

    return coefficients->values;
}
//////////////////////////////////////////////////////////////////



//距離計算//
int Calcurate_distance(pcl::PointCloud<pcl::PointXYZI>::Ptr cloud, double* average_distance, double* average_intensity,pcl::PointCloud<pcl::PointXYZ>::Ptr partial_cloud){
    
    
    
    // double n_distance = 0.;
    // double n_intensity = 0.;

    // int count = 0;

    double y_dev  = 10.0;
    int tmp_point_num = -1;


    for(int point = 0; point < cloud->points.size();point++){

        double distance = 0.;

        

        double x = cloud->points[point].x;
        double y = cloud->points[point].y;
        double z = cloud->points[point].z;


        double angle = std::atan2(z,x);

        double target_theta = PI/180.0;

        double upper_target_theta = 4.0*PI/180.0;

        double lower_target_theta = -2.0*PI/180.0;
        

        if (upper_target_theta > angle && lower_target_theta < angle){
            if(y >= -0.15 && y <= 0.15 && x > 0.){

                // distance = std::sqrt(x*x + y*y + z*z);
                // double intensity = cloud->points[point].intensity;
                // n_distance = distance + n_distance;
                // n_intensity = intensity + n_intensity;
                // count++;

                pcl::PointXYZ cloud_sub_point;
                cloud_sub_point.x = x;
                cloud_sub_point.y = y;
                cloud_sub_point.z = z;
                partial_cloud->points.push_back(cloud_sub_point);

                if (target_theta + PI/180.0 > angle && target_theta - PI/180.0 < angle){

                    if(y_dev > std::abs(y)){
                        y_dev = std::abs(y);
                        tmp_point_num  = point;
                    }
                }
            }
        }  

    }

    // n_distance = n_distance/(double)count;
    // n_intensity = n_intensity/(double)count;
    //std::cout << "intensity:" << n_intensity << std::endl;
    // *average_distance = n_distance;
    // *average_intensity = n_intensity;
    //std::cout << "intensity:" << *average_intensity<< std::endl;

    double last_x = cloud->points[tmp_point_num].x;
    double last_y = cloud->points[tmp_point_num].y;
    double last_z = cloud->points[tmp_point_num].z;
    
    double last_distance = std::sqrt(last_x*last_x + last_y*last_y + last_z*last_z);
    *average_distance = last_distance;
    *average_intensity = cloud->points[tmp_point_num].intensity;
    std::cout << "y_dev:" << cloud->points[tmp_point_num].y << std::endl;

    return 0;
}





//コールバック関数
void Cloud_cb (const sensor_msgs::PointCloud2ConstPtr& msg)
{
    double pre_time = ros::Time::now().toSec();
    //msg -> pcl///////////////////////
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZI>::Ptr cloud_i(new pcl::PointCloud<pcl::PointXYZI>);
    pcl::PointCloud<pcl::PointNormal>::Ptr cloud_n(new pcl::PointCloud<pcl::PointNormal>);

    pcl::PointCloud<pcl::PointXYZ>::Ptr partial_cloud(new pcl::PointCloud<pcl::PointXYZ>);

    pcl::fromROSMsg(*msg, *cloud);
    pcl::fromROSMsg(*msg, *cloud_i);
    //cloud_n = Calculate_Normals(cloud);
    

    //std_msgs::Float64 msg_distance;
    std_msgs::Float64MultiArray msg_distance;
    msg_distance.data.resize(3);
    sensor_msgs::PointCloud2 msg_cloud;

    double average_distance;
    double average_intensity;
    Calcurate_distance(cloud_i,&average_distance, &average_intensity,partial_cloud);

    

    std::vector<float> plane_params(4,0.);
    
    plane_params = plane_detector(partial_cloud);

    cloud_n = Calculate_Normals(partial_cloud);

    double n_normal_x= 0.;
    double n_normal_y= 0.;
    double n_normal_z= 0.;
    int normal_count = 0;

    for(int point = 0; point < cloud_n->points.size();point++){

        double distance = 0.;
        double n_x = cloud_n->points[point].normal_x;
        double n_y = cloud_n->points[point].normal_y;
        double n_z = cloud_n->points[point].normal_z;
        
        n_x = std::abs(n_x);
        //符号合わせ
        n_y = n_y*n_x/std::abs(n_x);
        n_z = n_z*n_x/std::abs(n_x);

        n_normal_x = n_normal_x + n_x;
        n_normal_y = n_normal_y + n_y;
        n_normal_z = n_normal_z + n_z;
        normal_count++;

    }

    n_normal_x = n_normal_x/(double)normal_count;
    n_normal_y = n_normal_y/(double)normal_count;
    n_normal_z = n_normal_z/(double)normal_count;


    double plane_n_x = plane_params[0];
    double plane_n_y = plane_params[1];
    double plane_n_z = plane_params[2];
    double n_d = plane_params[3];

    double plane = std::sqrt(plane_n_x*plane_n_x + plane_n_y*plane_n_y + plane_n_z*plane_n_z);

  if (plane_n_x < 0){
      plane_n_x = -plane_n_x/plane;
      plane_n_y = -plane_n_y/plane;
      plane_n_z = -plane_n_z/plane;

  }
  else{
      plane_n_x = plane_n_x/plane;
      plane_n_y = plane_n_y/plane;
      plane_n_z = plane_n_z/plane;
  }

  



    // std::cout << "a:" << n_normal_x <<  std::endl;
    // std::cout << "b:" << n_normal_y <<  std::endl;
    // std::cout << "c:" << n_normal_z <<  std::endl;

    double theta = std::acos(n_normal_x);

    
    double plane_theta = std::acos(plane_n_x*cos(PI/180) +plane_n_z*sin(PI/180));

    std::cout << "theta(-> 0):" << plane_theta*180.0/PI << "  normal_y(->0):" << plane_n_y*180.0/PI  << std::endl;

    msg_distance.data[0] = average_distance;
    msg_distance.data[1] = average_intensity;
    msg_distance.data[2] =  plane_theta;
    
    
    pcl::toROSMsg(*partial_cloud, msg_cloud);
    msg_cloud.header.frame_id = "velodyne";
  // Publish the data
    pub_cloud.publish (msg_cloud);
    pub_distance.publish (msg_distance);
    double now_time = ros::Time::now().toSec();
    //std::cout << "TIME:" << now_time -pre_time << std::endl;

}


int main(int argc, char **argv)
{
    ros::init(argc,argv,"subsribe_and_publish");
    ros::NodeHandle n;

    sub_cloud = n.subscribe<sensor_msgs::PointCloud2>("/velodyne_points",1000,Cloud_cb);

    pub_cloud = n.advertise<sensor_msgs::PointCloud2>("/these_cloud/pointnormal", 1);
    pub_distance = n.advertise<std_msgs::Float64MultiArray>("/these_cloud/distance", 1);
    ros::spin();

    return 0;

 }
