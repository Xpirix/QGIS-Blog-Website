---
title: "QGIS Userbase Analytics"
date: "2022-06-16T14:15:20+00:00"
draft: false
authors: ["timlinux"]
categories: ["Public Service Announcement"]
tags: ["analytics", "QGIS Community"]
featured_image: "/wp-content/uploads/2022/06/3dd204e4106cc6616aa45ef3d8ede731b8468ffe.png"
---

<p class="wp-block-paragraph"></p>



<h1 class="wp-block-heading">Background</h1>



<p class="wp-block-paragraph">Understanding which regions QGIS is being used in, which versions are in active use, which platforms it is being used on, and how many users we have is hugely beneficial to our ability as a project to serve our users. Back in 2017 at the bi-annual QGIS hackfest in Nødebo, Denmark, we had a long discussion about key project goals and the need to better understand our user base in order to plan the future direction of the project, and allocate funding and resources to where they are needed most</p>



<p class="wp-block-paragraph">Typically proprietary software vendors have ready access to detailed user data through telemetry code which they embed in their software. This telemetry code &#8216;phones home&#8217; key metrics, which together with other techniques such as license sales analysis gives them a very detailed insight into their user base. The data these vendors collect is typically not shared, so their users do not benefit from being able to understand how their data is used.</p>



<p class="wp-block-paragraph">For QGIS.org, having to resort to what are generally considered to be nefarious and privacy-invading techniques of siphoning user data from our users goes against the ethos we try to promote as an open project. Further, since QGIS is freely available and doesn&#8217;t require any self-registration,  we do not have a user database we can consult for such analytics. Additional factors make understanding usage levels hard. For example, a single user can download a copy of a QGIS installer and distribute it to many other users, and conversely web crawlers and bots can download many copies of QGIS installers and never install them. Because of this, simply counting the number of downloads from our website does not give a useful picture of our user base.</p>



<p class="wp-block-paragraph">So we needed to come up with an approach that:</p>



<ol class="wp-block-list"><li>Does not invade our user&#8217;s privacy</li><li>Does not require including telemetry code in QGIS which exfiltrates user information from their system</li><li>Does not store any user-identifiable data on our servers</li><li>Is open and transparent in the data collection methodology</li><li>Openly shares the insights we gain from our analytics to the broader community </li></ol>



<p class="wp-block-paragraph">The most obvious privacy-respecting way we could find to understand more about our users was to collect metrics of access to the QGIS News Feed. In order to display the latest news on startup, QGIS Desktop makes a request to <a href="https://feed.qgis.org">https://feed.qgis.org</a> when it is opened. On the server that hosts the feed, we can then use the web server logs to understand which operating system and version of QGIS made the news feed request. Additionally, using the GeoIP library we can resolve each request to the country from which it originated. These pieces of information are included in the User-Agent headers sent by QGIS when it makes a request to the QGIS News Feed.</p>



<p class="wp-block-paragraph">This process is anonymous, transparent, and simple to disable. It does not identify unique machines. Only one event is logged per unique network per hour. Only one event is logged per QGIS installation per day, and the event is only triggered when the user opens the QGIS Desktop application.</p>



<p class="wp-block-paragraph">Operating system statistics are derived from QGIS version information, and no system fingerprinting or telemetry is implemented.</p>



<p class="wp-block-paragraph">Location information is derived from the request source IP address, which is immediately discarded on the server after resolving it to the country of origin. </p>



<p class="wp-block-paragraph">No logging on the QGIS News Feed server occurs with legacy installations that do not have the news feed feature, offline usage of QGIS, and installations for which feed collection is disabled (see below for info on how to disable it). It will also have statistics skewed in scenarios where atypical networking infrastructure is in effect, such as using a virtual private network.</p>



<p class="wp-block-paragraph">Despite these caveats, the statistics should provide a good high-level overview of how QGIS is being used, such as the breakdown of QGIS across operating systems and versions &#8211; information that is incredibly useful to the QGIS developer team. Only the following four pieces of information are collected:</p>



<ul class="wp-block-list"><li>The date (aggregated by day)</li><li>The QGIS version</li><li>The Operating System</li><li>Country (based on IP which is immediately discarded)</li></ul>



<p class="wp-block-paragraph"></p>



<h2 class="wp-block-heading">Opting out</h2>



<p class="wp-block-paragraph">If you wish to opt-out of this data collection, simply disabling the feed retrieval, using QGIS offline, or blocking access to the QGIS RSS feed address (feed.qgis.org) on your network will exclude you from this process. QGIS Desktop provides options for disabling version checking and feed access under <code>Settings ➔ Options ➔ General ➔ Application</code>. Note that by default this setting is specific to each individual user profile.</p>



<figure class="wp-block-image size-large"><a href="/wp-content/uploads/2022/06/qgis_feed_settings_configuration.png"><img loading="lazy" width="628" height="527" data-attachment-id="2483" data-permalink="http://blog.qgis.org/2022/06/16/qgis-userbase-analytics/qgis_feed_settings_configuration/" data-orig-file="/wp-content/uploads/2022/06/qgis_feed_settings_configuration.png" data-orig-size="628,527" data-comments-opened="0" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;}" data-image-title="qgis_feed_settings_configuration" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2022/06/qgis_feed_settings_configuration.png" src="/wp-content/uploads/2022/06/qgis_feed_settings_configuration.png" alt="" class="wp-image-2483" srcset="/wp-content/uploads/2022/06/qgis_feed_settings_configuration.png 628w, /wp-content/uploads/2022/06/qgis_feed_settings_configuration.png 150w, /wp-content/uploads/2022/06/qgis_feed_settings_configuration.png 300w" sizes="(max-width: 628px) 100vw, 628px" /></a></figure>



<h2 class="wp-block-heading">Viewing the analytics</h2>



<p class="wp-block-paragraph">We have made a public dashboard publicly available at <a href="https://analytics.qgis.org">https://analytics.qgis.org</a>. The dashboard was made using the fantastic open-source <a href="https://www.metabase.com/">Metabase</a> analytics package. </p>



<p class="wp-block-paragraph"><strong>Credits:</strong> This post was written by Charles Dixon-Paver and Tim Sutton</p>



<p class="wp-block-paragraph"></p>
