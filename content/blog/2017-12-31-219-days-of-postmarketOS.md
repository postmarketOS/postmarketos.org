title: 219 days of postmarketOS
date: 2017-12-31
---

[TOC]

## Few Years Old Devices Should Not Be Electronic Waste

Most people around us have accepted that it is necessary to **buy a new phone every other year**. As a smartphone progresses through its own life cycle, manufacturer support for new features become rare, eventually stopping, and the device gets **[slower and slower](https://www.geekbench.com/blog/2017/12/iphone-performance-and-battery-age/)**. Even worse, after this period, the devices don't get **[security updates](https://threatpost.com/stagefright-2-0-vulnerabilities-affect-1-billion-android-devices/114863/)** anymore. This means that in many cases the bored IT student next door is able to look up on the Internet how to turn your phone into a surveillance device. Unfortunately the only way to continue to receive security updates after this point is to purchase a new device. In lieu of any alternatives today, you really should purchase a new device to stay current with security updates.

We want to have another option: **postmarketOS** is a Linux distribution based on (lightning fast) [Alpine](https://alpinelinux.org) that aims for a **[ten year life-cycle](https://postmarketos.org/blog/2017/05/26/intro/)**. Instead of having binaries and forked source code for every device, we unify them as much as possible. That allows us to provide updates for all devices at once. The project is still in an **early stage** (no, you still can't make calls with it.) But it would be a mistake to wait for phone call functionality without informing you about **all the breakthroughs we have had**. Read on for the exciting changes since day [one hundred](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos)!

## Weston Got Company

### Plasma Mobile

[![Plasma Mobile running on the sony-castor-windy with freedreno](/static/img/2017-12/plasma-castor-thumb.gif){: class="fr ml3 mb3" }](/static/video/2017-12/plasma-castor.mp4)

The Wayland reference compositor [Weston](https://en.wikipedia.org/wiki/Wayland_(display_server_protocol)#Weston) was the first interface we [had running on our devices](https://postmarketos.org/static/img/2017-05-26/i9100-filled.jpg). Good enough for a demo, but to get a **real tablet/smartphone experience** we always had an eye on KDE's [**Plasma Mobile**](https://plasma-mobile.org/) project. After countless hours of hard work we are proud to finally present it running **on real devices!**

Running plasma on real devices with postmarketOS is brand new, which means it has not been tested much and it is **far from a polished experience**. With that being said, it looks like it starts on most devices that can already run Weston but devices with hardware acceleration for graphics are much more usable at this point. The Z2 Tablet is one of the two devices booting postmarketOS and supporting hardware acceleration with the open user space driver [freedreno](https://github.com/freedreno/freedreno/wiki). All other devices must use OpenGL emulation in software due to them requiring proprietary GL drivers. We do have various ideas on improving the situation, such as [better software rendering](https://wiki.postmarketos.org/wiki/Software_OpenGL) or mainlining the devices and using FLOSS userspace drivers where possible.

The gif shows Plasma running on the [Sony Xperia Z2 Tablet](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z2_Tablet_(sony-castor-windy)) (click on it to see the full video). Below we show it on the [Google Nexus 5](https://wiki.postmarketos.org/wiki/Google_Nexus_5_(lg-hammerhead)), [Samsung Galaxy S Advance](https://wiki.postmarketos.org/wiki/Samsung_Galaxy_S_Advance_(samsung-i9070)), [Sony Xperia Z1 Compact](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z1_Compact_(sony-amami)) and again on the Z2 Tablet, but this time with [@MartijnBraam](https://github.com/MartijnBraam)'s postmarketOS wallpaper straight from our new [artwork](https://github.com/postmarketOS/artwork) repository.


[![](/static/img/2017-12/plasma-hammerhead-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/plasma-hammerhead.jpg)

[![](/static/img/2017-12/plasma-i9070-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/plasma-i9070.jpg)

[![](/static/img/2017-12/plasma-amami-3x-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/plasma-amami-3x.jpg)

[![](/static/img/2017-12/plasma-castor2-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/plasma-castor2.jpg)

<div class="cf"></div>

*Thanks to: [@ata2001](https://github.com/ata2001), [@bshah](https://github.com/bhush9), [@drebrez](https://github.com/drebrez), [@MartijnBraam](https://github.com/MartijnBraam), [@NotKit](https://github.com/NotKit), [@PureTryOut](https://github.com/PureTryOut), [@opendata26](https://github.com/opendata26), [@zhuowei](https://github.com/zhuowei)*


### LuneOS UI

[![](/static/img/2017-12/luna-qemu-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-12/luna-qemu.png)

Historically [LuneOS](https://en.wikipedia.org/wiki/LuneOS) and its interface have their roots in **webOS from late Palm devices**. It was rewritten from scratch to use modern technologies, such as Wayland. The UI is based on the concept of *cards* for various apps, which can be swiped away to close them, and related cards can be grouped to *stacks*. That sounds familiar, right?

Much of the UI and default applications are actually implemented as HTML web applications, thus the name webOS. During the porting we have learned that it is possible to run **non-HTML applications as well**, such as Wayland or even [X applications](https://github.com/postmarketOS/pmbootstrap/issues/629#issuecomment-349463841).

[@PureTryOut](https://github.com/PureTryOut) did the initial packaging while taking a short break from packaging Plasma a while back. Basic applications were packaged, but nothing ran yet. Then [@magmastonealex](https://github.com/magmastonealex) picked it up and with a **tremendous amount of work** he managed to get it going in QEMU. Afterwards [@zhuowei](https://github.com/zhuowei) got a proof of concept on his [Google Nexus 6P](https://wiki.postmarketos.org/wiki/Google_Nexus_6P) without hardware acceleration by using the [Xzibit-method](https://github.com/postmarketOS/pmbootstrap/issues/629#issuecomment-350810081) of running the LuneOS compositor inside of a running Weston compositor (this same trick [also works with plasma](https://github.com/postmarketOS/pmbootstrap/issues/987#issuecomment-350856570) by the way). [@NotKit](https://github.com/NotKit) showed us the real deal with his [Motorola Droid 4](https://github.com/postmarketOS/pmbootstrap/pull/1039) followed by [@magmastonealex](https://github.com/magmastonealex) [Teclast X80 Pro](https://wiki.postmarketos.org/wiki/Teclast_X80_Pro_(teclast-x80pro)) (third and fourth photos below, both have hardware acceleration).

Since Plasma Mobile and LuneOS share similar technologies, they have similar porting problems - and it's good for development to be able to look at problems from different angles through both UI ports. Before we continue, we should mention that **whole process** from asking *"hey how about packaging LuneOS UI"* to running it within postmarketOS on a device took **less than two months!**

[![](/static/img/2017-12/luna-lock-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/luna-lock.jpg)

[![](/static/img/2017-12/luna-firstrun-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/luna-firstrun.jpg)

[![](/static/img/2017-12/luna-droid4-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/luna-droid4.jpg)

[![](/static/img/2017-12/luna-x80pro-thumb.jpg){: class="fl mr3"}](/static/img/2017-12/luna-x80pro.jpg)

<div class="cf"></div>
*Thanks to: [@magmastonealex](https://github.com/magmastonealex), [@NotKit](https://github.com/NotKit), [@PureTryOut](https://github.com/PureTryOut), [@zhuowei](https://github.com/zhuowei)*

### Hildon, Gnome, MATE and XFCE4

[![](/static/img/2017-12/hildon-i9070-thumb.png){: class="fr ml3 mb3"}](/static/img/2017-12/hildon-i9070.png)

You see where we're heading with this: we got all of these environments running on real devices. [**Hildon**](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#hildon) was [updated](https://github.com/postmarketOS/pmbootstrap/pull/1015) by [@NotKit](https://github.com/NotKit) to use sources from [Maemo Leste](https://maemo-leste.github.io), which continues development upstream. More applications have been packaged, notably `hildon-home` which allows launching apps by touching icons.

[![](/static/img/2017-12/mate-i9070-thumb.png){: class="fr ml3 mb3 cr" }](/static/img/2017-12/mate-i9070.jpg)

The other three desktops are already maintained upstream in Alpine, which means we can just install them with little or no modifications. [@opendata26](https://github.com/opendata26) made a proof of concept running **Gnome 3** after applying a few hacks. There is a photo below with Gnome 3 on a Z2 Tablet running Firefox and watching a YouTube video. [@drebrez](https://github.com/drebrez) is [working on](https://github.com/postmarketOS/pmbootstrap/pull/1012) proper integration for **MATE** as you can see on the right.

Finally **XFCE4** was [pre-configured](https://github.com/postmarketOS/pmbootstrap/pull/695) by [@pavelmachek](https://github.com/pavelmachek). In order to make it usable on his [Nokia N900](https://wiki.postmarketos.org/wiki/Nokia_N900_(nokia-rx51)), he also [contributed](https://github.com/postmarketOS/pmbootstrap/pull/643) the `unicsy_demo` package, which reads various sensors and is able to send and receive SMS on his device after some manual preparation. [@drebrez](https://github.com/drebrez) [packaged](https://github.com/postmarketOS/pmbootstrap/pull/1001) the `matchbox-keyboard` to be used on interfaces lacking their own on screen keyboard. We can happily confirm that XFCE4 and MATE work well even ***without* hardware accelerated graphics!**


[![](/static/img/2017-12/gnome3-castor-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/gnome3-castor.jpg)


[![](/static/img/2017-12/xfce4-maguro-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/xfce4-maguro.jpg)


[![](/static/img/2017-12/xfce4-hammerhead-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/xfce4-hammerhead.jpg)

[![](/static/img/2017-12/xfce4-i9505-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/xfce4-i9505.jpg)

<div class="cf"></div>
*Thanks to: [@drebrez](https://github.com/drebrez), [@NotKit](https://github.com/NotKit), [@opendata26](https://github.com/opendata26), [@pavelmachek](https://github.com/pavelmachek)*

## Libre Drivers and Libhybris

In contrary to most Linux on smartphone projects, almost all these photos and the video are taken off devices which do not run proprietary code on the main CPU. The only exception is the Droid 4, which [@NotKit](https://github.com/NotKit) owns. He is [actively working](https://github.com/postmarketOS/pmbootstrap/pull/1002) on making proprietary Android drivers usable in postmarketOS with [**libhybris**](https://en.wikipedia.org/wiki/Hybris_(software)). Libhybris allows devices lacking FLOSS drivers to make full use of their hardware.

While we don't welcome binary blobs and prefer to sandbox them where we ship them at all, we embrace this solution for people who want it. However we intend to keep [closed source components entirely optional](https://github.com/postmarketOS/pmbootstrap/issues/756), so you can run pmOS as libre as you want it.

*Thanks to: [@NotKit](https://github.com/NotKit)*

## Mainline Linux Kernel
### Android Based Devices
[![](/static/img/2017-12/mainline-i9305-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-12/mainline-i9305.jpg)


It's always a super exciting time for [#postmarketOS](https://wiki.postmarketos.org/wiki/Matrix_and_IRC) when someone posts the **first photo** of their smartphone **running on a mainline kernel**, oftentimes with a distorted screen. Enjoy such pictures of the [Google Nexus 5](https://wiki.postmarketos.org/wiki/Google_Nexus_5_(lg-hammerhead)) ([@bshah](https://github.com/bhush9)) and [Fairphone 2](https://wiki.postmarketos.org/wiki/Fairphone-2) ([@z3ntu](https://github.com/z3ntu)) below. The [Sony Xperia Z1 Compact](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z1_Compact_(sony-amami)) ([@ata2001](https://github.com/ata2001)) boots a mainline kernel as well, however the screen does not work yet.

Together with the [Google Nexus 7 (2013)](https://wiki.postmarketos.org/wiki/Google_Nexus_7_2013_(asus-flo)), [Teclast X80 Pro](https://wiki.postmarketos.org/wiki/Teclast_X80_Pro_(teclast-x80pro)) and the [Xperia Z2 Tablet](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z2_Tablet_(sony-castor-windy)) &mdash; where [@opendata26](https://github.com/opendata26) fixed a mmc regression introduced with newer kernels &mdash; we now have **six Android-based devices packaged with partial mainline support**. We are still at the beginning of unifying them into one `linux-postmarketos-stable` package, but it's a huge step in the right direction!

While this blog post was in the making, [@fourkbomb](https://github.com/fourkbomb) showed us **even more mainlining progress**. This work is *not* packaged for postmarketOS yet, and he used **[`kexec`](https://forkwhiletrue.me/posts/kexec-on-galaxy-s3/)** to boot from the original kernel forks to the mainline kernel. Nevertheless, the results are impressive! On the right is the [Samsung Galaxy SIII LTE](https://wiki.postmarketos.org/wiki/Samsung_Galaxy_SIII_LTE_(samsung-i9305)) (`i9305`) running mainline (as you can see in the terminal when clicking on it). As if that wasn't cool enough he made it work on similar Samsungs ([`i9300`](/static/img/2017-12/mainline-i9300.jpg), [`n7100`](/static/img/2017-12/mainline-n7100.jpg), [`n7105`](/static/img/2017-12/mainline-n7105.jpg)) as well!

[![](/static/img/2017-12/mainline-hammerhead-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/mainline-hammerhead.jpg)

[![](/static/img/2017-12/mainline-fp2-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/mainline-fp2.jpg)

<div class="cf"></div>
*Thanks to: [@ata2001](https://github.com/ata2001), [@bshah](https://github.com/bhush9),
[@fourkbomb](https://github.com/fourkbomb), [@magmastonealex](https://github.com/magmastonealex), [@montvid](https://github.com/montvid), [@opendata26](https://github.com/opendata26), [@z3ntu](https://github.com/z3ntu)*

### Nokia N9xx Devices
[![](/static/img/2017-12/mainline-rm-969-thumb.jpg){: class="fr ml3 mb3" }](/static/img/2017-12/mainline-rm-969.jpg)

[Camera support](https://www.youtube.com/watch?v=fH6zuK2OOVU) for the **[N900](https://wiki.postmarketos.org/wiki/Nokia_N900_(nokia-rx51))** was merged by [@pavelmachek](https://github.com/pavelmachek). There's still a lot of work to do in kernel and user space, but the classic N900's hardware support is getting better. The only major areas not supported are Bluetooth and 3D acceleration.

**[Nokia N9](https://wiki.postmarketos.org/wiki/Nokia_N9)** packaging for postmarketOS with the mainline kernel is [ongoing](https://github.com/postmarketOS/pmbootstrap/pull/1046) now that [@filippz](https://github.com/filippz) [made it work](https://mobile.twitter.com/fi1ippz/status/945692340194349056) (photo on the right shows the N9 during [earlier porting stages](https://mobile.twitter.com/fi1ippz/status/927581300197863427)). [@sre](https://github.com/sre) has done a lot of work on display support for TI OMAP, and this work is slowly being merged into the mainline kernel. Support for battery status on N9 and [N950](https://en.wikipedia.org/wiki/N950) should be ready in kernel v4.15. In addition, light sensor drivers are now working. While this is amazing progress, a lot more work still needs to be done for these devices. For instance battery charging, a staple feature for smartphones, is currently not working yet.

*Thanks to: [@filippz](https://github.com/filippz), [@pavelmachek](https://github.com/pavelmachek), [@sre](https://github.com/sre)*

## New Devices
Despite not being a smartphone or tablet, this next device is still right at home in this section: [@dee-gomma](https://github.com/dee-gomma) managed to run and demonstrate basic functionality of `pmbootstrap` on a 32 bit "postmarket PC", check out [his instructions](https://github.com/postmarketOS/pmbootstrap/issues/933) if you still own such an old computer and feel adventurous.

[![](/static/img/2017-12/new-s6500d-thumb.png){: class="fr ml3 mb3"}](/static/img/2017-12/new-s6500d.jpg)

But what you are really looking for are the new supported devices running postmarketOS, right? Most people expect a certain level of functionality on *supported* devices, and almost all expect that a supported device can be used as daily driver. As a result, this section has historically started off with a disclaimer that our definition of "supported" essentially means that the devices will successfully boot postmarketOS. This time, however, we have decided to [abandon the term "supported" altogether](https://github.com/postmarketOS/wiki/issues/12) in order to help minimize confusion. Here are **twenty-five new devices**, on which **postmarketOS boots**. Click on them for detailed information about what works and what does not.

* [Amazon Kindle Fire HDX `(amazon-thor)`]( https://wiki.postmarketos.org/wiki/Amazon_Kindle_Fire_HDX) *(first below)*
* [Fairphone 2 `(fairphone-fp2)`](https://wiki.postmarketos.org/wiki/Fairphone_2_(fairphone-fp2))
* [Google Glass (Explorer Edition) `(google-glass)`](https://wiki.postmarketos.org/wiki/Google_Glass_(Explorer_Edition)) *(second below, [more pictures](https://github.com/postmarketOS/pmbootstrap/pull/957#issuecomment-348735547))*
* [Google Nexus 6P `(huawei-angler)`](https://wiki.postmarketos.org/wiki/Google_Nexus_6P)
* [Google Nexus 7 (2013) `(asus-flo)`](https://wiki.postmarketos.org/wiki/Google_Nexus_7_2013_(asus-flo))
* [Huawei Ascend Y530 `(huawei-y530)`](https://wiki.postmarketos.org/wiki/Huawei-Ascend-Y530)
* [Lenovo K6 Power `(lenovo-karate)`](https://wiki.postmarketos.org/wiki/Lenovo_K6_Power_(lenovo-karate))
* [LG G Watch `(lg-dory)`](https://wiki.postmarketos.org/wiki/LG_G_Watch_(lg-dory)) *(third below)*
* [LG G4 International `(lg-h815)`](https://wiki.postmarketos.org/wiki/LG_G4_International_(lg-h815))
* [LG L65 Dual SIM D285 `(lg-d285)`](https://wiki.postmarketos.org/wiki/LG_L65_Dual_SIM_D285_(lg-d285))
* [Moto G 2015 `(motorola-osprey)`](https://wiki.postmarketos.org/wiki/Moto_G_2015_(motorola-osprey))
* [OnePlus One `(oneplus-bacon)`](https://wiki.postmarketos.org/wiki/OnePlus_One_(oneplus-bacon))
* [OnePlus X `(oneplus-onyx)`](https://wiki.postmarketos.org/wiki/OnePlus_X_(oneplus-onyx))
* [Ouya `(ouya-ouya)`](https://wiki.postmarketos.org/wiki/Ouya_(ouya-ouya))
* [Samsung Galaxy Mini 2 `(samsung-s6500d)`](https://wiki.postmarketos.org/wiki/Samsung_Galaxy_Mini_2_(samsung-s6500d)) *(on the right)*
* [Samsung Galaxy SIII (i747m) `(samsung-i747m)`](https://wiki.postmarketos.org/wiki/Samsung-i747m)
* [Samsung Galaxy SIII (LTE) `(samsung-i9305)`](https://wiki.postmarketos.org/wiki/Samsung_Galaxy_SIII_LTE_(samsung-i9305))
* [Samsung Galaxy S4 (International) `(samsung-i9505)`](https://wiki.postmarketos.org/wiki/Samsung-i9505-(Samsung-Galaxy-S4-int))
* [Samsung Galaxy SL `(samsung-i9003)`](https://wiki.postmarketos.org/wiki/Samsung_Galaxy_SL_(samsung-i9003))
* [Samsung Galaxy Tab 2 10.1" `(samsung-espresso10)`](https://wiki.postmarketos.org/wiki/Samsung_Galaxy_Tab_2_10.1%22_(3G_and_Wifi)_(samsung-espresso10))
* [Sony Xperia Z1 `(sony-honami)`](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z1_(sony-honami)) *(fourth below)*
* [Sony Xperia Z3 Compact `(sony-aries)`](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z3C_(sony-aries))
* [Teclast X80 Pro `(teclast-x80pro)`](https://wiki.postmarketos.org/wiki/Teclast_X80_Pro_(teclast-x80pro))
* [Wiko Lenny 3 `(wiko-lenny3)`](https://wiki.postmarketos.org/wiki/Wiko_Lenny_3_(wiko-lenny3))
* [Xiaomi RedMi3 `(xiaomi-ido)`](https://wiki.postmarketos.org/wiki/Xiaomi_RedMi3_(xiaomi-ido))

The best way to get an overview of all devices at once is the [devices](https://wiki.postmarketos.org/wiki/Devices) page on the wiki. As of today, for example, it shows that we have **18 devices with working [Wi-Fi](https://wiki.postmarketos.org/wiki/Wifi)**.


[![](/static/img/2017-12/new-thor-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/new-thor.jpg)

[![](/static/img/2017-12/new-glass-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/new-glass.jpg)

[![](/static/img/2017-12/new-dory-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/new-dory.jpg)

[![](/static/img/2017-12/new-honami-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/new-honami.jpg)



<div class="cf"></div>
*Thanks to: [@ata2001](https://github.com/ata2001) [@dakk](https://github.com/dakk) [@dee-gomma](https://github.com/dee-gomma) [@drebrez](https://github.com/drebrez) [@flacks](https://github.com/flacks) [@Halamix2](https://github.com/Halamix2) [@kaendfinger](https://github.com/kaendfinger) [@kamnxt](https://github.com/kamnxt) [@kskarthik](https://github.com/kskarthik) [@lawl](https://github.com/lawl) [@limiter121](https://github.com/limiter121) [@magmastonealex](https://github.com/magmastonealex) [@montvid](https://github.com/montvid) [@MoreRobustThanYou](https://github.com/MoreRobustThanYou) [@rendeko](https://github.com/rendeko) [@rrooij](https://github.com/rrooij) [@shwsh](https://github.com/shwsh) [@tyxieblub](https://github.com/tyxieblub) [@WilliamO7](https://github.com/WilliamO7) [@z3ntu](https://github.com/z3ntu) [@zhenyolka](https://github.com/zhenyolka) [@zhuowei](https://github.com/zhuowei) and everyone who helped them out!*

## All New 'pmbootstrap init'

When you get started with postmarketOS development, the first thing you do is clone the **`pmbootstrap`** git repository. This provides you with a small Python script that runs on just about **every Linux distribution** because of Python's portability and the script's single dependency on <code>openssl</code>. With it, you will have a great deal of **tasks automated and streamlined**, so you can **focus on actual development** instead of spending hours on setting up your development environment.

```shell-session
$ git clone https://github.com/postmarketOS/pmbootstrap
$ cd pmbootstrap
$ ./pmbootstrap.py init
Target device (either an existing one, or a new one for porting).
Available (39): amazon-thor, asus-flo, asus-grouper, ...
Device [samsung-i9100]: 
```

The `init` action is what you run directly after cloning the source and whenever you want to change your configuration. Besides the devices we already have, it is also possible to type in a **new device name** now. In the "new device name" mode the script is eager to learn about your new device: *Who produced the device? Does it have an SD card slot or a hardware keyboard? Which CPU architecture and bootloader does it have? Oh fastboot you say - why don't you give me an existing **`boot.img`** file from a known working Android ROM while we're at it, so we can **extract the flashing offsets**?*

Once this information is gathered, it presents you with an **automatically generated kernel-package and [device-package](https://wiki.postmarketos.org/wiki/Device_specific_package)**. We get new devices running with their original kernel first, before we try to run the mainline kernel on them. Besides that, new questions were added for the interface: timezone (e.g. *Your host timezone is Europe/London, use that?*), username and **custom default packages** (e.g. *how about `vim`, `gdb`, `strace`?*).
[![https://wiki.postmarketos.org/wiki/Porting_to_a_new_device](/static/img/2017-12/porting-guide-thumb.png){: class="fr mt3 ml3" style="width:320px"}](https://wiki.postmarketos.org/wiki/Porting_to_a_new_device) Build options rarely need to be changed, so they were grouped together to make it easy to skip them.

After `init` is through, you are just **one command away from cross-compiling** packages or building a **full installation image**. We have whole new [porting](https://wiki.postmarketos.org/wiki/Porting_to_a_new_device) and [installation](https://wiki.postmarketos.org/wiki/Installation_guide) guides that walk you through the process step by step.

*Thanks to: [@craftyguy](https://github.com/craftyguy), [@drebrez](https://github.com/drebrez), [@ollieparanoid](https://github.com/ollieparanoid)*

## Binary Repository
In order to change something in ***Android's* system code**, you need to **download its entire source** code of 100 GB, then do your change and **build everything**, which takes another 150 GB of storage, as well as 16 GB of RAM (or SWAP) and **lots of time** even on the strongest computers (numbers from [here](https://source.android.com/setup/requirements), 2017-12). Subsequent builds are faster, but still you have this initial build which seemingly takes forever.

postmarketOS doesn't use Android's build system, but divides all of its software in **packages** just like a regular Linux distribution. As mentioned previously we directly use Alpine's repository for many packages in postmarketOS - but today we also have a binary repository for our own packages (with interfaces like Plasma Mobile, kernel packages, etc)! While it still has a few [rough edges](https://github.com/postmarketOS/pmbootstrap/issues/970) it gets the job done: Now you **only need to compile the packages that you want to change**. Even if your computer takes hours just to build the Linux kernel it is still feasible to use it for postmarketOS development. All compiler output is cached with [ccache](https://en.wikipedia.org/wiki/Ccache), so subsequent builds are a lot faster as well.

[![](/static/img/2017-12/logo-render.png){: class="fl mr3 mb3 mt3"}](https://github.com/postmarketOS/artwork/commit/805d8762426e69c2b1761e9bb2b0993509043c24)

This also means that it is possible to update your postmarketOS installation running on your device now. Keep in mind that we have not reached the point yet where we can verify each update on the device migrates properly from the previous one version, so you will probably have some breakage sooner or later. Kernel updates should work as well, thanks to the **kernel update script** [@ata2001](https://github.com/ata2001) wrote - but right now you will need to invoke it manually.

*Thanks to: [@ata2001](https://github.com/ata2001),  [@ollieparanoid](https://github.com/ollieparanoid)*

## Continuous Integration
`pmbootstrap` has had test cases since the day it was released. We hooked [Travis](https://github.com/postmarketOS/pmbootstrap/pull/760) and [Coveralls](https://github.com/postmarketOS/pmbootstrap/issues/761) up with that testsuite to automatically run it for each new pull request. And we steadily increased the coverage from [51%](https://github.com/postmarketOS/pmbootstrap/pull/820#issuecomment-339057618) to [64%](https://coveralls.io/builds/14788770). The [list of shell scripts](https://github.com/postmarketOS/pmbootstrap/blob/917f03d5f9f015fa9fc0be8093d87b7f21d98d4a/test/static_code_analysis.sh#L24-L48) we automatically verify with [shellcheck](https://shellcheck.net/) has grown again.

As we learned about [kernel config options](https://wiki.postmarketos.org/wiki/Kernel_configuration) that should or should not be enabled to work properly with Linux on smartphones, we created the [`pmbootstrap kconfig_check`](https://github.com/postmarketOS/pmbootstrap/pull/589) action to automatically check the configs. This runs whenever you change the kernel config with `pmbootstrap menuconfig`, and it runs on Travis as well.

<div class="cl"></div>
*Thanks to: [@ata2001](https://github.com/ata2001), [@drebrez](https://github.com/drebrez), [@MartijnBraam](https://github.com/MartijnBraam), [@ollieparanoid](https://github.com/ollieparanoid)*


## Other New Features

Running postmarketOS in a **QEMU VM**, with `pmbootstrap qemu`, will now use **3D acceleration** by default. In addition, QEMU image files can now be **resized on the fly** by using the new `--image-size` parameter. These changes continue to make QEMU an invaluable resource for developers packaging and testing new software in the postmarketOS/Alpine Linux environment.

Regarding encryption, it is possible to use [**encrypted swap files**](https://github.com/postmarketOS/pmbootstrap/pull/585) now. Furthermore the **touch screen keyboard for full disk encryption** ([osk-sdl](https://github.com/postmarketOS/osk-sdl)) we [introduced last time](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#initramfs-is-full-of-new-features) became the [default](https://www.reddit.com/r/postmarketOS/comments/76flrr/fde_unlocking_with_osksdl_has_been_merged/) now, and has helped to make full disk encryption a great deal more practical. You just don't need to fire up a [USB telnet session](https://ollieparanoid.github.io/img/2017-05-26/i9100/telnet.jpg) anymore to unlock your phone each time you reboot it. But for initramfs debug, you can still install a hook that gives you a **debug shell** - and it displays a nice splash screen until you tell it to continue booting.

[![](/static/img/2017-12/debug-shell-i9070-thumb.jpg){: class="fl mr3 mb3"}](/static/img/2017-12/debug-shell-i9070.jpg)

<div class="cl"></div>
*Thanks to: [@BrianOtto](https://github.com/BrianOtto), [@craftyguy](https://github.com/craftyguy), [@drebrez](https://github.com/drebrez)*

## Various Refactoring
[@drebrez](https://github.com/drebrez) made it possible to share code between the device specific package recipes with [`devicepkg-dev`](https://github.com/postmarketOS/pmbootstrap/pull/995). The package building code in `pmbootstrap` [was rewritten](https://github.com/postmarketOS/pmbootstrap/pull/935) by [@ollieparanoid](https://github.com/ollieparanoid) to make it easier to extend and to do build-time dependency installation just like Alpine's `abuild` for improved compatibility.

[@ata2001](https://github.com/ata2001) [refactored](https://github.com/postmarketOS/pmbootstrap/pull/901) the **Android recovery zip** installer to have close to zero dependencies on the recovery system used, which makes it possible to work not only in (exotic versions of) TWRP, but also in CWM and probably every other Android recovery system. He also [extended it](https://github.com/postmarketOS/pmbootstrap/pull/609) to support devices that need the `heimdall-isorec` flash method.

*Thanks to: [@ata2001](https://github.com/ata2001), [@drebrez](https://github.com/drebrez), [@ollieparanoid](https://github.com/ollieparanoid)*

## Raw Numbers
- `>`275 people in the [channel](https://wiki.postmarketos.org/wiki/Matrix_and_IRC) (+175)
- 1367 [/r/postmarketOS](https://www.reddit.com/r/postmarketOS/) readers (+762)
- [pmbootstrap](https://github.com/postmarketOS/pmbootstrap)
    - 763 stargazers *(+208)*
    - 567 closed PRs *(+344)*
    - 336 closed issues *(+151)*
    - 134 open issues *(+59)*
    - 102 forks *(+54)*
    - 74 watchers *(+25)*
    - 57 contributors (`git shortlog --summary --numbered | wc -l`) *(+30)*


## Environment
We would like to thank all projects that collaborate with us, and talk about some of their news which is relevant for us as well.

**Alpine Linux 3.7** [was released](https://alpinelinux.org/posts/Alpine-3.7.0-released.html) with thousands of git commits of hard work. While postmarketOS is still based on their rolling release `edge` branch, the idea is that we also base our work on the stable channels at some point in the future. [@awilfox](https://github.com/awilfox) from the upcoming [Adélie Linux](https://adelielinux.org/) assured that they will be **upstreaming and maintaining the LTS version of KDE Plasma** in Alpine. As soon as it's upstreamed we can base our Plasma Mobile packaging directly on the KDE Framework in Alpine, and when Plasma Mobile works with the LTS version of the Plasma Framework at some point in the future we can **build on top of that** as well! Several contributors to postmarketOS have also directly contributed to the Alpine Linux 3.7 release and, while not nearly as impactful as the official Alpine Linux developers, we are still very much committed to helping out our Alpine friends where ever we can!

The **Plasma Mobile** team recently detailed their [roadmap](https://vizzzion.org/blog/2017/10/plasma-mobile-roadmap/) in a recent blog post. And they got a lot of interest with the successfully funded **[Librem 5 phone](https://puri.sm/shop/librem-5/)**, which will either use [Plasma](https://www.kde.org/announcements/kde-purism-librem5.php) or [Gnome 3](https://www.gnome.org/news/2017/09/gnome-foundation-partners-with-purism-to-support-its-efforts-to-build-the-librem-5-smartphone/). We think the [Librem 5 is great for all Linux smartphone projects](https://postmarketos.org/blog/2017/09/24/librem-5/) out there.

The [somewhat mobile friendly](https://matrix.org/blog/2017/09/28/experiments-with-matrix-on-the-purism-librem5-starring-ubports-and-nheko/) matrix client **[nheko](https://github.com/mujx/nheko)** just had its [0.1.0 release](https://github.com/mujx/nheko/releases/tag/v0.1.0), and while we have [not finished packaging](https://github.com/postmarketOS/pmbootstrap/issues/900) it yet, author [@mujx](https://github.com/mujx) confirmed that he had an earlier version working on postmarketOS in QEMU.

[![](/static/img/2017-12/logo-tslib-thumb.png){: class="fr ml3 mb3" }](https://github.com/kergoth/tslib/issues/89#issuecomment-343443468)

**[tslib](http://www.tslib.org/)** powers the touch screen functionality in our initramfs. Shout out to [@merge](https://github.com/merge) from the project, who was incredibly helpful with [answering questions](https://github.com/kergoth/tslib/issues/103), **[making it work on Android devices](https://github.com/kergoth/tslib/issues/104)** and by patching tslib, the touch driver for the N900 in [the kernel](https://github.com/kergoth/tslib/issues/108#issuecomment-342887195), and even implementing [automatic touch screen detection](https://github.com/kergoth/tslib/issues/108)! To show our appreciation we solicited help for responding to a tslib request for a [vectorized logo](https://github.com/kergoth/tslib/issues/89) in #postmarketOS, and only a day later [@rrcha](https://github.com/rrcha) took care of it.

If you're into smartwatches and want to use an open source OS on them today, check out **[AsteroidOS](https://asteroidos.org/)**. [@FlorianRevest](https://github.com/FlorentRevest) [tagged a version](https://github.com/AsteroidOS/msm-fb-refresher/issues/1) of its `msm-fb-refresher` component, so were able to package it properly to **refresh the framebuffer** in postmarketOS for devices that need it.

*Thanks to everyone working on these projects!*

## How Can You Help?

[![](/static/img/2017-12/logo-shirt-thumb.jpg){: class="fr ml3 mb3" }](/static/img/2017-12/logo-shirt.jpg)

You read through the entire thing, didn't you? Looks like you have some interest in this project - and **we can use every helping hand.** We've put the more technical tasks at the bottom of each list. `pmbootstrap` is written in Python, packaging tasks require shell scripting knowledge. 

Tasks that **do not require** a device running postmarketOS:

* [Improve documentation](http://wiki.postmarketos.org/) (e.g. [potential apps](https://wiki.postmarketos.org/wiki/Potential_apps), [mainlining](https://wiki.postmarketos.org/wiki/The_Mainline_Kernel))
* [Donate](https://wiki.postmarketos.org/wiki/Donate)
* [Print yourself a postmarketOS fair trade t-shirt and wear it!](https://github.com/postmarketOS/artwork/pull/9)
* [Test pull requests](https://github.com/postmarketOS/pmbootstrap/pulls)
* [Review pull requests](https://github.com/postmarketOS/pmbootstrap/pulls)
* [Resolve open issues](https://github.com/postmarketOS/pmbootstrap/issues)
* Package and maintain apps (e.g. [nheko](https://github.com/postmarketOS/pmbootstrap/issues/900))
* Improve or package [your favorite user interface](https://github.com/postmarketOS/pmbootstrap/issues/62) (e.g. Asteroid OS, feature phone, Gnome, Hildon, Lune OS, MATE, Plasma, Ubuntu Touch, Weston, XFCE4)
* [Package `anbox` to run Android apps](https://www.reddit.com/r/postmarketOS/comments/6xuo1s/will_postmarketos_support_anbox/)
* [Package nexmon](https://github.com/postmarketOS/pmbootstrap/issues/592), so we can patch [security holes](https://ollieparanoid.github.io/post/security-warning/) in abandoned Wifi firmware
* [Improve Software OpenGL rendering](https://wiki.postmarketos.org/wiki/Software_OpenGL)

Tasks that **do require** a mobile device for development:

* [Port your phone](https://wiki.postmarketos.org/wiki/Porting_to_a_new_device) (or [install pmOS](https://wiki.postmarketos.org/wiki/Installation_guide) on it if there's already a port)
* Make [good photos/videos](https://wiki.postmarketos.org/wiki/Making_good_photos) of devices running pmOS for the [wiki](https://wiki.postmarketos.org/wiki/Special:ListFiles) and [/r/postmarketOS](https://www.reddit.com/r/postmarketOS/)
* [Test pull requests on devices](https://github.com/postmarketOS/pmbootstrap/pulls)
* [Get cellular modems working](https://github.com/postmarketOS/pmbootstrap/issues/598)
* [Work on the charging UI](https://github.com/postmarketOS/charging-sdl) for the initramfs (C++, started by [@IanS5](https://github.com/IanS5) and [@pavelmachek](pavelmachek))
* Help out [@McBitter](https://github.com/McBitter) with [Mediatek bootloader reverse engineering](https://wiki.postmarketos.org/wiki/Mediatek)

## Closing Words

What a crazy half year of development we have behind us. Who would have thought that this project would have taken off *this much*? That such a big community would have emerged out of nowhere? This is the **work of every single contributor**, we can all be proud of what we have achieved and we have *lots* of potential for the future. Thanks for reading, and now **go party hard on new years eve!**


## Bonus: `install_if`
*No fancy pictures here, just a little code snippet and possibly boring implementation details. We've moved this one to the bottom because the post has gotten really long again.*

In some cases, **device specific config files** are needed **for programs**, such as X11 or Weston. Now we could always bundle these configs with the device package, regardless of the program in question being installed or not. But then again we would **clutter up the filesystem** with useless files, which isn't nice. Thankfully Alpine developer [@kaniini](https://github.com/kaniini) [pointed us](https://github.com/postmarketOS/pmbootsatrap/issues/499#issuecomment-329600202) at Alpine's excellent **[`install_if`](https://wiki.alpinelinux.org/wiki/APKBUILD_Reference#install_if)** feature, which allows us to automatically install the config *if* both the program and the device package are installed. We [refactored](https://github.com/postmarketOS/pmbootstrap/issues/499) the device packages accordingly.
```shell
weston() {
	install_if="$pkgname weston"
	install -Dm644 "$srcdir"/weston.ini \
		"$subpkgdir"/etc/xdg/weston/weston.ini
}
```

*Thanks to: [@craftyguy](https://github.com/craftyguy), [@kaniini](https://github.com/kaniini), [@MartijnBraam](https://github.com/MartijnBraam), [@ollieparanoid](https://github.com/ollieparanoid), [@PureTryOut](https://github.com/PureTryOut), [@Wouter92](https://github.com/Wouter92)*
