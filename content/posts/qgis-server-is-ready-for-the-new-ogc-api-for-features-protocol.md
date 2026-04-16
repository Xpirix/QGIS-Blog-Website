---
title: "QGIS Server is ready for the new OGC API for Features protocol."
date: "2019-11-26T22:21:55+00:00"
draft: false
authors: ["neumannandreas"]
categories: ["QGIS Server"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>The new <a href="http://docs.opengeospatial.org/is/17-069r3/17-069r3.html">OGC API for Features (OAPIF)</a> (also formerly known as WFS3) is one of the first protocols of the new generation of OGC web services and we are happy to announce that QGIS Server is ready to serve data following the specifications of this new protocol.</p>
<p>A lot of work has been going on during last summer to make sure QGIS Server was ready to support the new family of REST APIs, the underlying architecture allows in fact to expand QGIS Server API capabilities with any kind of new API that will be available in the future.</p>
<p>The new API is very similar to the well known WFS, but it also comes with a distinct set of features like content negotiations, REST actions, HTML templates, JSON as a first class citizen, self-documentation of the API (following OpenAPI specifications) and a preliminary implementation (the specifications are not yet finalized) of the simple transactions.</p>
<p>The new API is already in the <a href="https://docs.qgis.org/testing/en/docs/user_manual/working_with_ogc/server/services.html#wfs3-ogc-api-features">QGIS Server documentation</a>, it only misses the transaction part because the specifications are not yet final and we don&#8217;t want people start relying on an API that is probably going to change quite soon.</p>
<p>The vast majority of this new development has been possible thanks to the volunteer work of our core developers but we also wish to thank <a href="https://www.osgeo.org/">OSGeo</a> and <a href="https://www.qgis.org/en/site/about/sustaining_members.html">QGIS sustaining members and donors</a> for funding a substantial part of the following activities:</p>
<div>
<div></div>
<div>
<table dir="ltr" border="1" cellspacing="0" cellpadding="0">
<colgroup>
<col width="322" /></colgroup>
<tbody>
<tr>
<td>OPENAPI validation (completed)</td>
</tr>
<tr>
<td>Online demo (TODO)</td>
</tr>
<tr>
<td>CI validation/ OGC CITE (started)</td>
</tr>
<tr>
<td>Expose Schema (completed)</td>
</tr>
<tr>
<td>Simple Transactions (completed)</td>
</tr>
<tr>
<td>Returned fields filter (completed)</td>
</tr>
<tr>
<td>Documentation (completed except for transactions)</td>
</tr>
<tr>
<td>JSON performance comparison with WFS (TODO)</td>
</tr>
<tr>
<td>Time filter support (completed)</td>
</tr>
</tbody>
</table>
</div>
<p>Enjoy the new API and beware that this is only the first of a brand new series of OGC APIs that will make much easier for users to interact with data and for developers to create applications that consume those data.</p>
</div>
<div></div>
<p>Text provided by Alessandro Pasotti (QGIS core developer)</p>
