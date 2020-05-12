#include <fstream>
#include <iostream>
#include<sstream>
#include <boost/algorithm/string/classification.hpp> // is_any_of
#include <boost/algorithm/string/split.hpp>

#include <limits>
#include <dirent.h>

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




std::vector<std::string> get_file_list(){

    std::vector<std::string> files(0);

    std::ifstream ifs("/home/these/data/names.txt");

    std::string line;
    while (std::getline(ifs, line)) {


        std::string line_ = line.substr(0,line.size()-1);
         
        std::cout << line_ << std::endl;
        files.push_back(line_);

    }

    return files;


}

int loadPointCloudFromCSV(const std::string &file_path, pcl::PointCloud<pcl::PointXYZ>::Ptr cloud) {
	std::ifstream ifs(file_path, std::ios::in);
	if(!ifs)
		return 1;	// File open failed
printf("load_fail\n");

	std::string buf;
	while(ifs && std::getline(ifs, buf)) {
		std::vector<std::string> v;
		boost::algorithm::split(v, buf, boost::is_any_of(","));
        //printf("%d\n",v.size());
		if(v.size() < 4)
			continue;
		pcl::PointXYZ p;
		p.x = std::atof(v[0].c_str());
		p.y = std::atof(v[1].c_str());
		p.z = std::atof(v[2].c_str());

		cloud-> points.push_back(p);
        
	}
	return 0;
}

//法線検出//////////////////////////////
pcl::PointCloud<pcl::PointNormal>::Ptr Calculate_Normals(const pcl::PointCloud<pcl::PointXYZ>::Ptr& cloud)
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

std::vector< std::vector<double> > Calculate_Cos(const pcl::PointCloud<pcl::PointNormal>::Ptr& cloud){

    //pcl::PointCloud<pcl::PointXYZI>::Ptr cloud_cos(new pcl::PointCloud<pcl::PointXYZI>);
    std::vector< std::vector<double> > output_points(0, std::vector<double>(7,0.));
    for(int point=0; point <cloud->points.size();point++){

double normal_x = cloud->points[point].normal_x; 
        double normal_y = cloud->points[point].normal_y; 
        double normal_z = cloud->points[point].normal_z;
 double x = cloud->points[point].x; 
        double y = cloud->points[point].y; 
        double z = cloud->points[point].z;
double cos = 0.;

if(!std::isnan(normal_x)){

	double distance  = std::sqrt(x*x + y*y + z*z);

        double n_x = x/distance;
        double n_y = y/distance;
        double n_z = z/distance;

        cos = std::abs(normal_x*n_x + normal_y*n_y + normal_z*n_z);

}
else{

normal_x = 0.;
normal_y = 0.;
normal_z = 0.;

cos = 0.;
}
        
//std::cout << "x:" << x << "y:" <<y <<  "z:" << z << "normal_x:" << normal_x<< "normal_y:" << normal_y << "normal_z:"  << normal_z <<std::endl;
std::vector<double> one_point{x,y,z,cos};
        output_points.push_back(one_point);
        



    }

    return output_points;
}



void csv2normal(std::string in_file_name, std::string out_file_name){

pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
//pcl::PointCloud<pcl::PointXYZI>::Ptr cloud_cos(new pcl::PointCloud<pcl::PointXYZI>);
pcl::PointCloud<pcl::PointNormal>::Ptr cloud_with_normals(new pcl::PointCloud<pcl::PointNormal>);

std::vector< std::vector<double> > cos_points;
std::cout << "load_points" << std::endl;
loadPointCloudFromCSV(in_file_name, cloud);
cloud_with_normals = Calculate_Normals(cloud);
cos_points = Calculate_Cos(cloud_with_normals);

std::ofstream ofs(out_file_name);

for (int i = 0; i <cos_points.size(); i++){
        for (int j = 0; j < 4; j++)
    {
        ofs<< cos_points[i][j];

        if(j != 3){

            ofs<< ",";
        }
    }
    ofs << std::endl;
}
ofs.close();
}


int main(){

    int start_num,end_num;
    std::string in_file_name,out_file_name;


    std::cin >> start_num;
    std::cin >> end_num;
std::cout << "input_done" << std::endl;

    int count = start_num;


    std::vector<std::string> filelist;
    filelist = get_file_list();

    std::cout << "input_done2" << std::endl;

    
    while(1){


        std::string filename = ""; 
        std::ostringstream oss;
        oss << count;
        std::string str_count = oss.str(); 

        
        // for(int i = 0;i<6- str_count.length();i++){

        //     filename = filename +  "0";
        // }

        std::cout << filelist.size() << std::endl;

        int index = -1; 





        for(int i = 0;i<filelist.size();i++){

            std::string str = filelist[i];

            std::string data_num;

            int find_value = -1;
            data_num  =  "_" + std::to_string(count) + ".";
            
            find_value = str.find(data_num);

            if(find_value != -1){
                index = i;
                break;
            }
        }

        std::cout << index << std::endl;


        filename = filelist[index];


        

        // in_file_name = "/home/these/data/velodyne_csv/" + filename + str_count + ".csv";
        // out_file_name = "/home/these/data/KITTI_for_PP/training/velodyne_cos_csv/" + filename + str_count + ".csv";
        in_file_name = "/home/these/data/velodyne_csv/Lidar_" + filename  + "csv";
        std::cout << in_file_name << std::endl;

        out_file_name = "/home/these/data/velodyne_cos_csv/Lidar_" + filename + "csv";
csv2normal(in_file_name,out_file_name);
std::cout << filename + str_count << std::endl;
if(count ==end_num){
break;
}

        count++;


    }
}

