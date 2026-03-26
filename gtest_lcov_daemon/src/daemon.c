#include "daemon.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

/* 可测试的小函数：加入 if/else 和 switch 分支 */
int daemon_increment(int v) {
    if (v < 0) {
        /* 负数视为错误，返回 -1 */
        return -1;
    } else if (v == 0) {
        /* 零特殊处理 */
        return 1;
    } else {
        /* 根据 v 对 3 的余数采取不同策略 */
        switch (v % 3) {
            case 0:
                /* 对能被3整除的值，+2 */
                return v + 2;
            case 1:
                /* 余1的值，+1 */
                return v + 1;
            default:
                /* 余2的值，返回原值 */
                return v;
        }
    }
}

#ifndef UNIT_TEST
/* 简单守护进程主循环（演示） */
int main(int argc, char **argv) {
    const char *log = "/tmp/simple_daemon.log";
    FILE *f = fopen(log, "a");
    if (!f) return 1;
    fprintf(f, "daemon started (pid=%ld)\n", (long)getpid());
    fflush(f);
    while (1) {
        time_t t = time(NULL);
        fprintf(f, "[%ld] heartbeat: %d\n", (long)t, daemon_increment(0));
        fflush(f);
        sleep(5);
    }
    fclose(f);
    return 0;
}
#endif