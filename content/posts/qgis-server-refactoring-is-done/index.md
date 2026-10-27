---
title: "QGIS Server refactoring is done!"
date: "2017-10-29T22:31:10+00:00"
draft: false
authors: ["underdark"]
categories: ["QGIS Server"]
tags: ["QGIS Server"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>As you may know, QGIS is jumping to a new major version. (Yes!) Doing so was made necessary because of the need to switch to Python 3, Qt5, but also because <a href="http://blog.qgis.org/2016/02/10/qgis-3-0-plans/">we needed to break the QGIS API in several places</a>.</p>
<p>A year ago there was an appeal on the QGIS developer mailing list about the strong need for love that the QGIS server code base required. Indeed, the API was locked by some old methods of QGIS server. In short, QGIS server was reparsing the .qgs project file in its own way, and created dependencies to parts of QGIS we needed to drop.</p>
<p>As outsourcing the server code base was not an option, so we had to refactor it. The involved parties decided to get engaged in a <a href="https://github.com/qgis/QGIS/wiki/QGIS3---QGIS-Server-code-sprint-Notes">code sprint</a> in the city of Lyon , France dedicated to sharing their vision, planning the work and finally making all the <a href="https://github.com/qgis/QGIS-Enhancement-Proposals/issues/74">following</a> happen:</p>
<p><b>Higher level refactoring</b></p>
<p>All services (WMS GetMap, WFS GetFeature, GetLegendGraphics, WCS, GetPrint etc..) have been rewritten. Some like WMS were entirely rewritten. Kudos to the devs!</p>
<p><b>New features</b></p>
<ul>
<li><a href="https://github.com/qgis/QGIS/pull/3886">Multi-thread rendering</a> like in the desktop</li>
<li>A new option to <a href="https://github.com/qgis/QGIS/pull/5094">trust layer metadata</a> and thus speed up project loading</li>
<li>WFS 1.1 support <a href="https://github.com/qgis/QGIS/pull/5297">https://github.com/qgis/QGIS/pull/5297</a></li>
<li>Full Python bindings for the server API</li>
<li>Server services as plugins like providers</li>
</ul>
<p><b>Deep, complex and unrewarding tasks</b></p>
<ul>
<li>Remove all singleton calls</li>
<li>Cut all the dependencies to the old QGIS project file parser</li>
<li>Minimize dependencies to GUI library. Since fonts are necessary to render maps, totally removing them was not feasible.</li>
</ul>
<p><b>Infrastructure tasks</b></p>
<ul>
<li><a href="http://oslandia.com/en/2017/06/16/qgis-server-ogc-cite-compliance-testing/">Build a OGC compliancy platform</a> and integrate it to a continuous integration platform. Conformity reports are now pushed to <a href="http://tests.qgis.org/">tests.qgis.org</a></li>
<li>Add unit tests &#8230; and again more unit tests</li>
<li><a href="http://oslandia.com/en/2017/06/14/qgis-server-security-aspect/">Stress QGIS server against security leaks</a> (SQL injections and other malicious attacks)</li>
<li>Start profiling and bench marking performances. This work still needs some love &#8211; and funding &#8211; to be achieved</li>
</ul>
<p>Additionally, some of these new developments have already been <a href="https://git.osgeo.org/gogs/foss4g-europe/foss4g-europe-2017-paris/src/master/presentations/2017-07-20/general_track/foss4g-europe-2017-QGIS_3_Refactoring_and_enhancement-DMarteau-PBlottiere.pdf">presented</a> at FOSS4G-EU in July.</p>
<p><b>Congratulations</b> to the developers who worked hard on this!</p>
<p>Now this deserves to be well tested, please report back any issues!</p>
