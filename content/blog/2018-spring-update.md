# postmarketOS and Low Level Liberation (Mediatek Phones)

## Introducing #postmarketOS-lowlevel
postmarketOS aims to give a ten year life cycle to mobile phones. It boils down to using a simple and sustainable architecture borrowed from typical Linux distributions instead of using Android's build system. The project is at an early stage and not useful for most people at this point. Check out the [front page we just updated](https://postmarketos.org) for more information, the [previous blog post for recent achievements](https://postmarketos.org/blog/2017/12/31/219-days-of-postmarketOS/), and the [closed pull requests](https://github.com/postmarketOS/pmbootstrap/pulls?q=is%3Apr+is%3Aclosed) to be informed about what's going on up to the current minute.

As we are a community project, that [doesn't tell people what they can and can not work on](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#why-we-evolve-in-many-directions), we have people on board with a broad range of interests and skill levels. Recently a small hacking group [#postmarketOS-lowlevel](https://matrix.to/#/#postmarketos-lowlevel:disroot.org) has emerged, and its driving forces [@craigcomstock](https://github.com/craigcomstock) and [@McBitter](https://github.com/McBitter) will introduce you to the madness that awaits you when digging deeper and deeper in the stack.

## MT6735P: Trying To Run An Open Bootloader
I ([McBitter](https://github.com/McBitter)) am currently trying to get the MT6735P SoC to boot both the preloader (1st programmable bootloader) and [Little Kernel](https://github.com/littlekernel/lk/wiki/Introduction) (LK), and am also in the process of adding some in-depth documentation about the chipset to the [wiki](https://wiki.postmarketos.org/wiki/Mediatek).

LK is a widely used bootloader for Android devices.  Besides booting the device, it also implements fastboot mode, which can be used to flash new operating systems to a device.  LK is open source under the MIT license, but vendors typically fork the code without sharing the source code with their customers.  That's the case on MediaTek devices, so one of the challenges will be to adjust the mainline LK code to run on them.  In order to do that, my goal is to figure out how the chip can be programmed.  That knowledge would allow us to boot the mainline Linux kernel.  Ideally, the same LK source could be shared between various SoCs, just like is possible with other bootloaders, such as U-Boot.

### Instrumentation with Qemu
Having no instrumentation makes reverse engineering an SoC difficult, and leads to a lot of dead ends.  To make it easier, Unreasonable and I decided to implement instrumentation using Qemu.  Our approach would be to send memory read commands to the board and mirror the device's memory in Qemu.  This would allow us to attach a debugger and step through code.  Being able to observe the code as it ran would greatly help us to understand how it worked, and therefore, how the device worked.

I knew that the MediaTek Boot ROM had an interface that would let us read from and write to memory, so I set about finding a way to access it.  The interface is found on UART0, which normally isn't accessible, but is also bootstrapped on the USB interface.  After playing around a bit with the protocol {link documentation here}, I got to something like [this](https://github.com/McBitter/flasher/blob/master/main.c).  Most of the code was constructed from usbmon captures I got while flashing with the SP Flashtool.  After painstakingly reproducing the protocol in C and adding in some diagnostics for probing the memory area, I finally came up with the following code to dump the interrupt vector table:

    for (int i = 0; i < 4; i++)
    {
        unsigned int addr = 0x00000000;
        unsigned int numBytes = 0x1;
        unsigned char comm = 0xD1;
        addr += i * 4;
        wprint(&comm, 1);
        rprint(1);
        littleToBig(&addr, 4);
        wprint((unsigned char*)&addr, 4);
        rprint(4);
        littleToBig(&numBytes, 4);
        wprint((unsigned char*)&numBytes, 4);
        rprint(4);
        rprint(2); // ack status
        printf("-------------------------------------\n");
        rprint(4); // read result
        printf("-------------------------------------\n");
        rprint(2); // command done
    }

Normally, the interrupt vector table on ARM chips is found at the address 0x00000000.  However, on some older SoCs, you can also find it at 0xffff0000, which would allow us to read the data from both addresses.  Armed with this knowledge, I tried to read the vector table; unfortunately, the read commands all failed.  I was confused about those results, so we tried to read the address 0x10206044 (some eFUSE-related stuff).  This returned the result I was expecting.  After I tried a few more addresses connected to specific function blocks, it became apparent that MediaTek had added restrictions to the read32 and read16 commands.  As such, I was forced to admit defeat.

After the frustration Unreasonable and I had been through, we decided that it was a good time to take a break of a few weeks from working on this.  We came back energized, and ready to give it another shot.  This time I took a step back to look over some leaked source files, which I had misplaced.

After creating a new platform for Coolpad, everything seemed fine, until I tried to flash it.  SP Flashtool reported that it wasn't able to initialize the DRAM.  Armed with new purpose, I looked at emi.c in the leaked source files, where memory gets initialized.  What I found seemed promising, so I fired up IDA to gather the actual timing information from the manufacturer's preloader.  (That is, the first bootloader after BootROM.)  On my first try, a byte search didn't return anything.

Since emi.c contained calibration information, I decided to see if I could find a similar pattern inside the original preloader.  For that search, I used KMQ8X000SA_B414 calibration data that I found in emi.c.  Since it's all about getting lucky, I selected a random pattern of 0xAA00AA00 from the calibration data.

After I ran the search, I immediately got a result.  It seemed obvious that I'd finally hit the jackpot, and found the location of the Coolpad's DRAM timing information.

Finally, here's some unsorted data for everybody to decipher: https://gist.github.com/McBitter/3a90851a6bed1efecdeb03e358a68895

### No Serial Access
In the postmarketOS community, we already know that having serial access to a device is an invaluable tool when you are debugging the booting process (on higher levels that is the kernel and initramfs). But the `UART0` serial port is not wired to the circuit board for most Mediatek phones. "I could do hardware modification, but all the side effects of this outweight the risks." So he evaluated alternative instrumentation methods: "just spam data to USB. But a more clever way would be to [interface Qemu with the USB interface](https://stackoverflow.com/a/2615816)."

## MT6260: Blinking LED As First Step To Porting Open Baseband Firmware
### Why is proprietary cellular firmware a problem again?
Having the main processor of a phone running a secure operating system would already be a great achievement in today's mobile word. And in our opinion, that starts with running [official kernel releases](http://www.kroah.com/log/blog/2018/02/05/linux-kernel-release-model/) on these, instead of inofficial and outdated forks where no one can realistically keep up with security patches.

However, we must not forget about the peripherals inside the device, which run their own firmware. Oftentimes they are able to compromise the whole system, and they are ["of dubious quality, poorly understood, entirely proprietary, and wholly insecure by design"](https://www.osnews.com/story/27416/The_second_operating_system_hiding_in_every_mobile_phone).

One way to deal with these is implementing kill-switches and sandboxing the cellular modem (like it is planned for in the [Librem 5](https://puri.sm/shop/librem-5/) and [Neo900](https://neo900.org/)). That means while you still don't know what it is doing, you can at least be sure that it is turned off when it should be. Another way is analyzing and binary patching the existing firmware files.

But let's be honest here, isn't it outrageous that even the projects coming from people who value free and open software, security and privacy, need to work around this gaping security hole present in every phone ever made? Yes it is a daunting task to truly fix this with an open source implementation and it will take forever. But we have to start somewhere, and letting more time pass by won't help either!

### Porting OsmocomBB to Fernvale
The good news is, there is already a free software implementation of a GSM baseband called [OsmocomBB](https://osmocom.org/projects/baseband/wiki). But it is only compatible with phones based on the TI Calypso chipset, such as the Motorola C123. Given that the Motorola C123 came out in 2006 and is no longer produced, OsmocomBB's use is limited unless we can port it to newer platforms.

<!-- add picture of motorola c123? -->

[@unreasonable](https://github.com/craigcomstock) chose the Fernvale plattform as new target. There's a [nice introduction talk](https://media.ccc.de/v/31c3_-_6156_-_en_-_saal_1_-_201412282145_-_fernvale_an_open_hardware_and_software_platform_based_on_the_nominally_closed-source_mt6260_soc_-_bunnie_-_xobs) by its creators that explains how Fernvale was created to enable open source engineers to build phones and other small devices with the cheap MT6260 SoC. Not only do they hack the hardware, but also provide a justifiable concepts to re-implement necessary code from abstracting facts found in leaked source core instead of copy and pasting.

So with Fernvale, you have three development boards centered around the MT6260 chip, and that way it is much easier to develop and debug your own software compared to having the chip integrated to a phone. But once custom firmware runs on the cellular modem on Fernvale, it will run on existing phones with the same SoC as well.

Part of the Fernvale project are the first-stage boot environment called [Fernly](https://github.com/xobs/fernly/) as well as a port of the [NuttX](https://en.wikipedia.org/wiki/NuttX) real-time operating system.

### Blinking LED
[@unreasonable](https://github.com/craigcomstock) had the first success already, as you can see on the right: "Fernly already had simple code to turn on and off the LED on the Fernvale hardware. I reworked the linker scripts and startup assembly code in OsmocomBB to work on fernvale hardware and was able to make an LED blinking firmware in OsmocomBB!"

<!-- TODO: add blinking LED gif! -->

Afterwards he continued to replace the functions in the layer one firmware in OsmocomBB with stubs that work on Fernvale to see if he can get more of OsmocomBB running. But he found out that the configuration in his linker script didn't provide enough space for the compiled firmware.

### Future Plans
Now we need to compare again Fernly, Fernvale-NuttX and OsmocomBB and arrive at a solution. Possibly it will be to coordinate slightly with [@McBitter](https://github.com/McBitter)'s work regarding the much larger system memory (also called `EMI`, `DRAM` or `PSRAM`). It could be used to load a larger firmware needed for OsmocomBB layer one.


The steps along the way are these:
* Layer one firmware in OsmocomBB, will enable using say fernvale hardware along with a laptop to do 2G voice/text/data as you can currently with supported old motorola phones in OsmocomBB
* Create layer1 as a library in OsmocomBB to use in an app for nuttx, bringing full userspace phone functionality to a small operating system like nuttx
* Attempt to support this layer1 on newer chipsets like MT6735 use this layer1 library and other bits of OsmocomBB project to create a RILD or oFono compatible interface to Mediatek baseband/RF chipsets
* Extend OsmocomBB to work with GSM protocols greater than 2G on mediatek chipsets (3G, 4G, LTE, ...)

### Help Wanted

(TODO)
