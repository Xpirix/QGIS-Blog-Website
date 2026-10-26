---
title: "QGIS Server and OGC API Features"
date: "2020-05-13T19:23:46+00:00"
draft: false
authors: ["neumannandreas"]
categories: ["QGIS Server"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>Based on text and information from Paul Blottiere and Alessandro Pasotti (both <a href="https://www.qcooperative.net/">QCooperative</a>)</p>
<p>QGIS Server implements a number of OGC services, such as WMS, WFS, WCS or WMTS and extends these services where useful. Thanks to the efforts of a number of QGIS Server developers and companies, QGIS 3.10 (and 3.4 before) had been certified by the OGC for the WMS 1.3.0 service, and is also a WMS reference implementation.</p>
<p><img src="https://www.qcooperative.net/images/blog/ogcapif/badge.png" alt="alt wording" /></p>
<p>Last year in 2019, a new protocol has been developed and named OGC API Features (commonly known as WFS3). With the purpose of having an up-to-date QGIS Server, both OSGeo and QGIS.ORG have dedicated funds to work on the implementation of this brand-new service: but we wanted to do it right, so the ambition was also to reach the OGC certification!</p>
<p>This new protocol with REST interfaces gets rid of the XML specification to use the OpenAPI standard as well as the JSON open format instead. In other words, it’s not just another protocol to support, but a whole package of changes and fresh mechanisms to work on. It was quite a challenge!</p>
<p>QGIS core developers of QCooperative were remotely participating in OGC sprints to closely monitor the development of the new OGC API Features protocol. Hence, we started its implementation and a fully operational version landed in <a href="http://blog.qgis.org/2019/11/26/qgis-server-is-ready-for-the-new-ogc-api-for-features-protocol/">QGIS Server 3.10</a>.</p>
<h2 id="implementation-and-features">Implementation and features</h2>
<p>As a reminder, the WFS protocol allows to query, retrieve and manipulate vector features, unlike the WMS format which provides raster outputs. OGC API Features is the natural continuity and consistently provides basic mechanisms to retrieve features and corresponding information in a specific area (the famous <code>GetFeatureInfo</code> request in WFS 1.X).</p>
<p>In addition, QGIS Server also provides transactions for the OGC API Features protocol. This means basically that we can update, insert or delete features in the underlying data. And of course, everything can be easily reached and configured through QGIS Desktop.</p>
<p>Yet another interesting thing to note is also the full support of the date and time filtering. Nifty!</p>
<p>And last, but not least, QGIS Server 3.10 provides a default HTML template with an embedded map to explore the data served by the server. There’s literally nothing to configure, it’s just there as soon as you work with the OGC API Features protocol :).</p>
<p align="center"><img src="https://www.qcooperative.net/images/blog/ogcapif/template.png" alt="alt wording" /></p>
<h2 id="ogc-certification">OGC Certification</h2>
<p>Once the implementation was completed, we started to address the OGC certification goal. To avoid unwanted regressions along the way, we first added nightly tests by updating the dedicated <a href="https://github.com/qgis/QGIS-Server-CertifSuite">QGIS repository for OGC tests</a>. From that moment, <a href="http://test.qgis.org/ogc_cite/">HTML reports</a> are available day-to-day to monitor development over time.</p>
<p>Then, some bugfixes and backports later, we’re finally there: OGC tests are green on the development version, 3.12 and 3.10 releases. Yippee!</p>
<p align="center"><img src="https://www.qcooperative.net/images/blog/ogcapif/green.png" alt="alt wording" /></p>
<h2 id="conclusion">Conclusion</h2>
<p>Now that everything is in order, the last step is to start the formal OGC certification process. From now on, the dedicated QGIS OGC Team takes care of further operations.</p>
<div class="social-share pt-4">
<h4></h4>
</div>
