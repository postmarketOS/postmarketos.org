# postmarketOS and Low Level Liberation (Mediatek Phones)

## Introducing #postmarketOS-lowlevel
postmarketOS aims to give a ten year life cycle to mobile phones. It boils down to using a simple and sustainable architecture borrowed from typical Linux distributions instead of using Android's build system. The project is at an early stage and not useful for most people at this point. Check out the [front page we just updated](https://postmarketos.org) for more information, the [previous blog post for recent achievements](https://postmarketos.org/blog/2017/12/31/219-days-of-postmarketOS/), and the [closed pull requests](https://github.com/postmarketOS/pmbootstrap/pulls?q=is%3Apr+is%3Aclosed) to be informed about what's going on up to the current minute.

As we are a community project, that [doesn't tell people what they can and can not work on](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#why-we-evolve-in-many-directions), we have people on board with a broad range of interests and skill levels. Recently a small hacking group [#postmarketOS-lowlevel](https://matrix.to/#/#postmarketos-lowlevel:disroot.org) has emerged, and its driving forces [@craigcomstock](https://github.com/craigcomstock) and [@McBitter](https://github.com/McBitter) will introduce you to the madness that awaits you when digging deeper and deeper in the stack.

## MT6735P: Trying To Run An Open Bootloader
I ([McBitter](https://github.com/McBitter)) am currently trying to get the MT6735P SoC to boot both the preloader (1st programmable bootloader) and [Little Kernel](https://github.com/littlekernel/lk/wiki/Introduction) (LK), and in the process add some in-depth documentation about the chipset to the [wiki](https://wiki.postmarketos.org/wiki/Mediatek)."

LK is a widely used bootloader for Android devices.  Besides booting the device it also implements "fastboot mode", which can be used to flash new operating systems to a device.  LK is open source under the MIT license, but vendors typically fork the code without sharing the source with their customers.  That is the case on MediaTek devices, so one of the challenges will be to adjust the mainline LK code such that it runs on MediaTek devices.  In order to do that, the aim of his work "is to get actual useful knowledge on how the chip could be programmed and from that knowledge the mainline Linux kernel could be booted" as high level goal.  Ideally the same LK source could be shared between various SoCs, just like it is possible with other bootloaders like U-Boot.

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
I ([unreasonable](https://github.com/craigcomstock)) did some experimentation with the Fernly bootloader for MediaTek chipsets, to try to find the CONFIG_BASE {what exactly is this?} for my ZTE Obsidian.

At the address 0x20000008 I saw 6735, which matched the number of the SoC (MT6735M).  The MT6260 has its number at 0x80000008.  Finding the CONFIG_BASE could allow us to figure out more information, and let us work toward finding similar IP blocks to those in the MT6235 and MT6260.  We already know about the MT6235 and MT6260 from [OsmocomBB](https://bb.osmocom.org/), [Fernly](https://github.com/xobs/fernly), and other codebases.  If we were able to apply what we know about those chipsets to other chipsets, it could make reversing them much quicker.

My hope is that I'll be able to port OsmocomBB to the Fernvale development platform (based on the MT6260), and then possibly be able to port it to other MediaTek chipsets, such as the MT6735.  OsmocomBB is a Free Software implementation of a GSM baseband which has the goal of completely replacing proprietary baseband firmware.  Porting it to newer platforms would give users the opportunity to rely less on proprietary sofware, with the end goal of eliminating it completely.  Unfortunately, OsmocomBB currently is only compatible with phones based on the TI Calypso chipset, such as the Motorola C123.  Given that the Motorola C123 came out in 2006 and is no longer produced, OsmocomBB's use is limited unless we can port it to newer platforms.

I've gotten a start on porting OsmocomBB to the MT6260 by writing a firmware that simply blinks an LED.  That was mostly done by modifying linker scripts and startup assembly code.  Currently, I'm working on porting the OsmocomBB layer 1 firmware by stubbing out all the Calypso-specific functions.  Once that's done, I'll gradually migrate those functions to equivalents that work on the MT6260.

I've acquired a Racal 6103E 2G GSM test set, which should be a great help in developing and debugging layer 1 firmware.

That's it for now.  Let us know if you'd like us to write similar posts in the future!
