---
title: "Update on QGIS 4.0 Release Schedule and LTR Plans"
date: "2025-10-07T21:24:52+00:00"
draft: false
authors: ["underdark"]
categories: ["Uncategorized"]
featured_image: "/wp-content/uploads/2025/10/blog-qgis40-soon.png"
---

<p class="wp-block-paragraph">Following the earlier announcement that <a href="https://blog.qgis.org/2025/04/17/qgis-is-moving-to-qt6-and-launching-qgis-4-0/">QGIS is moving to Qt 6 and launching QGIS 4.0</a>, we want to share an important update about the QGIS 4.x roadmap.</p>



<p class="wp-block-paragraph">After extensive discussion on the <a href="https://lists.osgeo.org/pipermail/qgis-developer/2025-September/067787.html">developer mailing list</a>, the QGIS community has agreed to adjust the 4.x release schedule to ensure a smooth transition to Qt 6 and give plugin developers, testers, and packagers the time they need.</p>



<h2 class="wp-block-heading">📅 New Release Date for QGIS 4.0</h2>



<p class="wp-block-paragraph">QGIS 4.0 will now be released in <strong>February 2026</strong> instead of October 2025. This change is reflected in the updated <a href="https://qgis.org/resources/roadmap/">QGIS release roadmap</a>.</p>



<h2 class="wp-block-heading">💡 QGIS 4.2 Will Be the First 4.x LTR</h2>



<p class="wp-block-paragraph">The first LTR in the 4.x series will be <strong>QGIS 4.2,</strong> and it is <a href="https://qgis.org/resources/roadmap/">scheduled</a> to land in the LTR repos in October 2026.<br>QGIS 3.44 has been released as the final version of the 3.x series and will serve as the last long-term release (LTR) before the transition to QGIS 4.0. This ensures users will have a stable 3.x platform for an extended period.<br>To avoid delays for macOS users, we are exceptionally working on backporting the notarised macOS build process developed for QGIS 4.0 to QGIS 3.44.</p>



<h2 class="wp-block-heading">🧭 What’s Next</h2>



<p class="wp-block-paragraph">We know many plugin developers and users are eager to test the new Qt6-based version, and we&#8217;re happy to report that Qt6 builds are available for all platforms:</p>



<ul class="wp-block-list">
<li><strong>Windows</strong>: Qt6 builds of&nbsp;<strong>all release branches and master</strong>&nbsp;are available now via the&nbsp;<a href="https://trac.osgeo.org/osgeo4w/">OSGeo4W installer</a></li>



<li><strong>Linux (Debian)</strong>: Qt6 support is available side-by-side with Qt5. Please check for your specific operating system version. </li>



<li><strong>MacOS</strong>: Mac users planning to test QGIS 4.0 are encouraged to try the new notarized builds provided at <a href="https://github.com/opengisch/qgis-notarize">opengisch/qgis-notarize</a>. These will be moved to QGIS.org and become the official, notarized packages for macOS as soon as 4.0 is released.</li>
</ul>



<p class="wp-block-paragraph">We’ll continue to share updates as we move closer to February 2026.</p>



<p class="wp-block-paragraph">Thank you for your understanding, contributions, and ongoing support!</p>
