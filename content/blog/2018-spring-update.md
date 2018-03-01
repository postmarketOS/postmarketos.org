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
