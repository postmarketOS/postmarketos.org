# postmarketOS and Low Level Liberation (Mediatek Phones)

## Introducing #postmarketOS-lowlevel
postmarketOS aims to give a ten year life cycle to mobile phones. It boils down to using a simple and sustainable architecture borrowed from typical Linux distributions instead of using Android's build system. The project is at an early stage and not useful for most people at this point. Check out the [front page we just updated](https://postmarketos.org) for more information, the [previous blog post for recent achievements](https://postmarketos.org/blog/2017/12/31/219-days-of-postmarketOS/), and the [closed pull requests](https://github.com/postmarketOS/pmbootstrap/pulls?q=is%3Apr+is%3Aclosed) to be informed about what's going on up to the current minute.

As we are a community project, that [doesn't tell people what they can and can not work on](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#why-we-evolve-in-many-directions), we have people on board with a broad range of interests and skill levels. Recently a small hacking group [#postmarketOS-lowlevel](https://matrix.to/#/#postmarketos-lowlevel:disroot.org) has emerged, and its driving forces [@craigcomstock](https://github.com/craigcomstock) and [@McBitter](https://github.com/McBitter) will introduce you to the madness that awaits you when digging deeper and deeper in the stack.

## MT6735P: Trying To Run An Open Bootloader
Let's start with what [@McBitter](https://github.com/McBitter) is doing: "Well, I'm currently trying to get MT6735P SoC to boot both preloader (1st programmable bootloader) and [Little Kernel](https://github.com/littlekernel/lk/wiki/Introduction) (LK) and in the process from time to time add some in depth documentation about the chipset [to the wiki](https://wiki.postmarketos.org/wiki/Mediatek)." LK is widely used for Android devices, besides booting the device it also implements the "fastboot mode" that can be used to flash new operating systems to the device. Furthermore, LK is open source under the MIT license, so typically vendors fork the code without sharing the source with customers of the device. This is also the case here, so one of the challenges is to adjust the mainline LK code in a way that it runs on the Mediatek devices. In order to do that, the aim of his work "is to get actual useful knowledge on how the chip could be programmed and from that knowledge the [mainline] Linux kernel could be booted" as high level goal. Ideally the same LK source could be shared between various SoCs, just like it is possible with other bootloaders like U-Boot.

### No Serial Access
In the postmarketOS community, we already know that having serial access to a device is an invaluable tool when you are debugging the booting process (on higher levels that is the kernel and initramfs). But the `UART0` serial port is not wired to the circuit board for most Mediatek phones. "I could do hardware modification, but all the side effects of this outweight the risks." So he evaluated alternative instrumentation methods: "just spam data to USB. But a more clever way would be to [interface Qemu with the USB interface](https://stackoverflow.com/a/2615816)."

## MT6260: Blinking LED As First Step To Porting Open Baseband Firmware
[@craigcomstock](https://github.com/craigcomstock) is working on libre cellular network firmware. "My hope is that I will accomplish porting [osmocom-bb](https://bb.osmocom.org/) (2G baseband) to fernvale (mt6260) and then possibly porting this work to mt6735 and other mediatek chipsets. I have an initial blink LED firmware in osmocom-bb, mostly by modifying linker scripts and startup assembly code."

## Instrumentation with Qemu
A lack of instrumentation makes reverse engineering an SoC difficult, and leads to a lot of dead ends.  To make it easier, we (McBitter and Unreasonable) decided to implement instrumentation using Qemu.  Our approach would be to send memory read commands to the board and store the results in Qemu's state machine.  We knew that the MediaTek Boot ROM had an interface that would let us do so.  The interface is found on UART0, which normally isn't accessible, but is also bootstrapped on the USB interface.

After playing around a bit with the protocol {link documentation here}, I (McBitter) got to something like [this](https://github.com/McBitter/flasher/blob/master/main.c).  Most of the code was constructed from usbmon captures while flashing with the SP Flashtool.  After painstakingly reproducing the protocol in C and adding in some diagnostics for probing the memory area, I finally came up with the following code to dump the interrupt vector table:

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

Normally, the interrupt vector table on ARM chips is found at the address 0x00000000.  However, on some older SoCs, you can also find it at 0xffff0000 {bootrom location?}, which would allow the programmer to read the data from both addresses.  Armed with this knowledge, we tried to read the vector table; unfortunately, we only got results about read failures.  We were confused about those results, so we tried to read the address 0x10206044 (some eFUSE-related stuff).  This returned the result we were expecting.  After we tried a few more addresses connected to specific function blocks, it became apparent that MediaTek had added restrictions to the read32 and read16 commands.  As such, we were forced to admit defeat.

{Unreasonable's block start}

I (Unreasonable) did some experimenting with the Fernly bootloader for MediaTek chipsets, to find the config_base {what exactly is this?} for my ZTE Obsidian.  At 0x20000008 I saw 6735, which matched the number of the SoC (MT6735M).  The MT6260 has this at 0x80000008.  Finding the config_base could allow us to reverse more information, and let us work toward finding similar IP blocks {what does he mean here?} as are in the MT6235 and MT6260, which we already know about from OsmocomBB, Fernly, and other codebases.

My hope is that I'll be able to port OsmocomBB (a 2G baseband) to Fernvale (MT6260), and then possibly be able to port it to other MediaTek chipsets, such as the MT6735.

I've written an initial firmware to blink an LED in OsmocomBB, mostly by modifying linker scripts and startup assembly code.  Currently, I'm working on OsmocomBB layer 1 firmware by stubbing out all the Calypso-specific functions.  Once that's done, I'll gradually migrate those functions to equivalents that work on MT6260.

I've acquired a Racal 6103E 2G GSM test set, which should be a great help in developing and debugging layer 1 firmware.

{Unreasonable's block end}

After the frustration we'd been through, we decided that it was a good time to take a break of a few weeks from working on this.  Once we returned, we, filled with Thor's lightning, thought it was time for round 2.  This time we took a step back to look over some leaked source files, which I had misplaced.

After creating a new platform for Coolpad, everything seemed fine, until we tried to flash.  SP Flashtool reported that it wasn't able to initialize the DRAM.  Armed with new purpose, we looked at emi.c in the leaked source files, where memory gets initialized.  What we found seemed promising, so we fired up IDA to gather the actual timing information from the manufacturer's preloader.  (That is, the first bootloader after BootROM.)  On our first go, a byte search didn't return anything.

Since emi.c contained calibration information, I decided to see if there was a similar pattern inside the original preloader.  For that search, we are going to use KMQ8X000SA_B414 calibration data that we found in emi.c.  Since it's all about getting lucky, I selected a random pattern of 0xAA00AA00 from the struct {which struct?}.

After we ran the search, we immediately got a result.  It seemed obvious that we'd hit the jackpot.  A few fields from the source file {significance?}:

    0x0, /* sub_version /
    0x0203, / TYPE */
    9,

Finally, here's some unsorted data for everybody to decipher: https://gist.github.com/McBitter/3a90851a6bed1efecdeb03e358a68895

That's it for now.  Let us know if you'd like us to write similar posts in the future!

# TODO
(original text below, needs to be integrated into the above)


Due to lack of instrumentation reversing can be chaotic and face many dead ends even to the point of giving up. That being said, let's get started on this journey.

To tackle this problem we (me and Unreasonable) decided that it would be helpful to implement qemu based instrumentation. In our heads we had this dream
of sending memory read commands to the board and getting result back, storing it in qemu's state machine. We knew of brom bare bones interface that's
normally rolled up on UART0, but normally it isn't wired to the circuit board. Luckily for us, the same protocol gets bootstrapped on USB interface. (Link to mediatek page or something)

After playing around a bit with the protocol (there is documentation found on the net) we got to something like this: https://github.com/McBitter/flasher/blob/master/main.c (horrible code ahead, proceed
on your own risk). Most of that code was constructed from usbmon captures on linux box while flashing with SP Flashtool. After painstakingly reproducing protocol in C and adding some diagnostics
for probing the memory area, following code was written:

    printf("-------------------------------------\n");

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

    return 0;

Normally at address 0x0 resides the vector table (http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0552a/BABIFJFG.html - mind the fact that it's about cortex-m series ;) ),
but during early stages brom could be there due to memory controller being able to relocate specific memory areas. On some older SoC's the 0x0 address was mapped to 0xffff0000 (bootrom location) address so in essence
programmer could just get the same data from both addresses.
Armed with this assumption/knowledge I first tried to access vector table, but console was only showing -1 results about read failures. Filled with confusion about the results, it was time for getting the hands dirty
and changed the read address to 0x10206044 (some eFUSE related stuff) and got back the expected result. After mindlessly trying few more addresses that were connected to specific function blocks I was forced to admit defeat that
on newer brom they added limitation to read32 and read16 commands.

(Unreasonable's block? Fit it here somehow...)
I did some experimenting with fernly bootloader to find the config_base for my ZTE Obsidian (mt6735M), at 0x20000008 I see 6735.
MT6260 has this config_base at 0x80000008. Finding the config_base could lead to reversing more information and working towards finding similar IP blocks as are in MT6235 and MT6260 which
we already know about from osmocom-bb and fernly and other code bases.

My hope is that I will accomplish porting osmocom-bb (2G baseband) to fernvale (mt6260) and then possibly porting this work to mt6735 and other mediatek chipsets.

I have an initial blink LED firmware in osmocom-bb, mostly by modifying linker scripts and startup assembly code.
Currently I am working on osmocom-bb layer1 firmware by stubbing out all of the calypso specific functions and then will gradually migrate these functions to equivalents that work on mt6260.
I have acquired a Racal 6103E 2G GSM test set which should be an excellent aid in developing/debugging layer1 firmware.
(Unreasonable's block end)

Since winning and losing ratio is competing against us it was decided that it's time to take a tiny (few weeks :O) break from the development.
On return, filled with Thor's lighting strike it was a time for round x + 99. This time a step back was taken to rely on leaked source files that I accidentally misplaced like year ago(whoops).
After creating new platform for Coolpad everything seemed fine until flashing itself when SP Flashtool reported that it was unable to init the DRAM. Well... why cannot stuff work on the first try.
Armed with new purpose search inside leaked sources led to emi.c where memory gets initialized. All this data seemed promising so fired up IDA to gather the actual timing information
from manufacturer's preloader (the 1'st bootloader after brom). On first go byte search didn't return anything, maybe that has something to do with IDA being subborn or something? Anyway,
let's try something different.
Since emi.c (EMI - external memory interface) contained calibration information, I decided to give it a shot if there is similar pattern inside original preloader. For search we are going to use
KMQ8X000SA_B414 calibration data that was provided to us from emi.c. Since it's all about getting lucky I selected random pattern from struct "0xAA00AA00".
After running the search we immediately got a result and it seemed obvious that we've hit the jackpot on this one. Few fields from the source file:
0x0, /* sub_version /
0x0203, / TYPE */
9,

Finally unsorted data for everybody to decipher: https://gist.github.com/McBitter/3a90851a6bed1efecdeb03e358a68895

That's it for this time. Let us know if you'd like to have similar short descriptions in the future!
