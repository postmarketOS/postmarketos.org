title: 100 days of postmarketOS
date: 2017-09-03
---

<!--

TODO:
- increase line-space to make it easier to read
- table of contents (automatically generated)?
- insert images
- more links
- change the formatting of the syntax highlighted code?
- link github issues
- link usernames
-->

### Sustainable approach for Linux on the phone

We are building an alternative to Android and other mobile operating systems by 
*(not forking but)* **bending the [time-proven](http://git.net/ml/linux.leaf.devel/2005-08/msg00039.html) [Alpine Linux](https://alpinelinux.org) distribution** 
to fit our purpose. Instead of using Android's build process, we build small 
software packages which can be installed with Alpine's package manager.
To achieve minimal maintenance effort, we want every device to have **only one 
unique package and share everything else**.

Although we develop at fantastic speed, at this point our OS is only 
suitable for fellow hackers who enjoy using the command-line and want to improve 
postmarketOS. **Telephony or other typical smartphone tasks are not working 
yet.** But enough of the introduction, let's take a look at our new features!

[image: weston in qemu]

### Integrated QEMU support

The idea of providing a device specific package for QEMU was introduced in July 
already with the words *"so it will be easier to try the project and/or develop 
userspace"*. Although the initial PR #56 didn't make it, the idea got picked up 
later and today we can provide you with an implementation of exactly that 
vision. **All you need to *dive right in* is to install Python (3.4+), git, QEMU and 
to run the following commands.** As usually, `pmbootstrap` does everything in 
chroots in the `install` step, so your host system does not get touched.

```shell
git clone https://github.com/postmarketOS/pmbootstrap
cd pmbootstrap
./pmbootstrap init # choose "qemu-amd64"
./pmbootstrap install
./pmbootstrap qemu
```
*Thanks to: @mmaret, @MartijnBraam, @PabloCastellano (#56, ??)*

### Early work on new user interfaces

Since postmarketOS was released, we have been using Wayland's reference 
compositor Weston as UI. But as stated in #62, it *"is a cool demo, but far 
from a usable day-to-day shell people can work with. **We need to provide a sane 
UI.**"*

[image: PureTryOut's cool gif booting up in Qemu to plasma mobile]

#### Plasma mobile (KDE's plasma desktop for phones)

Alpine Linux did not have any KDE programs or libraries packaged yet, so 
@PureTryOut went through the colossal task of packaging, looking for patches, 
compiling and debugging **more than 80 pieces of 
plasma mobile related software**. They are the very minimum to get the mobile 
version of KDE's Plasma desktop running. Alpine provided quite a few challenges 
along the way, such as the usage of the more standards compliant musl libc 
instead of the commonly used glic, but luckily @mpyne [already provided patches](https://phabricator.kde.org/D6596) in KDE's bugtracker which we were able to use.

Althought non-developers may not see it this way, this surely is a huge step 
in the direction of making plasma mobile work on postmarketOS! We're excited to 
see where this is heading, and **appreciate any help from interested developers**.
Jump right in with QEMU and the [inofficial binary packages](https://github.com/PureTryOut/pmos-plasma-mobile)!

*Thanks to: @PureTryOut, @bshah, @mpyne*

[image: Hildon in QEMU]

#### Hildon

...



[image: N900 running mainline, terminal with `uname -a` open to show the kernel version]

### Mainline kernel

One of our goals is using the mainline Linux kernel on **as many mobile devices as 
possible** (usually on Linux based smartphones, each device runs its own outdated
fork of the kernel, that can not be updated sanely to the latest version). This 
involves the huge task of rewriting the drivers to work with the current kernel 
APIs. Nevertheless, some people have been doing that since long before 
postmarketOS existed. In the case of the **Nokia N900**, their mainlining efforts 
are so advanced, that we are able to **use the mainline kernel as default** 
kernel already!

Moreover desktop Linux distributions do not only provide the kernel from the same
source code, but also use **one binary kernel package for multiple devices** (of 
the same CPU architecture). As this makes maintenance easier again, we 
follow that approach with our `linux-postmarketos` package. It 
configures the kernel to support multiple devices at once (currently the N900 
and QEMU) by supporting **kernel modules** and **multiple device trees**. On a side 
note, it is not possible for us to use Alpine's kernels right now, because it 
does not have support for smartphones configured and we wouldn't be as flexible 
as we are now (temporarily applying patches etc).

*Thanks to: @craftyguy, @MartijnBraam (#228, #159)*


### Closing words
