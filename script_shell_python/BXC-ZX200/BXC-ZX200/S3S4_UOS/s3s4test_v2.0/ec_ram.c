#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>  
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/ioctl.h>

#include "ec_ram.h"
#include "debug.h"

int ec_read(int fd,BYTE addr,BYTE *val)
{
	ecram_info_s ec_info;
	int ret;

	if((!fd)||(!val))
	{
		printf("ec_read: null point error!\n");
		return -1;
	}		
	ec_info.addrl = addr;
	ret = ioctl(fd,EC_RAM_READ,&ec_info);
	if(ret<0)
	{	
		printf("ec_read: ioctl error!(0x%x)(0x%x)\n",ret,ec_info.val);
		return ret;
	}	
	#if DEBUG_ECRAM
	printf("ec_read:read [0x%x]=0x%x\n",addr,ec_info.val);
	#endif
	*val = ec_info.val;
	return 0;
}

int ec_write(int fd,BYTE addr,BYTE val)
{
	ecram_info_s ec_info;
	int ret;
	
	if(!fd)
	{
		return -1;
	}	
	ec_info.addrl = addr;
	ec_info.val  = val;
	ret = ioctl(fd,EC_RAM_WRITE,&ec_info);
	if(ret < 0)
		return ret;
		
	return 0;
}

//flag ==1 set bit;
//     ==0 clear bit;
int ec_update_bit(int fd,BYTE addr,BYTE val,BYTE flag)
{
	BYTE tmp;
	int ret;
	
	ret = ec_read(fd, addr, &tmp);
	if(ret<0)
		return ret;
	
	#if DEBUG_ECRAM
		printf("ec_update_bit:read data=0x%x\n",tmp);
	#endif	
	if(flag)
		tmp |= val;
	else
		tmp &= (~val);

	#if DEBUG_ECRAM
		printf("ec_update_bit:set data=0x%x\n",tmp);
	#endif			

	ret = ec_write(fd, addr, tmp);
	if(ret<0)
		return ret;		
			
	return 0;
}

//dtime: delay time(secode)
//type: delay type.
//      ==0  S3 delay
//      ==1  S4 delay
int set_delay_time(BYTE dtime, BYTE type)
{
	int fd;
	int ret;
	BYTE val;
	
	if((type != 0)&&(type != 1))
	{
		printf("set_delay_time:para error!\n");
		return -1;		
	}
			
	fd = open(EC_RAM_DEV_PATH, O_RDWR);
	if (fd < 0)
	{
		printf("ec ram dev open fail!\n");
		return -1;
	}	
	
	ret = ec_write(fd,EC_RAM_DELAY_ADDR,dtime);
	if(ret<0)
	{	
		printf("ec ram write data fail!\n");
		close(fd);			
		return ret;		
	}
	switch(type)
	{
		case S3_STRESS_TYPE:
			val = S3_STRESS_TEST;
			break;
			
		case S4_STRESS_TYPE:
			val = S4_STRESS_TEST;
			break;
			
		default:
			val = 0;
			break;	
	}
		
	ret = ec_write(fd,EC_RAM_STRESS_ADDR,val);
	
	close(fd);	
	
	return ret;
}

int show_ec_version(void)
{
	int fd;
	int ret;
	BYTE mver,sver;
	
	fd = open(EC_RAM_DEV_PATH, O_RDWR);
	if (fd < 0)
	{
		printf("ec ram dev open fail!\n");
		return -1;
	}	
	
	ret = ec_read(fd,OWEN_MAIN_VERSION_ADDR,&mver);
	if(ret)
		goto ver_end;
		
	if(!mver)
	{
		//maybe pc product
		ret = ec_read(fd,PC_MAIN_VERSION_ADDR,&mver);
		if(ret)
			goto ver_end;
		
		ret = ec_read(fd,PC_SUB_VERSION_ADDR,&sver);	
		if(ret)
			goto ver_end;			
	}		
	else
	{
		ret = ec_read(fd,OWEN_SUB_VERSION_ADDR,&sver);	
		if(ret)
			goto ver_end;	
	}		
	
	if(mver)
		printf("ec current version:%02x.%02x\n",mver,sver);
	
	close(fd);	
	return 0;
	
ver_end:
	close(fd);		
	return -1;
}
