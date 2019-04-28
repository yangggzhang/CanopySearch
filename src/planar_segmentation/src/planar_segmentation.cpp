#include <iostream>
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/common/common.h>
#include <pcl/features/normal_3d.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/filters/passthrough.h>
#include <vector>
#include <cmath> 
#include <cstdlib>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <librealsense2/rs.hpp>
#include <librealsense2/rsutil.h>

using namespace std;
using namespace cv;

  float P[12] = {0.0688 ,  -0.3594  ,  0.9307 ,  -0.1849, -0.9976 ,  -0.0260 ,   0.0637  ,  0.0131, 0.0013 ,  -0.9328 ,  -0.3603 ,   0.4750};


pcl::PointCloud<pcl::PointXYZ>::Ptr points_to_pcl(const rs2::points& points)
{
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);

    auto sp = points.get_profile().as<rs2::video_stream_profile>();
    cloud->width = sp.width();
    cloud->height = sp.height();
    cloud->is_dense = false;
    cloud->points.resize(points.size());
    auto ptr = points.get_vertices();
    for (auto& p : cloud->points)
    {
        p.x = ptr->x;
        p.y = ptr->y;
        p.z = ptr->z;
        ptr++;
    }

    return cloud;
}

inline double distance(pcl::PointXYZ &p)
{
   return std::sqrt( p.x* p.x + p.y* p.y + p.z* p.z);
}

pcl::PointCloud<pcl::PointXYZ>::Ptr extract_plane(pcl::PointCloud<pcl::PointXYZ>::Ptr &cloud, pcl::SACSegmentation<pcl::PointXYZ> &seg, pcl::ModelCoefficients::Ptr &coefficients, std::vector<double> &centroid)
{
    pcl::PointCloud<pcl::PointXYZ>::Ptr plane(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_p (new pcl::PointCloud<pcl::PointXYZ>), cloud_f (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
    seg.setInputCloud (cloud);
    seg.segment (*inliers, *coefficients);

    if (inliers->indices.size () == 0)
    {
      PCL_ERROR ("Could not estimate a planar model for the given dataset.");
      return plane;
    }
  
    plane->points.resize (inliers->indices.size ());
    for (size_t i = 0; i < inliers->indices.size (); ++i) plane->points[i] = cloud->points[inliers->indices[i]];
    float x = 0.0;
    float y = 0.0;
    float z = 0.0;
    for (int i = 0; i < plane->points.size(); i++){
        x += plane->points[i].x;
        y += plane->points[i].y;
        z += plane->points[i].z;
    }
    centroid.resize(3);
    centroid[0] = x / (double)plane->points.size();
    centroid[1] = y / (double)plane->points.size();
    centroid[2] = z / (double)plane->points.size();
    
    pcl::ExtractIndices<pcl::PointXYZ> extract;
    // Extract the inliers
    extract.setInputCloud (cloud);
    extract.setIndices (inliers);
    extract.setNegative (false);
    extract.filter (*cloud_p);

    // Create the filtering object
    extract.setNegative (true);
    extract.filter (*cloud_f);
    cloud.swap (cloud_f);

    return plane;
}

void view_pcl(pcl::PointCloud<pcl::PointXYZ>::Ptr &cloud)
{
  pcl::visualization::CloudViewer viewer ("Simple Cloud Viewer");
  viewer.showCloud (cloud);
  while (!viewer.wasStopped ()) {}
}

void calculate_centroid(pcl::PointCloud<pcl::PointXYZ>::Ptr &cloud, std::vector<double> &centroid)
{
  centroid.resize(3);
  float x = 0.0;
  float y = 0.0;
  float z = 0.0;
  for (int i = 0; i < cloud->points.size(); i++){
        x += cloud->points[i].x;
        y += cloud->points[i].y;
        z += cloud->points[i].z;
  }
  x /= (double)cloud->points.size();
  y /= (double)cloud->points.size();
  z /= (double)cloud->points.size();

  centroid[0] = x;
  centroid[1] = y;
  centroid[2] = z;
}

int main (int argc, char** argv)
{
  rs2::pipeline pipe;
  pipe.start();


  // Camera warmup - dropping several first frames to let auto-exposure stabilize
  rs2::frameset frames;
  for(int i = 0; i < 30; i++)
  {
      //Wait for all configured streams to produce a frame
      frames = pipe.wait_for_frames();
  }

  // Get each frame
  rs2::frame color_frame = frames.get_color_frame();

  // Creating OpenCV Matrix from a color image
  Mat image0(Size(640, 480), CV_8UC3, (void*)color_frame.get_data(), Mat::AUTO_STEP);
  Mat image1 = image0.clone();


  auto test_color_frame = frames.get_color_frame();
  auto color_profile = test_color_frame.get_profile().as<rs2::video_stream_profile>();
  rs2_intrinsics color_intrin = color_profile.get_intrinsics();

  auto depth = frames.get_depth_frame();
  auto depth_profile = depth.get_profile().as<rs2::video_stream_profile>();
  rs2_intrinsics depth_intrin = depth_profile.get_intrinsics();

  rs2_extrinsics depth_to_color = depth_profile.get_extrinsics_to(color_profile);

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>), cloud_p (new pcl::PointCloud<pcl::PointXYZ>), cloud_f (new pcl::PointCloud<pcl::PointXYZ>);

  rs2::points points;
  rs2::pointcloud pc;
  pc.map_to(test_color_frame);
  points = pc.calculate(depth);

  cloud = points_to_pcl(points);

  // load data
  pcl::PCDReader Reader;
  Reader.read("/home/zy/Documents/RobotAutonomy/project/data/0.pcd", *cloud);
  view_pcl(cloud);

  pcl::PointXYZ minPt, maxPt;
  pcl::getMinMax3D (*cloud, minPt, maxPt);

  std::cout<<minPt.x<<" "<<maxPt.x<<std::endl;
  std::cout<<minPt.y<<" "<<maxPt.y<<std::endl;
  std::cout<<minPt.z<<" "<<maxPt.z<<std::endl; 

  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
  // Create the segmentation object
  pcl::SACSegmentation<pcl::PointXYZ> seg;
  // Optional
  seg.setOptimizeCoefficients (true);
  // Mandatory
  seg.setModelType (pcl::SACMODEL_PLANE);
  seg.setMethodType (pcl::SAC_RANSAC); 
  seg.setDistanceThreshold (0.01); //0.007

  std::vector<double> c0;
  pcl::PointCloud<pcl::PointXYZ>::Ptr plane_cloud = extract_plane( cloud, seg, coefficients, c0);
  view_pcl(plane_cloud);


  vector<double> centroid(3, 0.0);
  
  calculate_centroid(plane_cloud, centroid);

  std::cout<<centroid[0]<<" "<<centroid[1]<<" "<<centroid[2]<<std::endl;

  // std::cout<<x_min<<" "<<x_max<<std::endl;
  // std::cout<<y_min<<" "<<y_max<<std::endl;
  // std::cout<<z_min<<" "<<z_max<<std::endl; 


  // pcl::PointCloud<pcl::PointXYZ>::Ptr bb_cloud(new pcl::PointCloud<pcl::PointXYZ>);

  // BoundingBox Point cloud
  // // && cloud->points[i].z >= z_min && cloud->points[i].z <= z_max
  // for (int i = 0; i < cloud->points.size(); i++)
  // {
  //   // cout<<i<<endl;
  // // { (cloud->points[i].x >= x_min && cloud->points[i].x <= x_max && cloud->points[i].y >= y_min && cloud->points[i].y <= y_max  )
  //   if (cloud->points[i].z <= z_max && cloud->points[i].z >= z_min && cloud->points[i].x >= x_min && cloud->points[i].x <= x_max && cloud->points[i].y >= y_min && cloud->points[i].y <= y_max) 
  //   {
  //     bb_cloud->push_back(cloud->points[i]);
  //   }
  // }

  // view_pcl(table_cloud);
  // drawBoundingBox(image0, table_cloud, &color_intrin);

  // drawBoundingBox(image0, table_cloud, &color_intrin, cv::Scalar(0,0,0));

  // std::vector<std::vector<double>> v;
  // std::vector<double> d;
  // v.resize(3);
  // d.resize(3);



  // std::cout<<x<<" "<<y<<" "<<z<<std::endl;

  // float depth_xyz[3] = {x,y,z};
  // // std::cout<<x<<" "<<y<<" "<<z<<std::endl;
  // float rgb_xyz[3];

  // rs2_transform_point_to_point(rgb_xyz,  &depth_to_color, depth_xyz);

  // // std::cout<<rgb_xyz[0]<<" "<<rgb_xyz[1]<<" "<<rgb_xyz[2]<<std::endl;

  // float goal_x = P[0]*rgb_xyz[0] + P[1]*rgb_xyz[1] + P[2]*rgb_xyz[2] + P[3];
  // float goal_y = P[4]*rgb_xyz[0] + P[5]*rgb_xyz[1] + P[6]*rgb_xyz[2] + P[7];
  // float goal_z = P[8]*rgb_xyz[0] + P[9]*rgb_xyz[1] + P[10]*rgb_xyz[2] + P[11];

  // std::cout<<"x : "<<goal_x<<std::endl;
  // std::cout<<"y : "<<goal_y<<std::endl;
  // std::cout<<"z : "<<goal_z<<std::endl;


  return (0);
}