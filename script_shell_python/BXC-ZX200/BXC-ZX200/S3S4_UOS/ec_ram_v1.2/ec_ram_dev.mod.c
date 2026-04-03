#include <linux/build-salt.h>
#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0xd74c4fa0, "module_layout" },
	{ 0xc298e56, "param_ops_int" },
	{ 0x37a0cba, "kfree" },
	{ 0xdcb764ad, "memset" },
	{ 0x96bfa9bb, "device_destroy" },
	{ 0x6204b74, "kmem_cache_alloc_trace" },
	{ 0x122d0950, "kmalloc_caches" },
	{ 0x36d2d300, "class_destroy" },
	{ 0xfe2dab80, "device_create" },
	{ 0x3fd78f3b, "register_chrdev_region" },
	{ 0x85b051ff, "cdev_del" },
	{ 0xa42b9592, "__class_create" },
	{ 0x6091b333, "unregister_chrdev_region" },
	{ 0x54df74b3, "cdev_add" },
	{ 0x551e790f, "cdev_init" },
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0x1035c7c2, "__release_region" },
	{ 0x77358855, "iomem_resource" },
	{ 0x45a55ec8, "__iounmap" },
	{ 0xcc066231, "cpu_hwcaps" },
	{ 0x6b4b2933, "__ioremap" },
	{ 0x8610de5b, "cpu_hwcap_keys" },
	{ 0x6dfb912f, "arm64_const_caps_ready" },
	{ 0x6b2941b2, "__arch_copy_to_user" },
	{ 0xaf507de1, "__arch_copy_from_user" },
	{ 0x7c32d0f0, "printk" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "95937868F1ECA78532FB49B");
