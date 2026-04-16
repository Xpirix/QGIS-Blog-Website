---
title: "Introducing new QGIS macOS packages"
date: "2019-07-29T19:39:44+00:00"
draft: false
authors: ["timlinux"]
categories: ["Uncategorized"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p><em><span style="font-weight:400;">We now have signed packages for macOS. You can find these packages published on the official QGIS download page at </span><a href="http://download.qgis.org/"><span style="font-weight:400;">http://download.qgis.org</span></a><span style="font-weight:400;">. </span></em></p>
<h1><span style="font-weight:400;">Rationale</span></h1>
<p><span style="font-weight:400;">In addition to being a very powerful and user-friendly open source GIS application, QGIS can be installed on different operating systems: MS Windows, macOS, various flavours of Linux and FreeBSD. </span></p>
<p><span style="font-weight:400;">Volunteers help with generating the installers for those platforms. The work is highly valuable and the scale of effort put into packaging over the years is often underappreciated. QGIS has also grown significantly over the years and so has its complexity to package relevant libraries and 3rd party tools to the end-users.</span></p>
<p><span style="font-weight:400;">QGIS has been packaged on OSX/macOS for many years, making it one of the few GIS applications you can use on this platform. This is largely thanks to the tireless work of </span><span style="font-weight:400;">William Kyngesburye</span><span style="font-weight:400;"> (</span><a href="https://www.kyngchaos.com/software/qgis/"><span style="font-weight:400;">https://www.kyngchaos.com/software/qgis/</span></a><span style="font-weight:400;">) who has shouldered the task of compiling QGIS and its dependencies and offering them as disk images on the official QGIS website. The packages for each new release are available within days for all supported macOS versions.</span></p>
<p><span style="font-weight:400;">Unlike most other operating systems, macOS can only be run on Apple hardware. This is a barrier for developers on other platforms who wish to compile and test their code on macOS. For other platforms, QGIS developers have automated packaging, not only for the major releases but also for daily code snapshots (aka nightly or master builds). Availability of the daily packages has allowed testers to identify platform-specific issues, well before the official release.</span></p>
<p><span style="font-weight:400;">Apple also has a system of software signing so that users can verify if the packages are securely generated and signed by the developers. Up until now, signed macOS packages were not available, resulting in users who are installing QGIS needing to go into their security preferences and manually allow the QGIS application to be run. </span></p>
<h1><span style="font-weight:400;">A new approach</span></h1>
<p><span style="font-weight:400;">In October 2018, <a href="https://www.lutraconsulting.co.uk/">Lutra </a>Consulting </span><span style="font-weight:400;">started their work on packaging QGIS for macOS. The work has been based on OSGeo tap on <a href="https://github.com/OSGeo/homebrew-osgeo4mac">Homebrew</a></span><span style="font-weight:400;">. Homebrew is a ‘bleeding edge’ package manager similar to those provided by Gentoo or Arch Linux. The packages by Lutra bundle the various libraries and resources on which QGIS depends into a single QGIS.app application bundle.  The packages were made available in late 2018 for QGIS official releases and master. QGIS Mac users have eagerly tested and reported various issues and the majority of them were resolved in early 2019.</span></p>
<p><span style="font-weight:400;">Following the successful launch of the prototype packages and in discussion with other developers, it was agreed to transfer the ownership of the packaging infrastructure and scripts (</span><a href="https://github.com/qgis/QGIS-Mac-Packager"><span style="font-weight:400;">https://github.com/qgis/QGIS-Mac-Packager</span></a><span style="font-weight:400;">) to QGIS.org. Using the new infrastructure and OSGeo Apple developers certificate, all QGIS ‘disk images’ (installers) have been available since late May 2019.</span></p>
<p><span style="font-weight:400;">What are the main difference between the new installers and the ones offered by Kyngchaos? The new installer offers:</span></p>
<ul>
<li style="font-weight:400;"><span style="font-weight:400;">3 clicks to install: download, accept Terms &amp; Conditionss, drop to /Application</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">All dependencies (Python, GDAL, etc)  are bundled within the disk image</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">Signed by OSGeo Apple certificate</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">Availability of nightly builds (master)</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">Scripts for bundling and packaging are available on a public repository</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">Possibility of installing multiple versions (e.g. 3.4 LTR, 3.8 and master) side-by-side</span></li>
</ul>
<p><span style="font-weight:400;">There are some known issues:</span></p>
<ul>
<li style="font-weight:400;"><span style="font-weight:400;">Lack of support for macOS versions earlier than 10.13 (</span><a href="https://github.com/qgis/QGIS-Mac-Packager/issues/6"><span style="font-weight:400;">https://github.com/qgis/QGIS-Mac-Packager/issues/6</span></a><span style="font-weight:400;">)</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">Issues with some GRASS modules relient on Python 2.x</span></li>
</ul>
<p><span style="font-weight:400;">For a full list, see: </span><a href="https://github.com/qgis/QGIS-Mac-Packager"><span style="font-weight:400;">https://github.com/qgis/QGIS-Mac-Packager</span></a></p>
<h1><span style="font-weight:400;">Further work</span></h1>
<p><span style="font-weight:400;">We hope that by providing the new installers, macOS users will have a better experience in installing and using QGIS. Ideally, with the availability of nightly builds and being more accessible to new users, more software bugs and issues will be reported and this will help to improve QGIS overall.</span></p>
<p><span style="font-weight:400;">Maintaining and supporting macOS costs more compared with other platforms. As QGIS is one of the only viable GIS applications for macOS users in an enterprise environment, we encourage you and your organisation to <a href="https://www.qgis.org/en/site/getinvolved/governance/sustaining_members/sustaining_members.html">become a sustaining</a> member to help assure the continued availability and improvement of the macOS packages in the long term.</span></p>
<h1><span style="font-weight:400;">Future plans</span></h1>
<p><span style="font-weight:400;">In future we plan to migrate the packaging process to use Anaconda QGIS packages as the source for package binaries. We also would like to integrate macOS builds into the Travis-CI automated testing that happens whenever a new GitHub pull request is submitted so that we can validate that the macOS packages do not get any regressions when new features are introduced.</span></p>
<h1><span style="font-weight:400;">Conclusion</span></h1>
<p><span style="font-weight:400;">With this work, we now have nightly builds of the upcoming release (‘master’) branch available for all to use on macOS. We now have signed packages and we have an automated build infrastructure that will help to ensure that macOS users always have ready access to new versions of QGIS as they become available. You can find these packages published on the official QGIS download page at </span><a href="http://download.qgis.org/"><span style="font-weight:400;">http://download.qgis.org</span></a><span style="font-weight:400;">. A huge thanks to the team at Lutra Consulting for taking this much-needed work, and to </span><span style="font-weight:400;">William Kyngesburye</span><span style="font-weight:400;"> for the many years that he has contributed towards the macOS/OSX QGIS packaging effort!</span></p>
<p><span style="font-weight:400;"> </span></p>
