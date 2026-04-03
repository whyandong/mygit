
#ifndef _EC_RAM_DEV_H_
#define _EC_RAM_DEV_H_

typedef unsigned char BYTE;
typedef unsigned int  WORD;
typedef unsigned long   DWORD;

#define EC_RAM_DRV_VER  "1.2"

#define DEBUG 0

#ifndef EC_RAM_DEV_MAJOR
#define EC_RAM_DEV_MAJOR 231   
#endif

#ifndef EC_RAM_DEV_NR_DEVS
#define EC_RAM_DEV_NR_DEVS 2    
#endif

#ifndef EC_RAM_DEV_SIZE
#define EC_RAM_DEV_SIZE 4096
#endif

#define EC_RAM_CLASS_NAME "ecram_class"
#define EC_RAM_DEV_NAME "ecram"

#define LPC_IO_ADDR  0x20000000
#define LPC_IO_SIZE  0x8000000

#define LPC_CMD_PORT66             0x6C
#define LPC_DATA_PORT62            0x68
#define LPC_STATUS_PORT66          0x6C

#define LPC_OBF                   0x01
#define LPC_IBF                   0x02

#define LPC_DELAY_MAX             10000

#define EC_RAM_READ_CMD            0x80
#define EC_RAM_WRITE_CMD           0x81

#define EC_RAM_READ_EXCMD          0x92
#define EC_RAM_WRITE_EXCMD         0x93

/*ecram device struct*/
struct ecram_dev                                     
{                                                        
  char *data;                      
  unsigned long size;       
};

typedef struct ecram_info
{
	BYTE addrh;
	BYTE addrl;
	BYTE val;
	WORD buf_len;
	BYTE exval[256];
}ecram_info_s;

#define EC_IOCTL_BASE	'L'

#define	EC_RAM_READ     	_IOWR(EC_IOCTL_BASE, 0, ecram_info_s)
#define EC_RAM_WRITE 			_IOWR(EC_IOCTL_BASE, 1, ecram_info_s)
#define	EC_RAM_EX_READ  	_IOWR(EC_IOCTL_BASE, 2, ecram_info_s)
#define EC_RAM_EX_WRITE 	_IOWR(EC_IOCTL_BASE, 3, ecram_info_s)

#endif /* _EC_RAM_DEV_H_ */
