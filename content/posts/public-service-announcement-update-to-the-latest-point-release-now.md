---
title: "Public Service Announcement: Update to the latest point release now"
date: "2020-01-24T08:50:29+00:00"
draft: false
authors: ["underdark"]
categories: ["Uncategorized"]
tags: ["release"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>QGIS users who have adopted the 3.10 version when initially released at the end of October 2019 have likely noticed a sharp drop in reliability. The underlying issues have now been addressed in 3.10.2, all users are advised to update *now*.</p>
<p>When QGIS 3.10 was first released in the end of October 2019, a pair of libraries – namely GDAL and PROJ – were updated to their next-generation versions. The advantages are plenty: GeoPDF export[1] support, more accurate coordinate transformation, etc. For those interested, more technical information on this is available here[2].</p>
<p>The update of these crucial libraries led to a number of regressions. While we expected some issues to arise, the seriousness of the disruption caught us off guard. Yet, it was also somewhat inevitable: QGIS is the first large GIS project to expose these next-generation libraries to the masses. The large number of QGIS users across the globe were essentially stress testing both new code within QGIS as well as the libraries themselves.</p>
<p>Thanks to dedicated users taking time to file in report and the community helping out as well as our project sponsors for allowing us to fund development time, developers have been able to fix all known regressions in both in QGIS as well as underlying GDAL and PROJ libraries, benefiting a large number of open source projects.</p>
<p>As a result of this collective effort by the community, QGIS 3.10.2 is now back to being the reliable and stable GIS software we all love. As such, we cannot stress enough the importance of updating now.</p>
<p>Once again, thanks to our community of testers, sponsors, and developers for their countless hours and efforts in making QGIS better.</p>
<p>Happy mapping!</p>
<p>[1] <a href="https://north-road.com/2019/09/03/qgis-3-10-loves-geopdf/" target="_blank" rel="noopener">https://north-road.com/2019/09/03/qgis-3-10-loves-geopdf/</a><br />
[2] <a href="https://gdalbarn.com/" target="_blank" rel="noopener">https://gdalbarn.com/</a></p>
