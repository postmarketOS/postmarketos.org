title: "Frequently Asked Questions"
---

### Why is postmarketOS based on Alpine Linux?

The biggest upside is, that Alpine is small. The base installation is about **5 MB**! Only because of that, our development/installation tool <code>pmbootstrap</code> is able to abstract everything in chroots and therefore keep the development environment the same, no matter which Linux distribution your host runs on.

And if you messed up (or we have a bug), you can simply run <code>pmbootstrap zap</code> and the chroot will be set up again in seconds. Imagine how long it would take to do the same with Debian (which is a fine distributions for plenty of other use cases).

Another angle on the tininess of Alpine - many older devices don't have much space to spare, so hilariously tiny system images can be quite useful or even required.

### Will Android apps be supported?
Currently, our best bet seems to be getting [Anbox](https://wiki.postmarketos.org/wiki/Anbox) running on postmarketOS. It's highly recommended to use native Linux applications though, as there are some downsides to Android apps:

* Freedom issues (most are proprietary, or only work together with a proprietary network, some even track you), see [F-Droid](https://f-droid.org/) for FLOSS programs, that respect your freedom.
* Heavy resource usage: With all resources, we will most likely need to run a Android environment next to your regular Linux. So it will use up more RAM and CPU compared to native Linux applications.

So at least try to find a native-Linux alternative for your favorite application or ask yourself if you really need it. For app developers, consider using [Kirigami UI](https://dot.kde.org/2017/01/02/kde-releases-beta-kirigami-ui-20) or similar to develop apps for both mainstream mobile OSes (Android/iOS) as well as natively for Linux distributions.

### Can project Treble help postmarketOS?
Google proposed [Treble](https://android-developers.googleblog.com/2017/05/here-comes-treble-modular-base-for.html) to improve the update situation for Android by having a "vendor implementation" with a stable API, that Android builds upon. The idea is, that you can swap out the Android version easily, because of that API. As postmarketOS developers see it, that is a step in the right direction, but it does not resolve the updates problem completely.

You will still have the "vendor implementation", which is different for every device. It will contain at least the kernel and drivers (kernel/userspace), for which you, as a user, depend on the manufacturer to keep it updated, and which will probably not be mainlined. This means, that after two years or so, when the support runs out, you will still have a device, that does not get updates anymore. Only for a smaller component of the operating system.

Also keep in mind, that this will work for newer Android O phones only. We already have an alarmingly high number of phones, which will never get that improvement. They can be saved from being electronic waste with projects like postmarketOS.

## Development
See also: [Development guide](https://wiki.postmarketos.org/wiki/Development_guide)

### Why don't we use firmware files from Android's firmware partition?
When we package it directly, we have the following advantages (see the discussion in [#637](https://github.com/postmarketOS/pmbootstrap/issues/637)):

* We know which version we have
* We can update it easily (either with official new versions, or with hacks like nexmon)
* We don't run into conflict with other OSes that may be installed on the device (e.g. when uninstalling pmOS and installing another ROM, or when doing NFS boot)
* This also works for non-Android devices, which may not have such a firmware partition.

### Why do we use squash 'n' merge for pull requests?
First of all, we'll keep your comments in the commits, as long as they make sense in the squashed commit (no "fixed checksums" etc).
The big reason for "squash and merge" is, that the reviewer usually tests and reviews the last commit in the branch only. After all, that is the commit, that the users will run. Testing everything in-between would take a lot more time, which could be spent better elsewhere in the project. Besides that, it has the following advantages:

* Consistency with all other PRs
* Code is fully git-bisectable
* Less noise in the git log (also useful for git blame)

If you feel like multiple commits should be merged without being squashed, please make multiple PRs for them. Especially when you note somewhere, that you have another PR coming, that depends on the other one, we will do our best to prioritize getting that PR in, so you are not blocked.

Just to avoid confusion, ''we'' squash the commit for you, it's totally okay to have multiple commits in one PR (it even makes the history easier to read, when commits come after a code review for example).