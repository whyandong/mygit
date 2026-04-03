#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>  
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/ioctl.h>

#include "debug.h"
#include "ec_ram.h"
#include "s3s4_test.h"

#define TOOL_VERSION "v2.0"

void show_copyright(char *name)
{
	printf("%s %s is S3/S4 stress tool for FT platform .\n",name,TOOL_VERSION);
  printf("Copyright (c) Lenovo Corporation 2020-2025. All rights reserved.\n");	
  show_ec_version();
}
		
void show_help(char *name)
{
	printf("Usage :\n");
	printf("%s s3 [total count] (delay time) (keep time) \n", name);
	printf("%s s4 [total count] (delay time) (keep time)\n", name);	
	printf("(delay time) is option(from 1 to 255).The default value is 30s. \n");		
	printf("(keep time) is option(from 1 to 255).The default value is 30s. \n");		
	printf("(delay time) and (keep time) must be setted together.\n");		
	printf("%s s3 1000  or  %s s3 1000 40 40\n", name,name);
	printf("%s s4 1000  or  %s s4 1000 40 40\n", name,name);
}


void s3_stress_test(WORD cnt, BYTE delay, BYTE keep_time)
{
	WORD i;
	int ret;
	BYTE temp;
	char log_info[255]={0};
	
  printf("s3_stress_test start\n");
  #if DEBUG
  printf("s3_stress_test:cnt=%d,delay=%d\n",cnt,delay);
  #endif	
	log_save("s3_stress_test start\n");
	temp = keep_time - 5;
	for(i=0;i<cnt;i++)
	{
		sleep(temp);
		ret = set_delay_time(delay,S3_STRESS_TYPE);
		if(ret)
		{
			printf("s3_stress_test:set_delay_time error!\n");
			sprintf(log_info,"%d loop:set_delay_time error!\n",i);
			log_save(log_info);
			break;
		}		
		sleep(5);
		sprintf(log_info,"%d loop:suspend\n",i);
		log_save(log_info);
		printf("s3_stress_test %d loop: suspend...",i);
		system(S3_CMD);	
		printf("resume\n");
		sprintf(log_info,"%d loop:resume\n",i);
		log_save(log_info);	
	}	
	
	sprintf(log_info,"test %d loops\n",i);
	if(i!=cnt)
	{
		strcat(log_info,"s3_stress_test fail!\n");		
	}		
	else
		strcat(log_info,"s3_stress_test success!\n");
	log_save(log_info);	
	//log_save("s3_stress_test end\n");
	
	return ;	
}

void s4_stress_test(WORD cnt, BYTE delay, BYTE keep_time)
{
	WORD i;
	int ret;
	BYTE temp;
	char log_info[255]={0};
	
  printf("s4_stress_test start\n");
  #if DEBUG
  printf("s4_stress_test:cnt=%d,delay=%d\n",cnt,delay);
  #endif	
	log_save("s4_stress_test start\n");
	temp = keep_time - 5;
	for(i=0;i<cnt;i++)
	{
		sleep(temp);
		ret = set_delay_time(delay,S4_STRESS_TYPE);
		if(ret)
		{
			printf("s4_stress_test:set_delay_time error!\n");
			sprintf(log_info,"%d loop:set_delay_time error!\n",i);
			log_save(log_info);
			break;
		}		
		sleep(5);
		sprintf(log_info,"%d loop:suspend\n",i);
		log_save(log_info);
		printf("s4_stress_test %d loop: suspend...",i);
		system(S4_CMD);	
		printf("resume\n");
		sprintf(log_info,"%d loop:resume\n",i);
		log_save(log_info);	
	}	
	
	sprintf(log_info,"test %d loops\n",i);
	if(i!=cnt)
	{
		strcat(log_info,"s4_stress_test fail!\n");		
	}		
	else
		strcat(log_info,"s4_stress_test success!\n");
	log_save(log_info);	
	//log_save("s4_stress_test end\n");
	
	return ;	
}
	
int get_para(char *para, WORD *val, WORD min, WORD max)
{
	char * endp;
	WORD tmp;
	
	tmp = strtol(para, &endp, 10);
	if((tmp<min)||(tmp>max))
	{
		printf("para is invalid!\n");
		return -1;
	}		
	
	*val = tmp;
	
	return 0;
}
		
int main(int argc, char **argv)
{

	WORD delay = 1;
	WORD keep_time; 
	WORD cnt = 1;
	BYTE bdelay;
	int ret;

	show_copyright(argv[0]);
	
	if ((argc != 3)&&(argc != 5))
	{
		goto err;
	}
        
	if (strcmp(argv[1], "s3") == 0)
	{
		//printf("2\n"); 
		ret = get_para(argv[2],&cnt,COUNT_MIN,COUNT_MAX);
		if(ret)
			goto err;
		//printf("3 %d %d\n",cnt,argc); 	
		if(argc==5)	
		{
			ret = get_para(argv[3],&delay,TIME_MIN,TIME_MAX);
			if(ret)
				goto err;			
			
			ret = get_para(argv[4],&keep_time,OS_KEEP_TIME_MIN,TIME_MAX);
			if(ret)
				goto err;		
		}		
		else
		{	
			delay = S3_DELAY_TIME;
			keep_time = OS_KEEP_TIME;
		}	
    //printf("start s3 test:%d,%d\n",cnt,delay);
		s3_stress_test(cnt,delay,keep_time);
		//sleep(10);
		//system(S3_CMD);	
	}
	else if(strcmp(argv[1], "s4") == 0)
	{
		ret = get_para(argv[2],&cnt,COUNT_MIN,COUNT_MAX);
		if(ret)
			goto err;
		//printf("3 %d %d\n",cnt,argc); 	
		if(argc==5)	
		{
			ret = get_para(argv[3],&delay,TIME_MIN,TIME_MAX);
			if(ret)
				goto err;
						
			ret = get_para(argv[4],&keep_time,OS_KEEP_TIME_MIN,TIME_MAX);
			if(ret)
				goto err;					
		}		
		else
		{	
			delay = S4_DELAY_TIME;
			keep_time = OS_KEEP_TIME;
		}	
		s4_stress_test(cnt,delay,keep_time);	
			
	}
	else
	{
		goto err;
	}
	
	return 0;

err:
	show_help(argv[0]);
	return 0;	
}

