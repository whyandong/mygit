
#ifndef _S3S4_TEST_H_
#define _S3S4_TEST_H_

#define COUNT_MIN           1
#define COUNT_MAX           10000

#define TIME_MIN      10
#define TIME_MAX      255
#define OS_KEEP_TIME_MIN    20

#define OS_KEEP_TIME        30

#define S3_DELAY_TIME       30     // delay 30s

#define S4_DELAY_TIME       30     // delay 30s

#define S3_CMD    "echo mem > /sys/power/state"
#define S4_CMD    "echo disk > /sys/power/state"

#endif /* _S3S4_TEST_H_ */