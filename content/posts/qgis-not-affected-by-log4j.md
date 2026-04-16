---
title: "QGIS not affected by Log4J"
date: "2021-12-14T18:11:25+00:00"
draft: false
authors: ["underdark"]
categories: ["Public Service Announcement"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p class="wp-block-paragraph">The Log4J vulnerability has been dominating recent tech news. Consequently, we&#8217;ve received many request asking whether QGIS is affected. Therefore, we&#8217;d like to clarify: </p>



<p class="wp-block-paragraph">QGIS is not a Java application. QGIS is built using C++ and Python. QGIS therefore does not use any Java component, including Log4j(ava).</p>



<p class="wp-block-paragraph">It is technically possible that a plugin interfaces with Java applications. If you are aware of any potential vulnerabilities, please contact the plugin developers through the contact information provided in the plugin metadata. </p>
