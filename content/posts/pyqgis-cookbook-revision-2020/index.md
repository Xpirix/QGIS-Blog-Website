---
title: "PyQGIS Cookbook revision 2020"
date: "2020-04-19T16:48:40+00:00"
draft: false
authors: ["underdark"]
categories: ["QGIS Documentation"]
tags: ["documentation", "PyQGIS"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>We are happy to announce that the <a href="https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/">PyQGIS Cookbook</a> has received a complete overhaul and is now better than ever.</p>
<p>The PyQGIS Cookbook is a great source of information, not only for PyQGIS beginners or plugin developers, but also for C++ developers: it contains a lot of information about the internals of the QGIS API that you cannot really find anywhere else.</p>
<p>The main point addressed in this review were:</p>
<ol>
<li>All the code snippets have been reviewed and put under automated test in CI. Before this revision, there were 62 tests. Now there are over 300 tested snippets. </li>
<li>A few snippets had to be updated because of changes in the QGIS API or because of the deprecation of methods (CRS handling in particular due to the proj6 switch).</li>
<li>Textual descriptions have been edited to update the contents where the API has substantially changed.</li>
<li>The material covering Python for QGIS Server has been reorganized and now includes new snippets and introductory texts about the new modules and OGC APIs architecture.</li>
</ol>
<p>For the full summary, please refer to <a href="https://lists.osgeo.org/pipermail/qgis-psc/2020-April/008491.html">Alessandro Pasotti&#8217;s report on the PSC mailing list</a>. </p>
<p>Thank you to Alessandro Pasotti for taking on this project and thank you to all our sponsor and donors who make this initiative possible!</p>
