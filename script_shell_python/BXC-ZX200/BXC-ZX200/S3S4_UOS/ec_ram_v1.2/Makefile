ifneq ($(KERNELRELEASE),)

obj-m := ec_ram_dev.o

else
	
KDIR := /usr/src/linux-headers-4.19.0-arm64-desktop/
all:
	make -C $(KDIR) M=$(PWD) modules -Wall 
clean:
	rm -f *.ko *.o *.mod.o *.mod.c *.symvers

endif
