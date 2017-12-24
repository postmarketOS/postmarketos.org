title: nnn days of postmarketOS
date: 2017-12-31
---

**THIS IS A ROUGH DRAFT! People are not credited properly yet, links are missing, content is missing, content is probably too long in some places (it's already an 8 minute read). The date is not final, but the blog script crashes if the date is invalid :p**


[TOC]

## Two year old devices should not be electronic waste

Most people around us have accepted, that it is necessary to **buy a new phone every other year**. As the few years of a smartphone's lifecycle pass by, it gets **[slower and slower](https://www.geekbench.com/blog/2017/12/iphone-performance-and-battery-age/)** and shiny new features become rare until it the support just completely drops. Even worse, after this period the devices don't get **[security updates](https://threatpost.com/stagefright-2-0-vulnerabilities-affect-1-billion-android-devices/114863/)** anymore (that means the bored IT student next door is able to look up on the Internet how to turn your phone into a surveillance device). Good reasons to buy a new phone after the support runs out, and you should really do that.

We want to have another option: **postmarketOS** is a Linux distribution based on (lightning fast) [Alpine](https://alpinelinux.org) that aims for a **[ten year life-cycle](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/)**. Instead of having binaries and forked source code for every device, we unify them as much as possible. That allows us to provide updates for all devices at once. The project is still in an **early stage and no, you still can't make calls with it**. But it would be a mistake to wait for that and not inform you about **all the break-throughs we have had**. Read on for the diff since day [one hundred](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos).

## Weston is not alone anymore!

<!-- TODO:
- put classic i9100 weston photo in the initial blog post again (it's missing there), add table of contents to it and link to it!
- add photos of multiple devices running plasma mobile and the other interfaces, and describe which devices are on the photos in the text
-->

### Plasma Mobile

Wayland reference compositor [Weston]() was the first interface we had running on our devices. Good enough for a demo, but to get a real tablet or smartphone experience, we always had an eye on KDE's **Plasma Mobile** project. After countless hours of hard work we are proud to finally present it running on a real devices: on the right is a photo where it runs on the Sony Xperia Z2 and [here is a video]().

* interesting tales? more photos?

### LuneOS UI
Historically LuneOS and its interface have its roots in webOS from late Palm devices. But it was rewritten from scratch to use modern technologies, such as Wayland. The UI is based on the concept of *cards* for various apps, which can be swiped away to be closed, and related cards can be grouped to *stacks*. That sounds familiar, right?

Much of the UI and default applications are actually implemented as HTML web applications, thus the name webOS. But during the porting, we have learned that it is possible to run non-HTML applications as well, such as Wayland or even [X applications](https://github.com/postmarketOS/pmbootstrap/issues/629#issuecomment-349463841).


* initial work by PureTryOut
* magmastonealex jumped in
* zhuowei's xzibit method
* NotKit ran it on a real device
* all in less than two months (!)


### Hildon
* upstream switched
* running on real devices

### XFCE 4
The classic and rock stable desktop interface that is XFCE4 was already packaged for Alpine Linux, which saved us the 

* big buttons!

### Gnome and MATE

* proof of concept


## Libre drivers and libhybris

In contrary to most Linux on smartphone projects, almost all these photos and the video are taken off devices which do not run proprietary code on the main CPU. We even have 3D video acceleration on the Xperia Z2 thanks to the Freedreno project!

The only exception is the Droid 4, which **@NotKit** owns. He is actively working on making proprietary Android drivers usable in postmarketOS with libhybris. That way devices where FLOSS drivers are missing could also make full use of their hardware. While we don't welcome binary blobs and prefer to sandbox them where we ship them at all, we embrace this solution for people who want it. But we intend to keep [closed source components entirely optional](https://github.com/postmarketOS/pmbootstrap/issues/756), so you can run pmOS as libre as you want it.

## Mainline Linux Kernel

## Devices
* we don't call them "supported" anymore (https://github.com/postmarketOS/wiki/issues/12)

### Google Glass

### New ports

### Wifi working on many devices

## Enjoyable development!

When you get started with postmarketOS development, the first thing you do is cloning the `pmbootstrap` git repository. It's a small Python script that runs on just about every Linux distribution because of its portability and only one dependency (<code>openssl</code>). With it, you will have a great deal of tasks automatized and streamlined, so you can focus on actual development instead of spending hours of setting up your development environment. We'll show you a few example commands to illustrate the new features.

### Initialization

```shell-session
$ git clone https://github.com/postmarketOS/pmbootstrap
$ cd pmbootstrap
$ ./pmbootstrap.py init
Target device (either an existing one, or a new one for porting).
Available (39): amazon-thor, asus-flo, asus-grouper, ...
Device [samsung-i9100]: 
```

The `init` action is what you run directly after cloning the source and whenever you want to change your configuration. Besides the devices we already have, it is also possible to type in a **new device name** now. It is eager to learn about your new device then: *Who produced the device? Does it have an SD card slot or a hardware keyboard? Which CPU architecture and bootloader does it have? Oh fastboot you say - why don't you give me an existing `boot.img` file from a known working Android ROM while we're at it, so we can extract the flashing offsets?*

Once this information is gathered, it presents you with an automatically generated kernel- and [device-package](https://wiki.postmarketos.org/wiki/Device_specific_package) (we get new devices running with their original kernel first, before we try to mainline them). The times of copy pasting an existing device package and adjusting everything manually are finally over.

Next up is the interface list. Just like the devices list, it is automatically generated from the package building recipes. But it also shows the package description next to the name, so you get an idea of what you're about to use.
```shell-session
Available user interfaces (5):
* none: No graphical environment
* hildon: (X11) Lightweight GTK+2 UI (optimized for single-touch touchscreens)
* luna: (Wayland) webOS UI, ported from the LuneOS project (Not working yet)
* plasma-mobile: (Wayland) Mobile variant of KDE Plasma, optimized for touchscreen
* weston: (Wayland) Reference compositor (demo, not a phone interface)
* xfce4: (X11) Lightweight GTK+2 desktop (stylus recommended)
User interface [weston]:
```

Besides that, new questions were added for the timezone (*Your host timezone is Europe/London, use that?*), username and custom default packages (*how about `vim`, `gdb`, `strace`?*). 
Build options rarely need to be changed, so they were grouped together to make it easy to skip them (ccache size is new).

```shell-session
Build options: Parallel jobs: 3, ccache per arch: 5G, timestamp based rebuilds: True
Change them? (y/n) [n]:
```

After `init` is through, you are just one command away from cross-compiling packages or building a full installation image. We have **whole new [porting](https://wiki.postmarketos.org/wiki/Porting_to_a_new_device) and [installation](https://wiki.postmarketos.org/wiki/Installation_guide) guides**, that talk you through the process step by step.

### Binary repository
In order to change something in *Android's* system code, you need to download its entire source codes of 100 GB, then do your change and build everything, which takes another 150 GB of storage, as well as 16 GB of RAM (or SWAP) and LOTS of time even on the strongest computers (numbers from [here](https://source.android.com/setup/requirements), 2017-12). Subsequent builds are faster, but still you have this initial build which seemingly takes forever.

postmarketOS doesn't use Android's build system, but devides all of its software in packages just like a regular Linux distribution. Like before we directly use Alpine's repository - but today we also have a binary repository for our own packages (with interfaces like Plasma Mobile, kernel packages etc)! While it still has a few [rough edges](https://github.com/postmarketOS/pmbootstrap/issues/970) it gets the job done: Now you **only need to compile the packages that you want to change**. Even if your computer takes hours just to build the Linux kernel it is feasible to use it for postmarketOS development. All compiler output is cached with [ccache](https://en.wikipedia.org/wiki/Ccache), so subsequent builds are a lot faster as well.

This also means, that it is possible to update your postmarketOS installation on the device now. Keep in mind that we have not reached the point yet, where each update on the device migrates properly from the previous one, so you probably have some breakage sooner or later. Kernel updates should work as well, thanks to the update script **@ata2001** wrote - but right now you need to invoke it manually.

### Continuous integration
`pmbootstrap` had test cases since the day it was released. We hooked [Travis](https://github.com/postmarketOS/pmbootstrap/pull/760) and [Coveralls](https://github.com/postmarketOS/pmbootstrap/issues/761) up with that testsuite to automatically run it for each new pull request. And we steadily increased the coverage from [51%](https://github.com/postmarketOS/pmbootstrap/pull/820#issuecomment-339057618) to [64%](https://coveralls.io/builds/14788770). The [list of shell scripts](https://github.com/postmarketOS/pmbootstrap/blob/917f03d5f9f015fa9fc0be8093d87b7f21d98d4a/test/static_code_analysis.sh#L24-L48) we automatically verify with [shellcheck](https://shellcheck.net/) has grown again.

As we learned about [kernel config options](https://wiki.postmarketos.org/wiki/Kernel_configuration) that should or should not be enabled to work properly with Linux on smartphones, we created the [`pmbootstrap kconfig_check`](https://github.com/postmarketOS/pmbootstrap/pull/589) action to automatically check the configs. This runs whenever you changed the kernel config with `pmbootstrap menuconfig`, and it runs on Travis as well.

### Refactoring
In some cases, device specific config files are needed for X11, Weston or other programs to make them work properly. Now we could always bundle these configs with the device package, regardless of the program in question being installed or not. But then again we would clutter up the filesystem with useless files, which isn't nice. Thankfully Alpine developer **@kaniini** [pointed us](https://github.com/postmarketOS/pmbootsatrap/issues/499#issuecomment-329600202) at Alpine's excellent [`install_if`](https://wiki.alpinelinux.org/wiki/APKBUILD_Reference#install_if) feature, which allows us to automatically install the config if both the program and the device package are installed. We [refactored](https://github.com/postmarketOS/pmbootsatrap/issues/499) the device packages accordingly.
```shell
weston() {
	install_if="$pkgname weston"
	install -Dm644 "$srcdir"/weston.ini \
		"$subpkgdir"/etc/xdg/weston/weston.ini
}
```

**@drebrez** made it possible to share code between the device specific package recipes with [`devicepkg-dev`](https://github.com/postmarketOS/pmbootstrap/pull/995). The package building code in `pmbootstrap` [was rewritten](https://github.com/postmarketOS/pmbootstrap/pull/935) by **@ollieparanoid** to be easier to extend and to do build-time dependency installation just like Alpine's `abuild` for improved compatibility.

**@ata2001** refactored the **Android recovery zip** installer code: After [#901](https://github.com/postmarketOS/pmbootstrap/pull/901) it has close to zero dependencies on the recovery system used, which makes it possible to work not only in TWRP, but also in CWM and probably every other Android recovery system. He also [extended it](https://github.com/postmarketOS/pmbootstrap/pull/609) to supports devices, which need the `heimdall-isorec` flash method.


* qemu: easy partition resize (@BrianOtto), 3d acceleration

* initramfs: osk-sdl integrated, debug-shell hook, initfs cached

## Other changes
* osk-sdl is default now (#476 @craftyguy)
* a little progress regarding cellular network
* encrypted swap file support (used for N900 so far) (@craftyguy)
* pmbootstrap zap: new flags (@drebrez)
* so many fixes
* ssh key
* x86 support (build pmOS on postmarket PC)

## Environment
* plasma mobile roadmap: https://vizzzion.org/blog/2017/10/plasma-mobile-roadmap/
* Alpine: 3.7 release (mention it, although we're still on "edge"), version.py
* Adelie will upstream KDE to Alpine, we can build upon that
* Librem 5 got funded
* tslib
* msm-fb-refresher from AsteroidOS
* nheko

## Raw numbers

## How can you help?
  * join the chat
  * documentation
    * apps
    * mainlining
  * print yourself a t-shirt and wear it! (add a pic here)
  * review PRs
  * improve your favorite desktop (plasma, luna, xfce4, Gnome, MATE, Asteroid OS, feature phone, ...)
  * charging-sdl
  * telephony
  * nexmon
  * bootloader reversing -> McBitter
