#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <linux/errno.h>
#include <linux/input.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <string.h>
#include <time.h>

#include "debug.h"

char log_file[255]={0};

#define LOGFILE "/test.log"

void get_logfile(void)
{
	if(!log_file[0])   //create 
	{
		getcwd(log_file, 256);
		#if DEBUG_LOG
		printf("get_logfile:%s\n",log_file);
		#endif
		strcat(log_file,LOGFILE);
		#if DEBUG_LOG
		printf("get_logfile:%s\n",log_file);
		#endif
	}
	return ;		
}
	
int get_local_time(char * psDateTime) 
{
    time_t nSeconds;
    struct tm * pTM;
    
    time(&nSeconds);
    pTM = localtime(&nSeconds);

    /* 系统日期和时间,格式: yyyymmddHHMMSS */
    sprintf(psDateTime, "%04d-%02d-%02d %02d:%02d:%02d ",
            pTM->tm_year + 1900, pTM->tm_mon + 1, pTM->tm_mday,
            pTM->tm_hour, pTM->tm_min, pTM->tm_sec);
            
    return 0;
}

int log_save(char *log)
{
	int filefd;
	int len;
	int ret;
	char str_tmp[255]={0};

	if(log == NULL)
	{
		printf("log_save:log para error!\n");
		return -1;
	}	
	
	len = strlen(log);
	if((strlen(log) == 0) || (strlen(log)>255))	
	{
		printf("log_save:log para error!\n");
		return -1;
	}
		
	get_local_time(str_tmp);
	#if DEBUG_LOG	
	printf("current time is %s \n",str_tmp);
	#endif
	
	get_logfile();
	
	#if DEBUG_LOG	
	printf("current logfile is %s \n",log_file);
	#endif
		
	filefd = open(log_file, O_RDWR | O_CREAT | O_APPEND);	
	if(filefd < 0)
	{
		printf("log_save:open log file error!\n");
		return -1;
	}		
	//printf("log_save:open file ok!(0x%x)\n",filefd);
	
	//printf("log_save:start write time(0x%x)\n",(int)strlen(str_tmp));	
	ret = write(filefd,str_tmp,strlen(str_tmp));
	if(ret != strlen(str_tmp))
	{
		printf("log_save:save current time error!");
	}
	//printf("log_save:write time ok!(0x%x)\n",ret);
	//printf("log_save:start write log(0x%x)\n",len);	
	ret = write(filefd,log,len);
	if(ret != len)
	{
		printf("log_save:save log error!");
	}
	//printf("log_save:write log ok!(0x%x)\n",ret);
	close(filefd);
	return 0;
}
