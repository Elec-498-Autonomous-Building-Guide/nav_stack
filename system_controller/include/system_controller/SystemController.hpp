#include "owen_common/timestamp.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "create_msgs/msg/bumper.hpp"
#include "geometry_msgs/msg/twist.hpp"

struct RobotStatus
{
    create_msgs::msg::Bumper bumper;
};


class SystemController : public rclcpp_lifecycle::LifecycleNode
{
public:
    SystemController(const std::string &name);
private:
    void bumperCallback(const create_msgs::msg::Bumper::ConstSharedPtr msg);
    void cmdVelCallback(const geometry_msgs::msg::Twist::ConstSharedPtr msg);

private:
    rclcpp_lifecycle::LifecyclePublisher<geometry_msgs::msg::Twist>::SharedPtr _cmdVelPub;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr _cmdVelSub;
    rclcpp::Subscription<create_msgs::msg::Bumper>::SharedPtr _bumperSub;
    owen_common::Timestamp<RobotStatus> _status;
};
