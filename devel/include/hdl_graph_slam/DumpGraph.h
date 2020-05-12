// Generated by gencpp from file hdl_graph_slam/DumpGraph.msg
// DO NOT EDIT!


#ifndef HDL_GRAPH_SLAM_MESSAGE_DUMPGRAPH_H
#define HDL_GRAPH_SLAM_MESSAGE_DUMPGRAPH_H

#include <ros/service_traits.h>


#include <hdl_graph_slam/DumpGraphRequest.h>
#include <hdl_graph_slam/DumpGraphResponse.h>


namespace hdl_graph_slam
{

struct DumpGraph
{

typedef DumpGraphRequest Request;
typedef DumpGraphResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct DumpGraph
} // namespace hdl_graph_slam


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::hdl_graph_slam::DumpGraph > {
  static const char* value()
  {
    return "a8b810758ea760dd74984f070e767d53";
  }

  static const char* value(const ::hdl_graph_slam::DumpGraph&) { return value(); }
};

template<>
struct DataType< ::hdl_graph_slam::DumpGraph > {
  static const char* value()
  {
    return "hdl_graph_slam/DumpGraph";
  }

  static const char* value(const ::hdl_graph_slam::DumpGraph&) { return value(); }
};


// service_traits::MD5Sum< ::hdl_graph_slam::DumpGraphRequest> should match 
// service_traits::MD5Sum< ::hdl_graph_slam::DumpGraph > 
template<>
struct MD5Sum< ::hdl_graph_slam::DumpGraphRequest>
{
  static const char* value()
  {
    return MD5Sum< ::hdl_graph_slam::DumpGraph >::value();
  }
  static const char* value(const ::hdl_graph_slam::DumpGraphRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::hdl_graph_slam::DumpGraphRequest> should match 
// service_traits::DataType< ::hdl_graph_slam::DumpGraph > 
template<>
struct DataType< ::hdl_graph_slam::DumpGraphRequest>
{
  static const char* value()
  {
    return DataType< ::hdl_graph_slam::DumpGraph >::value();
  }
  static const char* value(const ::hdl_graph_slam::DumpGraphRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::hdl_graph_slam::DumpGraphResponse> should match 
// service_traits::MD5Sum< ::hdl_graph_slam::DumpGraph > 
template<>
struct MD5Sum< ::hdl_graph_slam::DumpGraphResponse>
{
  static const char* value()
  {
    return MD5Sum< ::hdl_graph_slam::DumpGraph >::value();
  }
  static const char* value(const ::hdl_graph_slam::DumpGraphResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::hdl_graph_slam::DumpGraphResponse> should match 
// service_traits::DataType< ::hdl_graph_slam::DumpGraph > 
template<>
struct DataType< ::hdl_graph_slam::DumpGraphResponse>
{
  static const char* value()
  {
    return DataType< ::hdl_graph_slam::DumpGraph >::value();
  }
  static const char* value(const ::hdl_graph_slam::DumpGraphResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // HDL_GRAPH_SLAM_MESSAGE_DUMPGRAPH_H
