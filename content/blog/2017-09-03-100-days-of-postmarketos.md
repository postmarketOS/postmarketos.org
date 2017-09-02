title: 100 days of postmarketOS
date: 2017-09-03
---

[TOC]

## Sustainable approach for Linux on the phone

We are building an alternative to Android and other mobile operating systems by *(not forking but)* **bending the [time-proven](http://git.net/ml/linux.leaf.devel/2005-08/msg00039.html) [Alpine Linux](https://alpinelinux.org) distribution** to fit our purpose. Instead of using Android's build process, we build small software packages which can be installed with Alpine's package manager. To achieve minimal maintenance effort, we want every device to have **only one unique package and share everything else**.

At this point our OS is only suitable for fellow hackers who enjoy using the command-line and want to improve postmarketOS. **Telephony or other typical smartphone tasks are not working yet.**


## Why we evolve in many directions

So why don't we focus on one "flagship" device and stop making blog posts until it can be used as daily driver?

Community based FLOSS projects need to **become known in the development phase to fellow developers.** Our way to do that is through posting reports summarizing our *real progress* every now and then.

Furthermore, the postmarketOS community is not a company where everybody gets paid to work in the same direction. We are a collective of hackers who make this project in their free time. We won't tell someone who wants to extend postmarketOS to run Doom on his smartwatch that his idea has no benefit the projects vision. Because even though it may not be part of most peoples vision, it shows what can be done with our project, and all contributions will improve the codebase, as it gets improved to work with many different use-cases we have not thought about before. Doing such *fun* stuff also increases knowledge about the software and hardware we work with. But most importantly we don't take the fun away. **Because without fun, a free time project becomes a dead project.**

With that being said, there are also individuals in the project, to whom the most fun is to [actually bring the project towards the daily-driver vision](https://wiki.postmarketos.org/wiki/Milestones). So read on to learn about both **incredibly beneficial efforts**, as well as **fun exercises** we have done since [the last post](https://ollieparanoid.github.io/post/50-days-of-postmarketOS/).

## Integrated QEMU support

The idea of providing a device specific package for QEMU was introduced in July already with the words *"so it will be easier to try the project and/or develop userspace"*. Although the initial PR #56 didn't make it, the idea got picked up later and today we can provide you with an implementation of exactly that vision. **All you need to *dive right in* is to install Python (3.4+), git, QEMU and to run the following commands.** As usually, `pmbootstrap` does everything in chroots in the `install` step, so your host system does not get touched.

```shell
git clone https://github.com/postmarketOS/pmbootstrap
cd pmbootstrap
./pmbootstrap init # choose "qemu-amd64"
./pmbootstrap install
./pmbootstrap qemu
```
*Thanks to: @mmaret, @MartijnBraam, @PabloCastellano*


## Early work on new user interfaces

Since postmarketOS was released, we have been using Wayland's reference compositor Weston as UI. But as stated in [#62](https://github.com/postmarketOS/pmbootstrap/issues/62), it *"is a cool demo, but far from a usable day-to-day shell people can work with. **We need to provide a sane UI.**"*


[![QEMU booting up to plasma-mobile](/static/img/2017-09-03/plasma-mobile-qemu-thumb.gif){: class="fr ml3 mb3" }](/static/video/2017-09-03/plasma-mobile-qemu.webm)

### plasma-mobile (KDE's plasma desktop for phones)

Alpine Linux did not have any KDE programs or libraries packaged yet, so @PureTryOut went through the colossal task of packaging, looking for patches, compiling and debugging **more than 80 pieces of plasma-mobile related software**. They are the very minimum to get the mobile version of KDE's Plasma desktop running. Alpine provided quite a few challenges along the way, such as the usage of the more standards compliant musl libc instead of the commonly used glibc, but luckily @mpyne [already provided patches](https://phabricator.kde.org/D6596) in KDE's bugtracker which we were able to use. @bshah not only helped us with the port, but also [mentioned postmarketOS](https://www.reddit.com/r/postmarketOS/comments/6p1avq/postmarketos_at_the_kde_akademy_2017_presented_by/) in his plasma-mobile talk at KDE's Akademy 2017!

Althought non-developers may not see it this way, this surely is a huge step in the direction of making plasma-mobile work on postmarketOS! We're excited to see where this is heading, and **appreciate any help from interested developers**. Jump right in with QEMU and the [inofficial binary packages](https://github.com/PureTryOut/pmos-plasma-mobile)!

*Thanks to: @bshah, @mpyne, @PureTryOut*


[![Hildon in postmarketOS](/static/img/2017-09-03/hildon-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/hildon.png)

### Hildon

The popular N900 had a desktop called *Hildon* running on it's Debian based [Maemo](https://maemo.org) operating system. @NotKit started a port, which also contains only the minimal packages to get it working at all. It only consists of a modified GTK+2 (to make GTK+2 windows mobile friendly) and 12 other packages.
A modernized GTK+3 version of Hildon is being worked on at [talk.maemo.org](https://talk.maemo.org/showthread.php?t=96800), which we could package in the future. While Hildon is based on X11 instead of Wayland, it is still a lightweight phone interface suitable for older devices.

*Thanks to: @NotKit*


[![Doom on pmOS with freedreno](/static/img/2017-09-03/doom-xperia-z2-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/doom-xperia-z2.png)

## "Of course it runs Doom!"

Speaking of classic interfaces, @Opendata26 made the obligatory Doom port. On the photo is his **[Xperia Z2 tablet](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z2_Tablet_(sony-castor-windy))** with a 4.3 kernel and the open source userspace driver **[freedreno](https://github.com/freedreno/freedreno/wiki)**. Furthermore he enabled that driver upstream in Alpine's `mesa` package, so everyone can use it. Check out his [/r/postmarketOS post](https://www.reddit.com/6temny/) for more photos of other games running. Please note, that freedreno still requires a proprietary firmware file for the 3D acceleration (but it makes the userspace code of the driver open source, in contrary to Android). Also the testing was made with X11, as it currently did not work with a Wayland compositor (which should be possible after some debugging though).


[![Doom on pmOS with freedreno](/static/img/2017-09-03/doom-lg-lenok-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/doom-lg-lenok.png)

Shortly after that, @Bloo decided to port postmarketOS to his **[LG G Watch R](https://wiki.postmarketos.org/wiki/LG_G_Watch_R_(lg-lenok))**, giving us the **first smartwatch port**. In order to take out the watch and shout *"It's time to play Doom!"* whenever asked for the time, he decided to compile and run it on his device, too. In the photo on the right, Doom is running in its **native resolution** of 320x240 (the watch has 320x320) in Weston through XWayland. On both devices, [Chocolate Doom](https://www.chocolate-doom.org/) has been used, and it is packaged for postmarketOS now.

*Thanks to: @Bloo, @Opendata26*

## Other new devices

We have **eight** new devices. The two from above plus the following:

[![Nexus 7 running Weston](/static/img/2017-09-03/nexus7-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/nexus7.png)

* [Google Nexus 7 (2012) `asus-grouper`](https://wiki.postmarketos.org/wiki/Google_Nexus_7_2012_(asus-grouper)) *(photo on the right)*
* [HTC Desire HD `htc-ace`](https://wiki.postmarketos.org/wiki/HTC_Desire_HD_(htc-ace))
* [HTC Desire `htc-bravo`](https://wiki.postmarketos.org/wiki/HTC_Desire_(htc-bravo))
* [Mozilla Flame `t2m-flame`](https://wiki.postmarketos.org/wiki/Mozilla_Flame_(t2m-flame))
* [Galaxy Note II `samsung-n7100`](https://wiki.postmarketos.org/wiki/Galaxy_Note_II_(samsung-n7100))
* [Sony Xperia Z1 Compact `sony-amami`](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z1_Compact_(sony-amami))


*Thanks to: @antonok, @ata2001, @Bloo, @drebrez, @kskarthik, @Victor9, @yuvadm and everyone who helped the porters in the chat*

## Initramfs is full of new features

[![on screen keyboard](/static/img/2017-09-03/osk-wave-thumb.gif){: class="fr ml3 mb3" }](/static/img/2017-09-03/osk-wave.gif)

The `initramfs` is a small filesystem with an init script, that prepares the environment before it passes control to the init system running in the real root partition. In case of postmarketOS, we use it to **find and optionally unlock the root** partition. When the "usb-shell" hook is installed, we also provide a **telnet shell**, which can be used to debug the initramfs (e.g. during new device ports).

@craftyguy and @MartijnBraam have started to write a new **on-screen-keyboard** named [`osk-sdl`](https://github.com/postmarketOS/osk-sdl) from scratch (because we couldn't find an existing one that did not  depend on heavy GUI libraries), which will allow us to do the **unlocking** directly with the device's touch screen (of course keyboards are also supported). It is currently in the process of being integrated, so it will fully replace the unlocking via telnet (in case somebody still wants that, reach out and we'll work out together how we implement it as an optional hook).

To work around tight size limitations on some devices (regarding the `boot.img` file, of which the `intiramfs` is a big part), @drebrez implemented the **`initramfs-extras`** trick: A second initramfs file will store **all the big files** and gets placed in the unencrypted `boot` partition. The real initramfs will detect that by its label and extract everything from `initramfs-extras`. At this point, the `init` script works like before and has all files it needs!

Speaking of small size: The system image generated in the installation step doesn't have a fixed size anymore, but adjusts dynamically! After flashing and booting, the initramfs will check if the flashed image takes up all available space of the system partition, and if it does not, **automatically resize the partition to use all available space**.

[![Splash screen rendered for the Samsung Galaxy SII](/static/img/2017-09-03/splash-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/splash.png)


Check out that cool new **splash screen** ([#206](https://github.com/postmarketOS/pmbootstrap/pull/206))! It gets built dynamically for the device's screen size whenever we build the initramfs. So it always fits perfectly! And in case you don't like it, it comes with a customizable [config](https://github.com/postmarketOS/pmbootstrap/blob/314c17e03cf8cddfd0f385d9db2f23f76f9a0418/aports/main/postmarketos-splash/config.ini)!

Last but not least we did a lot of refactoring (such as placing the `deviceinfo` file inside the initramfs instead of variables that duplicated everything), and added support for a configfs based USB network setup (as some devices need that).

*Thanks to: @craftyguy, @Defcat, @drebrez, @ollieparanoid, @pablog, @MartijnBraam*


## Interoperability

[![Recovery zip installation in TWRP](/static/img/2017-09-03/twrp-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/twrp.png)

With all the porting we have learned, that lots of devices have lots of different flashing methods, that we can or must use. In some cases it isn't even possible to directly write to the system partition for example, but it is possible to flash a **recovery zip** through a recovery operating system, such as the popular [TWRP](http://twrp.me/). @ata2001 made it possible to create such an image with `pmbootstrap install --android-recovery-zip`, and to *sideload* it while TWRP is running with `pmbootstrap flasher --method=adb sideload`!

Some older Samsung phones are not `fastboot` compatible, but their bootloader implements a so-called `odin`-mode. Samsung expects people to install their proprietary and Windows-only *Odin* program to be able to flash images in that mode. The protocol has been reverse engineered for some devices and can be used with the open source [heimdall](http://glassechidna.com.au/heimdall/) program, even wrapped with our `pmbootstrap`. But for some older phones, the necessary reverse engineering work has not been done and you might consider running the proprietary program to get anything working at all. If you are in that position, you can use the **Odin-compatible export** now, because @drebrez implemented it: `pmbootstrap flasher export --odin`.

In any case, run `pmbootstrap flasher export` to get **symlinks to all resulting files** from `pmbootstrap`, so you can use your favorite flasher tool to bring it onto the device.

*Thanks to: @ata2001, @drebrez*

## Mainline kernel

[![N900 running mainline kernel](/static/img/2017-09-03/n900-mainline-thumb.png){: class="fr ml3 mb3" }](/static/img/2017-09-03/n900-mainline.png)

One of our goals is using the mainline Linux kernel on **as many mobile devices as possible** (usually on Linux based smartphones, each device runs its own outdated fork of the kernel, that can not be updated sanely to the latest version). This involves the huge task of rewriting the drivers to work with the current kernel APIs. Nevertheless, some people have been doing that since long before postmarketOS existed. In the case of the **Nokia N900**, their mainlining efforts are so advanced, that we are able to **use the mainline kernel as default**  kernel already, therefore jumping from `2.6.x` to `4.12`!

Moreover desktop Linux distributions do not only provide the kernel from the same source code, but also use **one binary kernel package for multiple devices** (of the same CPU architecture). As this makes maintenance easier again, we follow that approach with our `linux-postmarketos` package. It configures the kernel to support multiple devices at once (currently the N900 and QEMU) by supporting **kernel modules** and **multiple device trees**. On a side note, it is not possible for us to use Alpine's kernels right now, because it does not have support for smartphones configured and we wouldn't be as flexible as we are now (temporarily applying patches etc).

*Thanks to: @craftyguy, @MartijnBraam (#228, #159)*


## New infrastructure

We now have several different key pieces of infrastructure in place to support the ongoing project development. First of all, as you might have noticed, we have a brand new **homepage** that hosts both our main landing page as well as this blog, and has links to all of our online resources. You might have also seen our new **logo** which - besides looking great - is [rendered programatically](https://github.com/postmarketOS/postmarketos.org/blob/2e4be89ee8ec656620203fa825e088421afcf092/logo/__init__.py)!

Our GitHub-based **wiki** has served us well up until now, but we have larger plans for it. To that end, we've [migrated](https://gist.github.com/ollieparanoid/6ac9122e31258a7ab8498a362b249fa8) to a [proper MediaWiki server](https://wiki.postmarketos.org). It has a complete [public backup](https://github.com/postmarketOS/wiki). Did you know that `git` has [MediaWiki support](https://github.com/Git-Mediawiki/Git-Mediawiki/wiki) nowadays?

**Travis CI** verifies the checksums of downloads in our package recipes now, and we run `shellcheck` over more scripts across the source tree. These changes in combination with only making PRs for almost all changes and consequently fixing bugs, [`pmbootstrap`](https://github.com/postmarketOS/pmbootstrap) runs pretty stable now.

With over 100 people in the [Matrix/IRC](https://wiki.postmarketos.org/wiki/Matrix_and_IRC) channel and *lots* of messages coming in every day, we decided to create **`##postmarketOS-offtopic`** to keep the backlog in `#postmarketOS` a bit shorter.

*Thanks to: @ata2001, @CmdrWgls, @MartijnBraam, @ollieparanoid, @yuvadm*

## Raw numbers
- `>`100 people in the [channel](https://wiki.postmarketos.org/wiki/Matrix_and_IRC)
- 605 [/r/postmarketOS](https://www.reddit.com/r/postmarketOS/) readers
- [pmbootstrap](https://github.com/postmarketOS/pmbootstrap)
    - 554 stargazers
    - 223 closed PRs
    - 185 closed issues
    - 75 open issues
    - 54 watchers
    - 47 forks
    - 27 contributors (`git shortlog --summary --numbered | wc -l`)

## Closing words
What you see here is only the tip of the iceberg. So much work has gone into fixing bugs, and little improvements, that it would be ridiculous to go through the effort and list them all. The community has grown so fast in such a short time, and we have **people with all kinds of skills** on board, ranging from Linux experts to kernel hackers to people who [reverse engineer bootloaders](https://wiki.postmarketos.org/wiki/Mediatek) (hi @McBitter!).

So if you read through the whole post, you are probably interested in what we do. Consider contributing to the project, the **entry barrier is really low**. [`pmbootstrap`](https://github.com/postmarketOS/pmbootstrap/) automatizes everything for you, and we do live hand-holding in the [chat](https://wiki.postmarketos.org/wiki/Matrix_and_IRC) in case something goes wrong. There are a lot of [issues](https://github.com/postmarketOS/pmbootstrap/issues), so there's plenty to do. And plenty of fun to have. **Join us and tell your favorite media about us!**



