#include <gtest/gtest.h>
extern "C" {
#include "daemon.h"
}

TEST(DaemonTest, Increment) {
    /* 负数 -> 错误码 */
    EXPECT_EQ(daemon_increment(-5), -1);
    /* 零的特殊处理 */
    EXPECT_EQ(daemon_increment(0), 1);
    /* 正数的不同分支：
       3 % 3 == 0 -> +2
       4 % 3 == 1 -> +1
       5 % 3 == 2 -> 原值
    */
    EXPECT_EQ(daemon_increment(3), 5);
    EXPECT_EQ(daemon_increment(4), 5);
    EXPECT_EQ(daemon_increment(5), 5);
    /* 之前的 41 (41%3==2) 应返回 41 */
    EXPECT_EQ(daemon_increment(41), 41);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}