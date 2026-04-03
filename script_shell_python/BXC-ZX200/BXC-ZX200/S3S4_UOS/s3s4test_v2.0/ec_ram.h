
#ifndef _EC_RAM_H_
#define _EC_RAM_H_

typedef unsigned char BYTE;
typedef unsigned int  WORD;
typedef unsigned long DWORD;

#define EC_RAM_DEV_PATH "/dev/ecram"

typedef struct ecram_info
{
	BYTE addrh;
	BYTE addrl;
	BYTE val;
	WORD buf_len;
	BYTE exval[256];
}ecram_info_s;

#define EC_IOCTL_BASE	'L'

#define	EC_RAM_READ     _IOWR(EC_IOCTL_BASE, 0, ecram_info_s)
#define EC_RAM_WRITE 		_IOWR(EC_IOCTL_BASE, 1, ecram_info_s)

#define OWEN_MAIN_VERSION_ADDR     0x1B
#define OWEN_SUB_VERSION_ADDR      0x1C
#define PC_MAIN_VERSION_ADDR       0x00
#define PC_SUB_VERSION_ADDR        0x01

#define EC_RAM_STRESS_ADDR    0x09
#define S3_STRESS_TEST        0x01    //bit0
#define S4_STRESS_TEST        0x02    //bit1

#define EC_RAM_DELAY_ADDR     0x0C

#define S3_STRESS_TYPE    0x0
#define S4_STRESS_TYPE    0x1

//dtime: delay time(secode)
//type: delay type.
//      ==0  S3 delay
//      ==1  S4 delay
extern int set_delay_time(BYTE dtime, BYTE type);
extern int show_ec_version(void);

#endif /* _EC_RAM_H_ */
