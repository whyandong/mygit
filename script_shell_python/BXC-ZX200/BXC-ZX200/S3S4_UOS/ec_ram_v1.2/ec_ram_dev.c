#include <linux/module.h>
#include <linux/types.h>
#include <linux/fs.h>
#include <linux/errno.h>
#include <linux/err.h>
#include <linux/mm.h>
#include <linux/sched.h>
#include <linux/init.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/slab.h>
#include <linux/ioport.h>
#include <asm/io.h>
#include <asm/uaccess.h>

#include "ec_ram_dev.h"

static int ecram_major = EC_RAM_DEV_MAJOR;

module_param(ecram_major, int, S_IRUGO);

struct ecram_dev *ecram_devp; 

struct cdev cdev; 
struct device *dev;
struct class *ecram_class;
struct resource *ecram_resource;

static volatile BYTE *lpc_addr;
BYTE dev_num;

static BYTE ec_ib_free(void)
{
	BYTE Status;
	WORD i = 0;
	
	do{
		i++;
		Status=readb(lpc_addr+LPC_STATUS_PORT66);
	}while((Status&LPC_IBF)&&(i<LPC_DELAY_MAX));
	
	return ((i==LPC_DELAY_MAX)?1:0);
}

static BYTE ec_ob_full(void)
{
	BYTE Status;
	WORD i = 0;
	
	do{
		i++;
		Status=readb(lpc_addr+LPC_STATUS_PORT66);
	}while((!(Status&LPC_OBF))&&(i<LPC_DELAY_MAX));
	
	return ((i==LPC_DELAY_MAX)?1:0);
}

static BYTE ec_write_cmd(BYTE cmd)
{
	if(ec_ib_free())
	{		
		printk(KERN_ERR "[ecramdev]ec_write_cmd:I/P buffer error!\n");
		return 1;
	}		
	writeb(cmd,lpc_addr+LPC_CMD_PORT66);
	return 0;
}

static BYTE ec_write_data(BYTE data)
{
	if(ec_ib_free())
	{
		printk(KERN_ERR "[ecramdev]ec_write_data:I/P buffer error!\n");
		return 1;		
	}		
	writeb(data,lpc_addr+LPC_DATA_PORT62);
	return 0;
}

static BYTE ec_read_data(BYTE *pData)
{
	if(ec_ob_full())
	{
		printk(KERN_ERR "[ecramdev]ec_read_data:O/P buffer error!\n");
		return 1;			
	}		
	*pData=readb(lpc_addr+LPC_DATA_PORT62);
	return 0;
}

int read_ec_ram(BYTE index, BYTE *Data)
{
	if(!Data)
	{	
		printk(KERN_ERR "[ecramdev]read_ec_ram:point NULL error!\n");
		return -EFAULT;
	}		
	#if DEBUG
	printk(KERN_INFO "[ecramdev]read_ec_ram:read ec ram start!\n");
	#endif
	if(ec_write_cmd(EC_RAM_READ_CMD))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ram:ec_write_cmd EC_RAM_READ_CMD error!\n");
		return -EFAULT;		
	}		

	if(ec_write_data(index))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ram:ec_write_data error!\n");
		return -EFAULT;		
	}		
	#if DEBUG
	printk(KERN_INFO "[ecramdev]read_ec_ram:read ec ram send addr=0x%x ok\n",index); 
	#endif	
	if(ec_read_data(Data))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ram:ec_read_data error!\n");
		return -EFAULT;			
	}		
	#if DEBUG
	printk(KERN_INFO "[ecramdev]read_ec_ram:read addr(0x%x)= 0x%x\n",index,*Data); 
	#endif
	return 0;
}

int write_ec_ram(BYTE index,BYTE Data)
{
	#if DEBUG
	printk(KERN_INFO "[ecramdev]ec_write_ram:write ec ram start!\n");
	#endif
	if(ec_write_cmd(EC_RAM_WRITE_CMD))
	{
		printk(KERN_ERR "[ecramdev]ec_write_ram:ec_write_cmd EC_RAM_WRITE_CMD error!\n");
		return -EFAULT;		
	}	

	if(ec_write_data(index))
	{	
		printk(KERN_ERR "[ecramdev]ec_write_ram:ec_write_data error!\n");
		return -EFAULT;	
	}
	
	#if DEBUG
	printk(KERN_INFO "[ecramdev]ec_write_ram:write ec ram send addr=0x%x ok\n",index);
	#endif 	
	
	if(ec_write_data(Data))
	{
		printk(KERN_ERR "[ecramdev]ec_write_ram:ec_write_data error!\n");
		return -EFAULT;		
	}	
	
	#if DEBUG
	printk(KERN_INFO "[ecramdev]ec_write_ram:write ec ram [0x%x]=0x%x ok\n",index,Data);	
	#endif
	
	return 0;
}

int read_ec_ex_ram(BYTE addrh, BYTE addrl, BYTE *Data)
{
	if(!Data)
	{	
		printk(KERN_ERR "[ecramdev]read_ec_ex_ram:point NULL error!\n");
		return -EFAULT;
	}		
	
	#if DEBUG
	printk(KERN_INFO "[ecramdev]read_ec_ex_ram:read ec ram start!\n");
	#endif
	
	if(ec_write_cmd(EC_RAM_READ_EXCMD))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ex_ram:ec_write_cmd EC_RAM_READ_EXCMD error!\n");
		return -EFAULT;		
	}		

	if(ec_write_data(addrh))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ex_ram:ec_write_data error!\n");
		return -EFAULT;		
	}
	
	if(ec_write_data(addrl))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ex_ram:ec_write_data error!\n");
		return -EFAULT;		
	}
	
	#if DEBUG		
	printk(KERN_INFO "[ecramdev]read_ec_ex_ram:read ec ram send addr=0x%x,0x%x ok\n",addrh,addrl); 
	#endif
		
	if(ec_read_data(Data))
	{
		printk(KERN_ERR "[ecramdev]read_ec_ex_ram:ec_read_data error!\n");
		return -EFAULT;			
	}	
	
	#if DEBUG	
	printk(KERN_INFO "[ecramdev]read_ec_ex_ram:read addr(0x%x,0x%x)= 0x%x\n",addrh,addrl,*Data); 
	#endif
	
	return 0;
}

int write_ec_ex_ram(BYTE addrh, BYTE addrl, BYTE Data)
{
	#if DEBUG
	printk(KERN_INFO "[ecramdev]write_ec_ex_ram:write ec ram start!\n");
	#endif
	
	if(ec_write_cmd(EC_RAM_WRITE_EXCMD))
	{
		printk(KERN_ERR "[ecramdev]write_ec_ex_ram:ec_write_cmd EC_RAM_WRITE_EXCMD error!\n");
		return -EFAULT;		
	}	

	if(ec_write_data(addrh))
	{	
		printk(KERN_ERR "[ecramdev]write_ec_ex_ram:ec_write_data error!\n");
		return -EFAULT;	
	}
	
	if(ec_write_data(addrl))
	{	
		printk(KERN_ERR "[ecramdev]write_ec_ex_ram:ec_write_data error!\n");
		return -EFAULT;	
	}
	
	#if DEBUG
	printk(KERN_INFO "[ecramdev]write_ec_ex_ram:write ec ram send addr=0x%x,0x%x ok\n",addrh,addrl);
	#endif 	
	
	if(ec_write_data(Data))
	{
		printk(KERN_ERR "[ecramdev]write_ec_ex_ram:ec_write_data error!\n");
		return -EFAULT;		
	}	
	
	#if DEBUG
	printk(KERN_INFO "[ecramdev]write_ec_ex_ram:write ec ram [ix%x,0x%x]=0x%x ok\n",addrh,addrl,Data);	
	#endif
	
	return 0;
}


int ec_io_init(void)
{
	lpc_addr = (BYTE *)ioremap(LPC_IO_ADDR,LPC_IO_SIZE);
  if(!lpc_addr)
  {
  		printk(KERN_ERR "[ecramdev]ec_io_init:init io mem error!\n");  
  		return -EFAULT;	
  }		
  #if DEBUG
	printk(KERN_INFO "[ecramdev]ec_io_init:init io mem ok!(0x%x)\n",lpc_addr); 
	#endif
	return 0; 
}

void ec_io_release(void)
{
	if(lpc_addr)
		iounmap(lpc_addr);
	
	if(ecram_resource)
	{	
		release_mem_region(LPC_IO_ADDR,LPC_IO_SIZE);
		ecram_resource = NULL;	
	}	
	
	return ;
}
		
int ecram_open(struct inode *inode, struct file *filp)
{
    struct ecram_dev *dev;
    
    int num = MINOR(inode->i_rdev);

    if (num >= EC_RAM_DEV_NR_DEVS) 
            return -ENODEV;
    dev = &ecram_devp[num];
    
    if(!dev_num)
    {
    	if(ec_io_init())
    	{
    		printk(KERN_ERR "[ecramdev]ecram_open:ec_io_init error!\n");  
    		return -ENODEV;
    	}		
    }		
    dev_num++;
    
    filp->private_data = dev;
    printk(KERN_INFO "ecramdev:open devices ok!\n");    
    return 0; 
}

int ecram_release(struct inode *inode, struct file *filp)
{
	if(dev_num)
		dev_num--;
	if(!dev_num)
		ec_io_release();	
  return 0;
}

static ssize_t ecram_read(struct file *filp, char __user *buf, size_t size, loff_t *ppos)
{
  int ret = 0;

  return ret;
}

static ssize_t ecram_write(struct file *filp, const char __user *buf, size_t size, loff_t *ppos)
{
  int ret = 0;

  return ret;
}

static loff_t ecram_llseek(struct file *filp, loff_t offset, int whence)
{ 
    loff_t newpos = 0;

    return newpos;
}

static long ecram_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
	void __user *argp = (void __user *)arg;
	uint8_t err;
	ecram_info_s ecram_info;
	
	switch (cmd) 
	{
		case EC_RAM_READ:
		   err = raw_copy_from_user((void *)(&ecram_info), argp, sizeof(ecram_info_s));
		   err |= read_ec_ram(ecram_info.addrl,&ecram_info.val);
		   err = raw_copy_to_user(argp, (void *)(&ecram_info), sizeof(ecram_info_s));
			break;
	
		case EC_RAM_WRITE:
			err = raw_copy_from_user((void *)(&ecram_info), argp, sizeof(ecram_info_s));
			err |= write_ec_ram(ecram_info.addrl,ecram_info.val);
			break;
	
		case EC_RAM_EX_READ:
		   err = raw_copy_from_user((void *)(&ecram_info), argp, sizeof(ecram_info_s));
		   err |= read_ec_ex_ram(ecram_info.addrh,ecram_info.addrl,&ecram_info.val);
		   err = raw_copy_to_user(argp, (void *)(&ecram_info), sizeof(ecram_info_s));
			break;
	
		case EC_RAM_EX_WRITE:
			err = raw_copy_from_user((void *)(&ecram_info), argp, sizeof(ecram_info_s));
			err |= write_ec_ex_ram(ecram_info.addrh,ecram_info.addrl,ecram_info.val);
			break;
				
		default:
			err = -ENOTTY;
			break;
	}
	
	return err;	
}
	
static const struct file_operations ecram_fops =
{
  .owner = THIS_MODULE,
  .llseek = ecram_llseek,
  .read = ecram_read,
  .write = ecram_write,
  .open = ecram_open,
  .unlocked_ioctl = ecram_ioctl,
  .release = ecram_release,
};

static int ecramdev_init(void)
{
  int result;
  int i;
  dev_t devno;

  if (ecram_major)
  {	  	
 		devno = MKDEV(ecram_major, 0);
    result = register_chrdev_region(devno, 2, "ecram");
    if(result<0)
    {
    	printk(KERN_ERR "[ecramdev]ecramdev_init:register dev no(%d) error!\n",ecram_major);
    }		
  }
  
  if((result<0)||(!ecram_major))
  {
    result = alloc_chrdev_region(&devno, 0, 2, "ecram");
    ecram_major = MAJOR(devno);
    printk(KERN_INFO "[ecramdev]ecramdev_init:register dev no(%d) ok!\n",ecram_major);
  }  
  
  if (result < 0)
  {	
  	printk(KERN_ERR "[ecramdev]ecramdev_init:alloc_chrdev_region error!\n");
    return result;
	}
	
  cdev_init(&cdev, &ecram_fops);
  cdev.owner = THIS_MODULE;
  cdev.ops = &ecram_fops;
  
  result = cdev_add(&cdev, MKDEV(ecram_major, 0), EC_RAM_DEV_NR_DEVS);
  if(result)
  	goto fail_malloc;
 
 	ecram_class = class_create(THIS_MODULE, EC_RAM_CLASS_NAME);
  if (IS_ERR(ecram_class)) {
  		result = PTR_ERR(ecram_class);
      goto out_unregister_cdev;
  } 
 
    dev = device_create(ecram_class, NULL, devno, NULL, EC_RAM_DEV_NAME);
    if (IS_ERR(dev)) {
        result = PTR_ERR(dev);
        goto out_del_class;
    }
      
  ecram_devp = kmalloc(EC_RAM_DEV_NR_DEVS * sizeof(struct ecram_dev), GFP_KERNEL);
  if (!ecram_devp)   
  {
    result =  - ENOMEM;
    goto out_del_dev;
  }
  memset(ecram_devp, 0, sizeof(struct ecram_dev));
  
  for (i=0; i < EC_RAM_DEV_NR_DEVS; i++) 
  {
        ecram_devp[i].size = EC_RAM_DEV_SIZE;
        ecram_devp[i].data = kmalloc(EC_RAM_DEV_SIZE, GFP_KERNEL);
        memset(ecram_devp[i].data, 0, EC_RAM_DEV_SIZE);
  }
  dev_num = 0;
  lpc_addr = NULL;
  printk(KERN_INFO "ecramdev:init devices ok,version:%s\n",EC_RAM_DRV_VER);  
  return 0;

	out_del_dev:
			device_destroy(ecram_class, MKDEV(ecram_major, 0));
	out_del_class:
	    class_destroy(ecram_class);
	out_unregister_cdev:
	    cdev_del(&cdev);
  fail_malloc: 
  	unregister_chrdev_region(devno, 1);
  
  return result;
}

static void ecramdev_exit(void)
{
	if(lpc_addr)
		iounmap(lpc_addr);
	device_destroy(ecram_class, MKDEV(ecram_major, 0));	
	class_destroy(ecram_class);
  cdev_del(&cdev);   
  kfree(ecram_devp);     
  unregister_chrdev_region(MKDEV(ecram_major, 0), 2); 
}

MODULE_AUTHOR("zhanglh7@lenovo.com");
MODULE_DESCRIPTION("EC Ram Driver");
MODULE_VERSION(EC_RAM_DRV_VER);
MODULE_LICENSE("GPL");

module_init(ecramdev_init);
module_exit(ecramdev_exit);
