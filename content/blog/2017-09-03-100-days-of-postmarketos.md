title: 100 days of postmarketOS
date: 2017-09-03
---

[TOC]

## Sustainable Approach For Linux on Phones

We are building an alternative to Android and other mobile operating systems by *not* forking but **bending the [time-proven](http://git.net/ml/linux.leaf.devel/2005-08/msg00039.html) [Alpine Linux](https://alpinelinux.org) distribution** to fit our purpose. Instead of using Android's build process, we build small software packages that can be installed with Alpine's package manager. To minimize the amount of effort for maintenance, we want every device to require **only one device-specific package and share everything else**.

At this point our OS is only suitable for fellow hackers who enjoy using the command-line and want to improve postmarketOS. **Telephony or other typical smartphone tasks are not working yet.**


## Why We Evolve in Many Directions

Why don't we focus on one "flagship" device and stop making blog posts until it can be used as daily driver?

Our philosophy is that community-based FLOSS projects need to **become known during the development phase to fellow developers.** Our way of doing that is through periodically posting reports summarizing our *real progress*.

The postmarketOS community is a collective group of hackers who contribute to this project in their free time. We won't tell someone who wants to, for example, extend postmarketOS to run Doom on their smartwatch that their idea has no benefit to the project's vision. Such activities demonstrate the flexibility of postmarketOS and oftentimes leads to improvements to the project's codebase as new requirements are implemented to cover previously unforeseen use cases. In addition, these *fun* activities also increase our collective knowledge about the software and hardware we work with. But most importantly we don't want to, or plan to, take the fun away. **Because without being fun and rewarding, a free time project becomes a dead project.**

It's not all about running Doom though, there are also individuals in the project who have the most fun by [actually bringing the project towards this daily-driver vision](https://wiki.postmarketos.org/wiki/Milestones). Read on to learn about both the **incredibly beneficial efforts** as well as the **fun exercises** we have done since [the last post](https://ollieparanoid.github.io/post/50-days-of-postmarketOS/)!

## Integrated QEMU Support

The idea of providing a device specific package for QEMU was introduced back in July *"so it will be easier to try the project and/or develop userspace"*. Although the initial PR [#56](https://github.com/postmarketOS/pmbootstrap/pull/56) didn't make it, the idea got picked up again and today we can provide you with an implementation of exactly that vision. **All you need to *dive right into running postmarketOS on QEMU* is to install Python (3.4+), git, QEMU, and run the following commands.** As expected, `pmbootstrap` does everything in chroots in the `install` step, so your host operating system does not get touched.

```shell
git clone https://github.com/postmarketOS/pmbootstrap
cd pmbootstrap
./pmbootstrap init # choose "qemu-amd64"
./pmbootstrap install
./pmbootstrap qemu
```
*Thanks to: [@mmaret](https://github.com/mmaret), [@MartijnBraam](https://github.com/MartijnBraam), [@PabloCastellano](https://github.com/PabloCastellano)*


## Early Work on New User Interfaces

Since postmarketOS was released, we have been using Wayland's reference compositor Weston as a UI. However, as stated in [#62](https://github.com/postmarketOS/pmbootstrap/issues/62), it *"is a cool demo, but far from a usable day-to-day shell people can work with. **We need to provide a sane UI.**"*


[![QEMU booting up to plasma-mobile](/static/img/2017-09-03/plasma-mobile-qemu-thumb.gif){: class="fr ml3 mb3" }](/static/video/2017-09-03/plasma-mobile-qemu.webm)

### plasma-mobile (KDE's plasma desktop for phones)

Alpine Linux does not have any KDE programs or libraries packaged yet, so [@PureTryOut](https://github.com/PureTryOut) went through the colossal task of packaging, looking for patches, compiling and debugging **more than 80 pieces of plasma-mobile related software**. This is the very minimum to get the mobile version of KDE's Plasma desktop running. Alpine provided quite a few challenges along the way, such as the usage of the more standards compliant musl libc instead of the commonly used glibc. Luckily [@mpyne](https://phabricator.kde.org/p/mpyne) [already provided patches](https://phabricator.kde.org/D6596) in KDE's bugtracker that we were able to use. [@bshah](https://github.com/bhush9) not only helped us with the port, but also [mentioned postmarketOS](https://www.reddit.com/r/postmarketOS/comments/6p1avq/postmarketos_at_the_kde_akademy_2017_presented_by/) in his plasma-mobile talk at KDE's Akademy 2017!

This is definitely a huge step in the direction towards making plasma-mobile work on postmarketOS! We're excited to see where this is heading, and would **greatly appreciate any help from interested developers**. Jump right in with QEMU and the [unofficial binary packages for KDE/Plasma](https://github.com/PureTryOut/pmos-plasma-mobile)!

*Thanks to: [@bshah](https://github.com/bhush9), [@mpyne](https://phabricator.kde.org/p/mpyne), [@PureTryOut](https://github.com/PureTryOut)*


[![Hildon in postmarketOS](/static/img/2017-09-03/hildon-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/hildon.png)

### Hildon

The popular Nokia N900 originally shipped with a desktop called *Hildon*, which ran on its Debian-based [Maemo](https://maemo.org) operating system. [@NotKit](https://github.com/NotKit) started a port currently containing the minimum packages required to get working: a modified, mobile friendly, GTK+2 and 12 other packages.
A modernized GTK+3 version of Hildon is being worked on at [talk.maemo.org](https://talk.maemo.org/showthread.php?t=96800), which we could package in the future. While Hildon is based on X11 instead of Wayland, it is still a lightweight phone interface suitable for older devices.

*Thanks to: [@NotKit](https://github.com/NotKit)*


## "Of Course it Runs Doom!"

[![Doom on pmOS with freedreno](/static/img/2017-09-03/doom-xperia-z2-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/doom-xperia-z2.png)

Speaking of classic interfaces, [@Opendata26](https://github.com/Opendata26) made an obligatory Doom port. In the photo is his **[Xperia Z2 tablet](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z2_Tablet_(sony-castor-windy))** with a 4.3 kernel and the open source userspace driver **[freedreno](https://github.com/freedreno/freedreno/wiki)**. In addition to running Doom, he also enabled the driver upstream in Alpine's `mesa` package so that all Alpine users can benefit from it! Check out his [/r/postmarketOS post](https://www.reddit.com/6temny/) for more photos of other games running. Even though freedreno provides a FOSS implementation of the userspace portion of the driver, it still requires a proprietary firmware file for 3D acceleration. This test was made with X11, as it currently does not work with a Wayland compositor. Further debug will be required to determine why this is the case!


[![Doom on pmOS with freedreno](/static/img/2017-09-03/doom-lg-lenok-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/doom-lg-lenok.png)

Next up is [@Bloo](https://github.com/Bloo), who decided to port postmarketOS to his **[LG G Watch R](https://wiki.postmarketos.org/wiki/LG_G_Watch_R_(lg-lenok))**, giving us the **first smartwatch port**! In order to take out the watch and shout *"It's time to play Doom!"* whenever asked for the time, he decided to compile and run it on his device too. In the photo on the right, Doom is running in its **native resolution** of 320x240 (compare to the watch at 320x320) in Weston through XWayland. For both the Xperia Z2 and LG G Watch R, [Chocolate Doom](https://www.chocolate-doom.org/) was used and is being packaged for postmarketOS now.

*Thanks to: [@Bloo](https://github.com/Bloo), [@Opendata26](https://github.com/Opendata26)*

## Other New Devices

We have **nine** new devices in the last 50 days! In addition to the two mentioned above, we also have:

[![Nexus 7 running Weston](/static/img/2017-09-03/nexus7-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/nexus7.png)

* [Google Nexus 7 (2012) `(asus-grouper)`](https://wiki.postmarketos.org/wiki/Google_Nexus_7_2012_(asus-grouper)) *(photo on the right)*
* [HTC Desire HD `(htc-ace)`](https://wiki.postmarketos.org/wiki/HTC_Desire_HD_(htc-ace))
* [HTC Desire `(htc-bravo)`](https://wiki.postmarketos.org/wiki/HTC_Desire_(htc-bravo))
* [Mozilla Flame `(t2m-flame)`](https://wiki.postmarketos.org/wiki/Mozilla_Flame_(t2m-flame))
* [Galaxy Note II `(samsung-n7100)`](https://wiki.postmarketos.org/wiki/Galaxy_Note_II_(samsung-n7100))
* [Sony Xperia Z1 Compact `(sony-amami)`](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z1_Compact_(sony-amami))
* [Sony Xperia Z `(sony-yuga)`](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z_(sony-yuga))


*Thanks to: [@antonok](https://github.com/antonok), [@ata2001](https://github.com/ata2001), [@Bloo](https://github.com/Bloo), [@drebrez](https://github.com/drebrez), [@kskarthik](https://github.com/kskarthik), [@Victor9](https://github.com/Victor9), [@wfranken](https://github.com/wouter92), [@yuvadm](https://github.com/yuvadm) and everyone who helped them in the chat*

## Initramfs is Full of New Features

[![on screen keyboard](/static/img/2017-09-03/osk-wave-thumb.gif){: class="fr ml3 mb3" }](/static/img/2017-09-03/osk-wave.gif)

The `initramfs` is a small filesystem with an `init.sh` file that prepares the environment before it passes control to the init system running in the real root partition. For postmarketOS we use it to **find and optionally unlock the root** partition.

[@craftyguy](https://github.com/craftyguy) and [@MartijnBraam](https://github.com/MartijnBraam) have started to write a new **on-screen keyboard** named [`osk-sdl`](https://github.com/postmarketOS/osk-sdl) from scratch because we couldn't find an existing one that did not depend on heavy GUI libraries. `osk-sdl` will allow us to **unlock** the root filesystem directly with the device's touch screen or physical keyboard (if applicable). It is currently in the process of being integrated into postmarketOS, after which it will fully replace the current method of unlocking via telnet. If unlocking via telnet is a requirement for you, please reach out to us and let us know!

To work around the tight size limitations on some devices which do not support having a large `boot.img` file, [@drebrez](https://github.com/drebrez) implemented the **`initramfs-extras`** trick: a second initramfs file stores **all the big files** and is placed in the unencrypted `boot` partition. The real initramfs then detects this file by its label and extracts everything from `initramfs-extras`. At this point the `init` script works like before and has all files it needs!

Speaking of small size: the system image generated in the installation step doesn't have a fixed size anymore, it now adjusts dynamically! After flashing and booting, the initramfs will check whether the flashed image takes up all available space of the system partition and, if it does not, **automatically resizes the partition to use all available space**.

[![Splash screen rendered for the Samsung Galaxy SII](/static/img/2017-09-03/splash-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/splash.png)


Check out that cool new **splash screen** ([#206](https://github.com/postmarketOS/pmbootstrap/pull/206))! It gets built dynamically for the device's screen size whenever we build the initramfs. So it always fits perfectly! And in case you don't like it, it comes with a customizable [config](https://github.com/postmarketOS/pmbootstrap/blob/314c17e03cf8cddfd0f385d9db2f23f76f9a0418/aports/main/postmarketos-splash/config.ini)!

Last but not least we did a lot of refactoring, such as placing the `deviceinfo` file inside the initramfs for easy access to device-specific settings and adding support for a configfs-based USB network setup to help out some devices that need it.

*Thanks to: [@craftyguy](https://github.com/craftyguy), [@Defcat](https://github.com/Defcat), [@drebrez](https://github.com/drebrez), [@ollieparanoid](https://github.com/ollieparanoid), [@PabloCastellano](https://github.com/PabloCastellano), [@MartijnBraam](https://github.com/MartijnBraam)*


## Interoperability

[![Recovery zip installation in TWRP](/static/img/2017-09-03/twrp-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/twrp.png)

With all the recent device porting we have learned that there are *many* different flashing methods required for different devices. In some cases it isn't even possible to directly write to the system partition on a device but it is possible to flash a **recovery zip** through a recovery operating system, such as the popular [TWRP](http://twrp.me/). [@ata2001](https://github.com/ata2001) made it possible to create such an image with `pmbootstrap install --android-recovery-zip`. This allows flashing a device by *sideloading* this image while TWRP is running with `pmbootstrap flasher --method=adb sideload`!

Some older Samsung phones are not `fastboot` compatible, but their bootloader implements a so-called `odin`-mode. Samsung expects people to install their proprietary, Windows-only *Odin* program to be able to flash images in this mode. The protocol has been reverse engineered for some devices and can be used with the open source [heimdall](http://glassechidna.com.au/heimdall/) program, which has been wrapped with our `pmbootstrap`. But for some older phones the necessary reverse engineering work has not been done and you still have to run the proprietary program to get anything working at all. [@drebrez](https://github.com/drebrez) has implemented an **Odin-compatible export** option to help out folks in this situation: `pmbootstrap flasher export --odin`.

*Thanks to: [@ata2001](https://github.com/ata2001), [@drebrez](https://github.com/drebrez)*

## Mainline Kernel

[![N900 running mainline kernel](/static/img/2017-09-03/n900-mainline-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/n900-mainline.png)

One of our previously stated goals is using the mainline Linux kernel on **as many mobile devices as possible**. This is not as easy as it might sound, since many Linux-based smartphones (Android) require binary drivers which depend on very specific kernel versions. It's a tremendous task to rewrite these drivers to work with the current kernel APIs. Nevertheless, some people have been doing that since long before postmarketOS existed. In the case of the **Nokia N900** this has been going on for some number of years and almost all components are now supported in the mainline kernel. This has allowed us to **use the mainline kernel as the default** kernel for the N900, jumping from Maemo's `2.6.x` to mainline `4.12`!

Most desktop Linux distributions not only provide the kernel from the same source code but also use **one binary kernel package for multiple devices** for systems of the same CPU architecture. Since this makes maintenance easier, we follow that approach with our `linux-postmarketos` package. This package configures the kernel to support multiple devices at once, currently the N900 and QEMU, by supporting **kernel modules** and **multiple device trees**. On a side note, it is currently not possible for us to use Alpine's kernels because they do not have support for many components found in smartphones and we wouldn't be as flexible as we are now with temporarily applying patches.

*Thanks to: [@craftyguy](https://github.com/craftyguy), [@MartijnBraam](https://github.com/MartijnBraam) ([#228](https://github.com/postmarketOS/pmbootstrap/pull/228), [#159](https://github.com/postmarketOS/pmbootstrap/pull/159))*


## New Infrastructure

We now have several different key pieces of infrastructure in place to support ongoing project development! The first and most obvious if you are a returning reader: we have a brand new **homepage** that hosts both our main landing page, this blog, and has links to all of our online resources. You might have also seen our new **logo** which - besides looking great - is [rendered programatically](https://github.com/postmarketOS/postmarketos.org/blob/2e4be89ee8ec656620203fa825e088421afcf092/logo/__init__.py)!

Our GitHub-based **wiki** has served us well up until now, but we have outgrown it. We've since [migrated](https://gist.github.com/ollieparanoid/6ac9122e31258a7ab8498a362b249fa8) to a [proper MediaWiki server](https://wiki.postmarketos.org) with complete [public backups](https://github.com/postmarketOS/wiki). Did you know that `git` has [MediaWiki support](https://github.com/Git-Mediawiki/Git-Mediawiki/wiki) nowadays?

**Travis CI** now verifies the checksums of downloads in our package recipes and also runs `shellcheck` over more scripts across the source tree. With these changes, in combination with numerous bug fixes and requiring that nearly all changes to the `master` branch are presented as PRs for review, [`pmbootstrap`](https://github.com/postmarketOS/pmbootstrap) runs pretty stable now.

With over 100 people in the [Matrix/IRC](https://wiki.postmarketos.org/wiki/Matrix_and_IRC) channel and *lots* of messages coming in every day, we decided to create **`##postmarketOS-offtopic`** to keep the backlog in `#postmarketOS` a bit shorter.

*Thanks to: [@ata2001](https://github.com/ata2001), [@CmdrWgls](https://github.com/CmdrWgls), [@MartijnBraam](https://github.com/MartijnBraam), [@ollieparanoid](https://github.com/ollieparanoid), [@yuvadm](https://github.com/yuvadm)*

## Raw numbers
- `>`100 people in the [channel](https://wiki.postmarketos.org/wiki/Matrix_and_IRC)
- 605 [/r/postmarketOS](https://www.reddit.com/r/postmarketOS/) readers
- [pmbootstrap](https://github.com/postmarketOS/pmbootstrap)
    - 555 stargazers
    - 223 closed PRs
    - 185 closed issues
    - 75 open issues
    - 55 watchers
    - 48 forks
    - 27 contributors (`git shortlog --summary --numbered | wc -l`)

## Closing words
What you see here is only the tip of the iceberg. So much work has gone into fixing bugs, and little improvements, that it would be ridiculous to go through the effort and list them all. The community has grown so fast in such a short time and we have **people with all kinds of skills** on board, ranging from Linux experts to kernel hackers to people who [reverse engineer bootloaders](https://wiki.postmarketos.org/wiki/Mediatek) (hi [@McBitter](https://github.com/McBitter)!). We collaborate with people from other projects as well, such as [@pavelmalchek](https://github.com/pavelmalchek), who is close to using his N900 as a daily driver with his own distribution, recently [just reached out](https://github.com/postmarketOS/pmbootstrap/issues/438) to us.

So if you read through the whole post, you are probably interested in what we do. Consider contributing to the project, the **entry barrier is really low**. [`pmbootstrap`](https://github.com/postmarketOS/pmbootstrap/) automates everything for you and we are more than happy to help you through any issues you encounter in the [chat](https://wiki.postmarketos.org/wiki/Matrix_and_IRC). There are also a lot of [opportunities to help with development](https://github.com/postmarketOS/pmbootstrap/issues), so there's plenty to do. And plenty of fun to have. **Join us and tell your friends!**

## Comments
* [HackerNews](https://news.ycombinator.com/item?id=15160137)
* [Reddit](https://www.reddit.com/r/postmarketOS/duplicates/6xrvef/100_days_of_postmarketos/)
* [Twitter](https://mobile.twitter.com/postmarketOS/status/904249086366404609)
