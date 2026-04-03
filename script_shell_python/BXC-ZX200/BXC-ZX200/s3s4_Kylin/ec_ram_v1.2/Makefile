ifneq ($(KERNELRELEASE),)

obj-m := ec_ram_dev.o

else
	
KDIR := /usr/src/kylin-headers-4.4.131-20200710-generic/
all:
	make -C $(KDIR) M=$(PWD) modules -Wall 
clean:
	rm -f *.ko *.o *.mod.o *.mod.c *.symvers

endif
