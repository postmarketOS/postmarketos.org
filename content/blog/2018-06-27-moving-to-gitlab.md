title: "postmarketOS is #movingtogitlab"
date:  2018-06-27
---

[![Broken Sony Xperia Z2 Tablet](/static/img/2018-06/broken-castor-thumb.jpg)](/static/img/2018-06/broken-castor.jpg)

After learning that [Microsoft will buy GitHub at the end of 2018](https://www.bloomberg.com/news/articles/2018-06-04/microsoft-agrees-to-buy-coding-site-github-for-7-5-billion), for a lot of people [trust in GitHub was shattered](https://jacquesmattheij.com/what-is-wrong-with-microsoft-buying-github) like the glass of [@opendata26](https://gitlab.com/opendata26)'s [Sony Xperia Z2 Tablet](https://wiki.postmarketos.org/wiki/Sony_Xperia_Z2_Tablet_(sony-castor-windy)). But independent of that, GitHub has always had a vendor lock-in with the user's issues and pull requests hidden behind a rate limited API instead of a proper export feature. And even if you managed to export it through that API, you can not host your own GitHub instance and modify it as you like because there is not even a partially open source version of it.

We want to be in control of our own data. While we can't maintain a self-hosted solution at this point, at least we want to be able to create a public backup of all our > 1500 issues and pull requests once a week. After [some discussion](https://github.com/postmarketOS/postmarketos.org/issues/37) we ended up with gitlab.com as alternative, because its API allows to create a [whole backups at once](https://docs.gitlab.com/ee/api/project_import_export.html) and we can [import](https://gitlab.com/help/user/project/settings/import_export.md) them into our own instance if we want to do that in the future. The workflow is similar to GitHub, so we expect a rather smooth transition compared to using something entirely different.

The migration is scheduled for **Saturday (2018-06-30)**. If you have written anything in issues or pull requests in the postmarketOS repositories on GitHub, consider **[creating a gitlab account](https://gitlab.com/users/sign_in) with the same e-mail address as your GitHub account** for a smooth migration (so it will show what you have written on GitHub with your gitlab user on gitlab).

Thanks to [@craftyguy](https://gitlab.com/craftyguy) for migrating our CI scripts in [#1539](https://github.com/postmarketOS/pmbootstrap/pull/1539). Also thanks to everyone working at GitHub for providing us with their hosting service for [more than a year](/blog/2018/06/09/one-year/). A good opportunity for Microsoft to follow through with their promises of being nice to the open source community would be opening up GitHub more. In case you think that won't happen and want to move away from GitHub as well, make sure to carefully evaluate all the platforms that are out there. Only because gitlab was the best match for us doesn't mean that you can't find a better one for your project.

### Comments
* Reddit
* HN
