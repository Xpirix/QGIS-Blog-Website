---
title: "QGIS Server certified as official OGC reference implementation"
date: "2018-06-27T17:34:46+00:00"
draft: false
authors: ["underdark"]
categories: ["QGIS Server"]
tags: ["OGC", "QGIS Server"]
featured_image: "/wp-content/uploads/2019/04/ogc-1.png"
---

<p>We are very excited to announce that <a href="https://www.qgis.org/fr/site/about/features.html?highlight=server#qgis-server">QGIS Server</a> has been successfully certified as a compliant WMS 1.3 server against the <a href="http://www.opengeospatial.org/resource/products/details/?pid=1496">OGC certification platform</a>, and moreover, it is even considered as a reference implementation now!</p>
<p><img loading="lazy" data-attachment-id="2014" data-permalink="http://blog.qgis.org/2018/06/27/qgis-server-certified-as-official-ogc-reference-implementation/qgis_server_wms_ogc_badge/" data-orig-file="/wp-content/uploads/2018/06/qgis_server_wms_ogc_badge.png" data-orig-size="227,255" data-comments-opened="0" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;}" data-image-title="qgis_server_wms_ogc_badge" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2018/06/qgis_server_wms_ogc_badge.png" class="size-full wp-image-2014 aligncenter" src="/wp-content/uploads/2018/06/qgis_server_wms_ogc_badge.png" alt="" width="227" height="255" srcset="/wp-content/uploads/2018/06/qgis_server_wms_ogc_badge.png 227w, /wp-content/uploads/2018/06/qgis_server_wms_ogc_badge.png 134w" sizes="(max-width: 227px) 100vw, 227px" /></p>
<p>This is the first step on our roadmap of having a fast, compliant and bullet proof web map server that is straightforward to publish from a classical QGIS project.</p>
<p><strong>What does it mean?</strong></p>
<p>Having a certified server means that QGIS Server successfully passes the automated and semi automated tests that ensure we are 100% compliant with the standards. That means you can trust QGIS to be used by any WMS client seamlessly.<br />
Moreover, that certification is now powered by a continuous integration system that checks every night in developement versions if we still pass the tests.</p>
<p>Daily compliance reports are available on the new <a href="http://test.qgis.org/" target="_blank" rel="noopener">test.qgis.org</a> website.</p>
<p><strong>What&#8217;s next?</strong></p>
<p>Building the automated testing platform and getting officially certified was only the first step. We now are starting to certify the WFS services, thanks to the <a href="http://blog.qgis.org/2018/06/22/qgis-grant-programme-2018-results/">latest grant application program</a> support.</p>
<p>We also want QGIS server development to be performance-driven. The following projects are particularly relevant:</p>
<ul>
<li><a href="https://github.com/camptocamp/ms_perfs">MS-Perf</a> produces <a href="https://gmf-test.sig.cloud.camptocamp.net/ms_perfs/">benchmark reports with MapServer and GeoServer</a>.</li>
<li><a href="https://github.com/pblottiere/graffiti">graffiti </a> and <a href="https://github.com/Oslandia/QGIS-Server-PerfSuite">PerfSuite</a> tools have been designed to create a really light tool, easy to enrich with new datasets and performance tests, and easy to integrate in continuous integration systems. It compares QGIS-ltr, QGIS-rel and QGIS-dev nightlies for the same scenarios in details and produces <a href="http://test.qgis.org/perf_test/graffiti/" target="_blank" rel="noopener">html reports</a>. It can also graph performance history for the development version to track regressions or improvements.</li>
</ul>
<p>Many thanks to the supporters and voting members that helped bootstrap all those testing platforms and offer them to the community.</p>
<p>If you want to support or give a hand on the QGIS desktop client side, we think that area would deserve some love too!</p>
