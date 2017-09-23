title: Why supporting the Librem Phone crowdfunding campaign helps postmarketOS (and friends)
date: 2017-09-24
---

[TOC]

## Proprietary components make smartphones insecure
Whenever you buy *any* smartphone, you get a device full of proprietary components. These are integrated so deeply, that they can access everything on your phone (e.g. camera, microphone, browser history and chat messages). Proprietary means, that it is designed to be impossible to be changed by anyone but the vendor and that it can only be understood with immense efforts.

Oftentimes, when people analyze them anyway, they find security holes and sometimes even [backdoors](https://redmine.replicant.us/projects/replicant/wiki/SamsungGalaxyBackdoor). Vendors refuse to update known security holes, when the short times of support run out. People who are aware of this issue are forced to buy new devices every few years, while the general public doesn't even realize how insecure their devices are, thus lowering security for everyone. What good is it when you have a protected phone, but most other people you meet and communicate with might as well be carrying around spying devices?


## postmarketOS tries to fix existing devices
Our solutions is replacing the entire operating systems of these devices with an alternative one, that contains as much free- and open source software as possible. In order to do that, we're bending the security-focused [Alpine Linux](https://alpinelinux.org) (you may know it from Docker, but it is [much older](http://git.net/ml/linux.leaf.devel/2005-08/msg00039.html)) to work on all kinds of existing mobile devices. In the spirit of real Linux distributions, there is a package manager and as much freedom for the user as possible. We aim for a [10 year life-cycle for smartphones](https://postmarketos.org/blog/2017/05/26/intro/) and although we're in pre-alpha state, we made [quite some progress](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/) and have [lots of documentation](https://wiki.postmarketos.org/) available.


## Librem 5 phone does it right by design
The people from Purism provide another way to reach the same goal: They bend [Debian GNU/Linux](https://debian.org) for one specific phone, which they will create from scratch, the [Librem 5](https://puri.sm/shop/librem-5/). It will only have as few proprietary components as necessary, and these will be isolated from the rest of the system. That means, even if someone hacks them through a security hole, your chat messages stored on the device are still safe.

Planned hardware kill-switches for camera, microphone, wifi, bluetooth and cellular modem will allow you to turn on certain components (which are highly likely to be proprietary) only when needed. Imagine flipping the microphone switch before and after each phone call - that way you could be sure that it can not listen to any private conversations you are having from person to person while carrying your phone around.

It will be possible to exchange the battery and extend the space with a microSD slot, two important characteristics that increase the lifetime of a phone.


## Common ground
The Librem 5 is privacy and security focused, so we expect it to have full disk encryption. This term means, that before you can boot into your operating system, you would need to type in a password. And without that password, someone else is not able to find out which data is stored on the device, or which programs are installed. So in order to type in that password, you would use a keyboard on a PC, but on a phone you will need an on-screen keyboard. We have put some research into this topic already, and as there was no existing Linux program just for that purpose, we created our own [osk-sdl](https://github.com/postmarketOS/osk-sdl) program. That is one example where the Purism could use a component written by our community and make it a shared component, that we develop and improve with joined forces.

User interfaces are another example: Purism will either use [KDE's plasma-mobile](https://www.kde.org/announcements/kde-purism-librem5.php) or [Gnome](https://www.gnome.org/news/2017/09/gnome-foundation-partners-with-purism-to-support-its-efforts-to-build-the-librem-5-smartphone/), while postmarketOS is interested in [all kinds of mobile-friendly user interfaces](https://github.com/postmarketOS/pmbootstrap/issues/62). We have done [early work](https://postmarketos.org/blog/2017/09/03/100-days-of-postmarketos/#plasma-mobile-kdes-plasma-desktop-for-phones) on plasma-mobile already, and Gnome is [directly provided](https://pkgs.alpinelinux.org/packages?name=gnome*&branch=edge&repo=&arch=&maintainer=) by our upstream friends. So no matter which one will finally run on the Librem 5, we will benefit from them making sure it is ready for daily usage on mobile phones.

We were happy to read, that Purism teamed up with [Matrix](https://matrix.org/blog/2017/08/24/the-librem-5-from-purism-a-matrix-native-smartphone/) to provide the native dialer and messaging program. While not being related to the movie, Matrix is a decentralized open source protocol for real-time communication with state-of-the-art end-to-end encryption. It is a big win for privacy and security, that Librem users will be able to use that by default. In addition to traditional, unencrypted telephony and SMS when necessary. The best part for us is of course, that we could package the resulting applications for postmarketOS as well, bringing them to a wide range of old devices!

## All or nothing
There is a pattern here: Once the Librem 5 development takes off, everything that gets built for it (by Purism or by the wider community) and that is not strictly tied to Debian, can be used by postmarketOS and friends.

No matter which Linux distribution, phone, desktop environment, messenger, init system or libc you prefer: A successful Librem 5 campaign will rapidly improve the situation for all Linux distributions on phones. But it's an all or nothing campaign. When they don't reach their funding goal, they won't even start with any of the awesome features they have in mind.

[So let's make sure that it succeeds.](https://puri.sm/shop/librem-5/)


## Comments
*Whoa, you're early! We'll add the links to HN and Reddit shortly.*
