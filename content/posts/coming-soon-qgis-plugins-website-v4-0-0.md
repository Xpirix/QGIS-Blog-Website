---
title: "Coming soon: QGIS Plugins Website v4.0.0"
date: "2026-07-06T12:41:13+00:00"
draft: false
authors: ["lova65df7ff1260"]
categories: ["Plugin update"]
tags: ["QGIS Plugins", "QGIS Website"]
featured_image: "/wp-content/uploads/2025/01/qgis-plugin-update-1.png"
---

<p class="wp-block-paragraph">We are preparing version <strong>v4.0.0</strong> of the QGIS Plugins Website (<a href="https://plugins.qgis.org">https://plugins.qgis.org</a>), a planned milestone release scheduled for <strong>13 July 2026</strong>. Below is a summary of what is coming and how it may affect plugin developers, so you can review ahead of time.</p>



<h2 class="wp-block-heading">Highlights</h2>



<p class="wp-block-paragraph">This will be our first major release that adopts a proper announcement and release schedule. It will include major improvements and changes related to the security checks and plugins auto-approval; and a new feature for Qt6 compatibility check which was funded by Oslandia (<a href="http://oslandia.com">oslandia.com</a>) and developed by <a href="https://github.com/florentfougeres">@florentfougeres</a>.</p>



<h2 class="wp-block-heading">What is changing in v4.0.0</h2>



<p class="wp-block-paragraph">The items below are planned for this release and are tracked in the changelog until v4.0.0 ships.</p>



<h3 class="wp-block-heading">Major/Breaking changes</h3>



<ul class="wp-block-list">
<li>Expose security checks rules and allow managing them (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/316">#316</a>)<a href="https://github.com/Xpirix"> @Xpirix</a>
<ul class="wp-block-list">
<li>All Security/QA checks rules with their details/status/severity will be exposed in the plugins website docs (Screenshot 1)</li>



<li>Plugin Website administrator can switch the status of each rule or make some rules skippable by plugin authors</li>



<li>Plugin authors will be able to skip some of the rules during the upload with the web UI/API/RPC (Screenshot 2)</li>



<li>Status and severity of each rule can be discussed depending on specific cases. For that, plugin authors are free to raise an issue at <a href="https://github.com/qgis/QGIS-Plugins-Website/issues">https://github.com/qgis/QGIS-Plugins-Website/issues</a>&nbsp;</li>



<li>A detailed documentation about the Security/QA checks will be provided (please see the PR for more information)</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-large"><a href="/wp-content/uploads/2026/06/image.png"><img loading="lazy" width="1024" height="812" data-attachment-id="3550" data-permalink="http://blog.qgis.org/2026/07/06/coming-soon-qgis-plugins-website-v4-0-0/image-27/" data-orig-file="/wp-content/uploads/2026/06/image.png" data-orig-size="1411,1119" data-comments-opened="0" data-image-title="image" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2026/06/image.png" src="/wp-content/uploads/2026/06/image.png" alt="" class="wp-image-3550" srcset="/wp-content/uploads/2026/06/image.png 1024w, /wp-content/uploads/2026/06/image.png 150w, /wp-content/uploads/2026/06/image.png 300w, /wp-content/uploads/2026/06/image.png 768w, /wp-content/uploads/2026/06/image.png 1411w" sizes="auto, (max-width: 1024px) 100vw, 1024px" /></a></figure>



<p class="has-text-align-center wp-block-paragraph"><strong><em>Screenshot 1: QA and Security rules list in the plugins Docs</em></strong></p>



<figure class="wp-block-image size-large"><a href="/wp-content/uploads/2026/06/image-1.png"><img loading="lazy" width="1024" height="863" data-attachment-id="3551" data-permalink="http://blog.qgis.org/2026/07/06/coming-soon-qgis-plugins-website-v4-0-0/image-28/" data-orig-file="/wp-content/uploads/2026/06/image-1.png" data-orig-size="1425,1202" data-comments-opened="0" data-image-title="image" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2026/06/image-1.png" src="/wp-content/uploads/2026/06/image-1.png" alt="" class="wp-image-3551" srcset="/wp-content/uploads/2026/06/image-1.png 1024w, /wp-content/uploads/2026/06/image-1.png 150w, /wp-content/uploads/2026/06/image-1.png 300w, /wp-content/uploads/2026/06/image-1.png 768w, /wp-content/uploads/2026/06/image-1.png 1425w" sizes="auto, (max-width: 1024px) 100vw, 1024px" /></a></figure>



<p class="has-text-align-center wp-block-paragraph"><strong><em>Screenshot 2: Skippable rules during upload</em></strong></p>



<ul class="wp-block-list">
<li>Fix for plugin auto-approval logic (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/294">#294</a>)<a href="https://github.com/Xpirix"> @Xpirix</a>
<ul class="wp-block-list">
<li>Plugins auto-approval will be explicit (two steps) and only available for users who have permission to approve plugins</li>



<li>New plugins version won’t be automatically approved anymore for standard authors even if the previous version was approved. The change here is that <strong>we trust people, not plugins</strong>.</li>
</ul>
</li>



<li>Add a Qt6 compatibility check when releasing a version (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/282">#282</a>) <a href="https://github.com/florentfougeres">@florentfougeres</a>
<ul class="wp-block-list">
<li>An asynchronous task to check the Qt6 compatibility will run whenever a new version is uploaded</li>



<li>The result will be available in the “Qt6 Check” tab in each version details (Screenshot 3)</li>
</ul>
</li>
</ul>



<figure class="wp-block-image size-large"><a href="/wp-content/uploads/2026/06/image-2.png"><img loading="lazy" width="1024" height="387" data-attachment-id="3553" data-permalink="http://blog.qgis.org/2026/07/06/coming-soon-qgis-plugins-website-v4-0-0/image-29/" data-orig-file="/wp-content/uploads/2026/06/image-2.png" data-orig-size="1371,519" data-comments-opened="0" data-image-title="image" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2026/06/image-2.png" src="/wp-content/uploads/2026/06/image-2.png" alt="" class="wp-image-3553" srcset="/wp-content/uploads/2026/06/image-2.png 1024w, /wp-content/uploads/2026/06/image-2.png 150w, /wp-content/uploads/2026/06/image-2.png 300w, /wp-content/uploads/2026/06/image-2.png 768w, /wp-content/uploads/2026/06/image-2.png 1371w" sizes="auto, (max-width: 1024px) 100vw, 1024px" /></a></figure>



<p class="has-text-align-center wp-block-paragraph"><strong><em>Screenshot 3: Qt6 Check tab</em></strong></p>



<ul class="wp-block-list">
<li>Plugin email needs to be verified before approval (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/345">#345</a>) <a href="https://github.com/Xpirix">@Xpirix</a>
<ul class="wp-block-list">
<li>Having an actively contactable email address is going to be a hard requirement going forward and will be part of the approval criteria.</li>



<li>This is important as we will start to share news/updates regarding the plugins website or just as a contact for people that use the specific plugin.</li>



<li>The email validation process will be triggered automatically on plugin upload, email change.</li>



<li>A yearly re-verification will be automatically triggered for each plugin so we can be sure whether the email address is still active or not.</li>
</ul>
</li>
</ul>



<h3 class="wp-block-heading">Minor features, fixes and improvements</h3>



<ul class="wp-block-list">
<li>Add detailed docs for each release type (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/359">#359</a>)<a href="https://github.com/Xpirix"> @Xpirix</a></li>



<li>Fix failing comment creation on fork PRs (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/366">#366</a>)<a href="https://github.com/Xpirix"> @Xpirix</a></li>



<li>Match the PRs/release process with qgis-desktop-docker (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/360">#360</a>)<a href="https://github.com/Xpirix"> @Xpirix</a></li>



<li>Attach static files inside the docker image (<a href="https://github.com/qgis/QGIS-Plugins-Website/pull/352">#352</a>)<a href="https://github.com/Xpirix"> @Xpirix</a></li>
</ul>



<h2 class="wp-block-heading">What this means for plugin developers</h2>



<p class="wp-block-paragraph">If you maintain a plugin, please review the planned changes above before <strong>13 July 2026</strong> to confirm nothing affects your publishing workflow, and tell us about any concerns while there is still time to adjust the release. For that, please raise an issue at&nbsp; <a href="https://github.com/qgis/QGIS-Plugins-Website/issues">https://github.com/qgis/QGIS-Plugins-Website/issues</a>.&nbsp;</p>



<h2 class="wp-block-heading">When and where</h2>



<p class="wp-block-paragraph">Version v4.0.0 is planned for 13 July 2026 and will be deployed as the pinned image `<em>qgis/qgis-plugins-uwsgi:v4.0.0</em>`. You can follow progress on the <a href="https://github.com/qgis/QGIS-Plugins-Website/milestone/1">v4.0.0 milestone</a>. The final release notes will be published on the <a href="https://github.com/qgis/QGIS-Plugins-Website/releases">release page</a> once it ships.</p>



<h2 class="wp-block-heading">Thanks</h2>



<p class="wp-block-paragraph">Thank you to everyone contributing issues, code, and review for the work going into this release.</p>



<p class="wp-block-paragraph"><strong>Reminder: Confirming Plugin Contact Emails</strong></p>



<p class="wp-block-paragraph">If you maintain plugins on the <a href="http://plugins.qgis.org">plugins.qgis.org</a> site, please check for a recent email regarding address verification. If you have not yet verified the email address associated with your plugin, we kindly ask that you do so. Ensuring your contact information is verified allows us to maintain reliable communication and keep you informed about upcoming news and technical updates. In the future, it is our intention to unpublish plugins that do not have a valid maintainer contact email address.</p>



<p class="wp-block-paragraph"></p>
