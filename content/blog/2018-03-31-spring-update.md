title: "postmarketOS and Low Level Liberation (Mediatek Phones)"
date:  2018-03-31
---

# Introducing #postmarketOS-lowlevel
postmarketOS aims to give a ten year life cycle to mobile phones.  It boils down to using a simple and sustainable architecture borrowed from typical Linux distributions instead of using Android's build system.  The project is at an early stage and isn't useful for most people at this point.  Check out the newly-updated [front page](https://postmarketos.org) for more information, the [previous blog post](https://postmarketos.org/blog/2017/12/31/219-days-of-postmarketOS/) for recent achievements, and the [closed pull requests](https://github.com/postmarketOS/pmbootstrap/pulls?q=is%3Apr+is%3Aclosed) to be informed about what's going on up to the current minute.

As we are a community project, that [doesn't tell people what they can and can not work on](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#why-we-evolve-in-many-directions), we have people on board with a broad range of interests and skill levels.  Recently a small hacking group [#postmarketOS-lowlevel](https://matrix.to/#/#postmarketos-lowlevel:disroot.org) has emerged, and its driving forces [@craigcomstock](https://github.com/craigcomstock) and [@McBitter](https://github.com/McBitter) will introduce you to the madness that awaits you when digging deeper and deeper in the stack.

# MT6735P: Trying To Run An Open Bootloader
Being able to use open source software as far down as the bootloader would be a significant step in giving users full control of their devices.  [McBitter](https://github.com/McBitter) has been working on getting the [Little Kernel](https://github.com/littlekernel/lk/wiki/Introduction) (LK) bootloader running on the MT6735P System-on-Chip (SoC), as a starting point for open bootloaders.

LK is a widely used bootloader for Android devices.  Besides booting the device, it also implements fastboot mode, which can be used to flash new operating systems to a device.  LK is open source under the MIT license, but vendors typically fork the code without making the source code available to their customers.  That's the case on MediaTek devices, so one of the challenges will be to adjust the mainline LK code to run on them.  In order to do that, McBitter's goal is to collect information on programming MediaTek SoCs.  That knowledge would be a significant step toward booting the mainline Linux kernel on MediaTek devices.  Ideally, the same LK source could be shared between various SoCs, which would give us a unified bootloader between platforms.

## No Serial Access
In the postmarketOS community, we've found that a serial console is an invaluable tool to help us troubleshoot when bringing up a new device.  Most MediaTek devices don't have their serial ports wired to the boards, though, which makes them difficult to bring up.  McBitter and [Unreasonable](https://github.com/craigcomstock) have been working on MediaTek devices, and needed a way to debug them.  "I could do hardware modification," McBitter said, "but all the side effects of this outweigh the risks."  It is possible to [connect a serial cable](http://www.stevenhoneyman.co.uk/2014/11/mtk-mediatek-debug-cable.html) to the USB port on many MediaTek devices, but McBitter and Unreasonable had an idea on how to take it a step further.

## Instrumentation with Qemu
During their work with MediaTek chips, McBitter and Unreasonable thought it might be possible to implement instrumentation using Qemu.  Their approach would be to send memory read commands to the board and mirror the device's memory in Qemu.  They would then be able to attach gdb to Qemu's [gdb stub](https://stackoverflow.com/a/2615816), and view code as it ran.  Being able to step through LK and OsmocomBB in a debugger would make getting them running much easier.

[![](/static/img/2018-03-31/Instrumentation-overview.png){: class="fl w-60 ml3 mr3"}](/static/img/2018-03-31/Instrumentation-overview.png)

<div class="cf"></div>

Using an interface in the [MediaTek Boot ROM](http://read.pudn.com/downloads119/sourcecode/comm/mtk/507390/System_and_Debug/System_Service/BROM_Design_V2.0.0.pdf), McBitter worked on accessing MediaTek devices' memory via USB.  Based on USB captures taken while flashing with the SP Flashtool, McBitter wrote [test code](https://github.com/McBitter/flasher/blob/master/main.c) to read memory using that interface.  Unfortunately, MediaTek placed restrictions to the memory locations that the Boot ROM will read.  The memory restrictions would make debugging with Qemu impossible, so McBitter decided to move on to another project.

[![](/static/img/2018-03-31/Memory-read-test.png){: class="fl ml3 mr3"}](/static/img/2018-03-31/Memory-read-test.png)

<div class="cf"></div>

## DRAM Calibration on Coolpad
After a break of a few weeks, McBitter decided to see what he could learn from leaked source files to a MediaTek preloader.

McBitter created a new platform in the preloader for the Coolpad, but wasn't able to flash it.  SP Flashtool reported that it wasn't able to initialize the NAND flash memory, so McBitter searched for NAND timing information in the Coolpad's preloader.  A byte search in IDA didn't return anything, so McBitter took a look at the memory initialization code in the preloader.

[![](/static/img/2018-03-31/Coolpad-front-thumb.jpg){: class="fl w-20 ml3"}](/static/img/2018-03-31/Coolpad-front.jpg)

[![](/static/img/2018-03-31/Coolpad-back-opened-thumb.jpg){: class="fl w-20 ml3"}](/static/img/2018-03-31/Coolpad-back-opened.jpg)

<div class="cf"></div>

The code contained calibration information, so McBitter decided to look for patterns from the calibration data in the Coolpad's memory.  A common pattern in the calibration data for the KMQ8X000SA_B414 NAND flash chip was 0xAA00AA00, so McBitter searched for that.  There was an immediate result, and McBitter was able to dump the [calibration data](https://gist.github.com/McBitter/3a90851a6bed1efecdeb03e358a68895).

[![](/static/img/2018-03-31/IDA-memory-calibration.png){: class="fl ml3 mr3"}](/static/img/2018-03-31/IDA-memory-calibration.png)

<div class="cf"></div>

# MT6260: Blinking LED As First Step To Porting Open Baseband Firmware
## Why is proprietary cellular firmware a problem again?
Having the main processor of a phone running a secure operating system would already be a great achievement in today's mobile word. And in our opinion, that starts with running [official kernel releases](http://www.kroah.com/log/blog/2018/02/05/linux-kernel-release-model/) on these, instead of inofficial and outdated forks where no one can realistically keep up with security patches.

However, we must not forget about the peripherals inside the device, which run their own firmware. Oftentimes they are able to compromise the whole system, and they are ["of dubious quality, poorly understood, entirely proprietary, and wholly insecure by design"](https://www.osnews.com/story/27416/The_second_operating_system_hiding_in_every_mobile_phone).

One way to deal with these is implementing kill-switches and sandboxing the cellular modem (like it is planned for in the [Librem 5](https://puri.sm/shop/librem-5/) and [Neo900](https://neo900.org/)). That means while you still don't know what it is doing, you can at least be sure that it is turned off when it should be. Another way is analyzing and binary patching the existing firmware files.

But let's be honest here, isn't it outrageous that even the projects coming from people who value free and open software, security and privacy, need to work around this gaping security hole present in every phone ever made? Yes it is a daunting task to truly fix this with an open source implementation and it will take forever. But we have to start somewhere, and letting more time pass by won't help either!

## Porting OsmocomBB to Fernvale
The good news is, there is already a free software implementation of a GSM baseband called [OsmocomBB](https://osmocom.org/projects/baseband/wiki). But it is only compatible with phones based on the TI Calypso chipset, such as the Motorola C123. Given that the Motorola C123 came out in 2006 and is no longer produced, OsmocomBB's use is limited unless we can port it to newer platforms.

<!-- add picture of motorola c123? -->

[@unreasonable](https://github.com/craigcomstock) chose the Fernvale plattform as new target. There's a [nice introduction talk](https://media.ccc.de/v/31c3_-_6156_-_en_-_saal_1_-_201412282145_-_fernvale_an_open_hardware_and_software_platform_based_on_the_nominally_closed-source_mt6260_soc_-_bunnie_-_xobs) by its creators that explains how Fernvale was created to enable open source engineers to build phones and other small devices with the cheap MT6260 SoC. Not only do they hack the hardware, but also provide a justifiable concepts to re-implement necessary code from abstracting facts found in leaked source core instead of copy and pasting.

So with Fernvale, you have three development boards centered around the MT6260 chip, and that way it is much easier to develop and debug your own software compared to having the chip integrated to a phone. But once custom firmware runs on the cellular modem on Fernvale, it will run on existing phones with the same SoC as well.

Part of the Fernvale project are the first-stage boot environment called [Fernly](https://github.com/xobs/fernly/) as well as a port of the [NuttX](https://en.wikipedia.org/wiki/NuttX) real-time operating system.

## Blinking LED
[@unreasonable](https://github.com/craigcomstock) had the first success already, as you can see on the right: "Fernly already had simple code to turn on and off the LED on the Fernvale hardware. I reworked the linker scripts and startup assembly code in OsmocomBB to work on fernvale hardware and was able to make an LED blinking firmware in OsmocomBB!"

<!-- TODO: add blinking LED gif! -->

Afterwards he continued to replace the functions in the layer one firmware in OsmocomBB with stubs that work on Fernvale to see if he can get more of OsmocomBB running. But he found out that the configuration in his linker script didn't provide enough space for the compiled firmware.

## Future Plans
Now we need to compare again Fernly, Fernvale-NuttX and OsmocomBB and arrive at a solution. Possibly it will be to coordinate slightly with [@McBitter](https://github.com/McBitter)'s work regarding the much larger system memory (also called `EMI`, `DRAM` or `PSRAM`). It could be used to load a larger firmware needed for OsmocomBB layer one.


The steps along the way are these:
* Layer one firmware in OsmocomBB, will enable using say fernvale hardware along with a laptop to do 2G voice/text/data as you can currently with supported old motorola phones in OsmocomBB
* Create layer1 as a library in OsmocomBB to use in an app for nuttx, bringing full userspace phone functionality to a small operating system like nuttx
* Attempt to support this layer1 on newer chipsets like MT6735 use this layer1 library and other bits of OsmocomBB project to create a RILD or oFono compatible interface to Mediatek baseband/RF chipsets
* Extend OsmocomBB to work with GSM protocols greater than 2G on mediatek chipsets (3G, 4G, LTE, ...)

## Help Wanted

(TODO)
