---
title: "Your donations/sponsorships help to maintain and improve the quality of QGIS"
date: "2015-11-09T19:51:40+00:00"
draft: false
authors: ["neumannandreas"]
categories: ["Uncategorized"]
---

<p>The QGIS project is growing in size, number of contributors/contributions and code complexity. This introduces challenges for the project, especially for maintaining quality. Maintaining and improving quality is one of the main concerns of the QGIS.ORG board and some core developers.</p>
<p><strong>Past and current QA efforts</strong></p>
<p>Tim Sutton introduced a first unit test framework several years ago. But it wasn&#8217;t very visible then and passing the tests as a prerequisite to make changes to master wasn&#8217;t enforced. About a year ago, Matthias Kuhn introduced automated unit testing for the Linux builds &#8211; using <a href="https://travis-ci.org/">Travis continuous integration testing</a>. At our <a href="https://github.com/qgis/QGIS">github page</a> you can always see whether the master version builds fine and whether the tests are passing &#8211; see the green &#8220;Build passing&#8221; button at the beginning of the Readme.md file.</p>
<p>Since then, OS X automated building/testing was added. Pull requests (new contributions from developers) can be tested prior to integration into the master branch. Another effort was to use <a href="https://scan.coverity.com/">coverity code scans</a> to detect memory leaks. Nyall Dawson and others did a lot of improvements/fixes due to this automated code scans.</p>
<p><strong>Upcoming challenges</strong></p>
<p>There is still a lot to do regarding quality and automated testing. Because continuous integration tests were only introduced about a year ago, it means that still a lot of areas in the code base remain untested. Also, the current unit tests do not test GUI interactions. There is an <a href="https://github.com/qgis/QGIS-Enhancement-Proposals/issues/30">ongoing discussion</a> if critical classes should have unit tests enforced for any code changes. Finally, our bug queue at <a href="http://hub.qgis.org/projects/quantum-gis/issues">http://hub.qgis.org/projects/quantum-gis/issues</a> is still quite long, with lots of bigger and minor issues.</p>
<p><strong>Your financial support really matters!</strong></p>
<p>This is where your donations and sponsorships come in. For the past 3-4 releases we were able to pay 2-4 developers who worked for several days concentrating on bug fixing. For QGIS 2.12 we had Nyall Dawson, Jürgen Fischer and Larry Shaffer working on bug fixing. We also financially support Giovanni Manghi for working on our <a href="http://hub.qgis.org/issues">bug tracker</a> (e.g. classifying issues correctly, trying to reproduce the issue, ask bug reporters for more details).</p>
<p>Now &#8211; you may wonder why they didn&#8217;t fix all the &#8220;BLOCKER&#8221;s first and then continue on with &#8220;HIGH&#8221;, &#8220;NORMAL&#8221; &#8220;LOW&#8221;  issues &#8211; and why a lot of unreported issues and issues with label &#8220;LOW&#8221; were also fixed? The answer is that it is often more efficient for the developers to concentrate on a certain part of the code &#8211; e.g. concentrating on geometry, labeling and editing issues, as Nyall did for this round of bug fixing. This means that he would not only fix issues labeled as &#8220;BLOCKER&#8221; or &#8220;HIGH&#8221; but also other bugs that are in the same code. Finally, not all of the &#8220;Blocker&#8221; and &#8220;High&#8221; bugs are reproducable or the issue may be much too hard/time consuming to fix.</p>
<p>Due to your financial support, the 3 developers were able to fix the following list of issues for the QGIS 2.12 release &#8211; many of the fixes also get back-ported to QGIS 2.8 LTS release:</p>
<ul>
<li>Sweep of all changed dialogs, ensuring tab order is correct</li>
<li>UNREPORTED: Only save effect element if it is non-default (decreases size of qgs project files)</li>
<li>HIGH: Fix map rotation not considered for ellipse marker data defined rotation (<a href="http://hub.qgis.org/issues/13367">#13367</a>)</li>
<li>HIGH: Maintain order of recent expressions (<a href="http://hub.qgis.org/issues/13461">#13461</a>)</li>
<li>NORMAL: Make sure recent expression group is always listed last (<a href="http://hub.qgis.org/issues/13462">#13462</a>)</li>
<li>NORMAL: [diagrams] Fix initial value of transparency slider not set (<a href="http://hub.qgis.org/issues/13434">#13434</a>)</li>
<li>UNREPORTED: Fix potential crashes in renderer widgets</li>
<li>NORMAL: Fix legends are empty if presets used with filtered legend (<a href="http://hub.qgis.org/issues/13300">#13300</a>)</li>
<li>UNREPORTED: Fix crashes and inconsistent ui when atlas is set to a geometryless layer</li>
<li>BLOCKER: Fix diagrams are always shown, regardless of setting (<a href="http://hub.qgis.org/issues/13501">#13501</a>)</li>
<li>BLOCKER: Fix fill ring tool used with advanced digitising crashes QGIS (<a href="http://hub.qgis.org/issues/13355">#13355</a>)</li>
<li>NORMAL: Fix add ring/fill ring tool works on first polygon (<a href="http://hub.qgis.org/issues/13069">#13069</a>)</li>
<li>BLOCKER: Fix missing sip bindings for renderers (<a href="http://hub.qgis.org/issues/13545">#13545</a>)</li>
<li>BLOCKER: Fix crash in label property dialog (<a href="http://hub.qgis.org/issues/13543">#13543</a>)</li>
<li>NORMAL: Fix hardcoded border for raster legend items (<a href="http://hub.qgis.org/issues/13540">#13540</a>)</li>
<li>BLOCKER: Fix symbols drawn multiple times in rule based renderer if symbol (<a href="http://hub.qgis.org/issues/13220">#13220</a>)</li>
<li>BLOCKER: Use a model for node editor table, fixed hang when node tool used on large feature (<a href="http://hub.qgis.org/issues/13541">#13541</a>)</li>
<li>BLOCKER: Fix node tool duplicates nodes when topological editing and snap are both enabled (<a href="http://hub.qgis.org/issues/13466">#13466</a>)</li>
<li>NORMAL: Fix broken data defined SVG marker outline width (<a href="http://hub.qgis.org/issues/13423">#13423</a>)</li>
<li>HIGH: Scale svg marker outline width to match context (<a href="http://hub.qgis.org/issues/11522">#11522</a>)</li>
<li>HIGH: Allow coloring of svg markers and svg fills when used with graduated/categorised renderers (<a href="http://hub.qgis.org/issues/11658">#11658</a>)</li>
<li>HIGH: Fix svg outline widths are incorrectly scaled (<a href="http://hub.qgis.org/issues/11522">#11522</a>)</li>
<li>UNREPORTED: Fix snapping options dialog not correctly initialised when loading projects</li>
<li>UNREPORTED: Fix uninitialized variables in advanced digitizing dock which meant that sometimes advanced digitising tools would be activated unexpectedly</li>
<li>NORMAL: Fix curved labels ignore line orientation placement flag (<a href="http://hub.qgis.org/issues/5778">#5778</a>)</li>
<li>UNREPORTED: [console] Move run button earlier in console editor toolbar (prevents it being hidden in overflow menu on small screens)</li>
<li>UNREPORTED: Fix fill and outline color for svg markers sometimes enabled even though SVG file does not support parameters</li>
<li>UNREPORTED: Fix svg marker colors not correctly restored from project</li>
<li>UNREPORTED: If svg files with params do not have a default value set, then don&#8217;t reset the fill/border color and border width when changing svg marker/svg fill SVG files (made the behaviour consistent between the svg marker and the other marker symbols)</li>
<li>NORMAL: Fix svg symbols are shown in white and hard to see in svg picker (<a href="http://hub.qgis.org/issues/10908">#10908</a>)</li>
<li>NORMAL: Fix refining rule based renderer using expression (<a href="http://hub.qgis.org/issues/10815">#10815</a>)</li>
<li>UNREPORTED: Fix crash when changing symbol types on windows</li>
<li>BLOCKER: Fix split parts tool only leaves one of the newly created parts (<a href="http://hub.qgis.org/issues/13421">#13421</a>)</li>
<li>BLOCKER: Fix using add part tool to add part to geometryless rows (<a href="http://hub.qgis.org/issues/12885">#12885</a>, <a href="http://hub.qgis.org/issues/11319">#11319</a>)</li>
<li>UNREPORTED: Fix some potential crashes with edit tools and null geometry</li>
<li>UNREPORTED (thought I&#8217;d submitted this years ago but can&#8217;t find the issue now): Allow adding features with empty geometry via attribute table</li>
<li>HIGH: Allow delete part tool to remove geometry from single type point and line layers (<a href="http://hub.qgis.org/issues/13258">#13258</a>)</li>
<li>LOW: Fix overview canvas background color not set (<a href="http://hub.qgis.org/issues/11157">#11157</a>)</li>
<li>Add some unit tests for QgsWKBTypes</li>
<li>NORMAL: When adding ring to a geometry, add z or m dimensions to the ring geometry if required (<a href="http://hub.qgis.org/issues/7400">#7400</a>, <a href="http://hub.qgis.org/issues/7401">#7401</a>)</li>
<li>NORMAL: Also show features with modified geometry when &#8220;show edited and new features&#8221; filter is active in attribute dialog (<a href="http://hub.qgis.org/issues/11684">#11684</a>)</li>
<li>BLOCKER: Fix broken apply button in label config dialog (<a href="http://hub.qgis.org/issues/13543">#13543</a>)</li>
<li>BLOCKER: Fix area calculation when OTF active and no ellipsoid, add unit test (<a href="http://hub.qgis.org/issues/13601">#13601</a>)</li>
<li>UNREPORTED: Fix exporting geometry collections to WKT would result in invalid WKT</li>
<li>UNREPORTED: Fix unable to import WKT using MultiPoint(1 1,2 2,&#8230;) format</li>
<li>UNREPORTED: Fix GeometryCollection WKT to support collections with multi* children and GeometryCollection children (allowed by spec)</li>
<li>Add a bunch of unit tests to geometry<br />
&#8211; UNREPORTED: Fix calculation of area and length of mixed geometry collections</li>
<li>UNREPORTED: Fix geometry casting in python bindings (missing MultiLineString and GeometryCollection casts)</li>
<li>UNREPORTED: Fix calculation of length/perimeter for geometry collections</li>
<li>UNREPORTED: when creating geometry from WKT, upgrade dimensionality of geometry if coordinates are 3/4 dimensional</li>
<li>UNREPORTED: match dimensionality of collections to child dimensionality</li>
<li>UNREPORTED: fix area of curves was non-zero if curve is closed</li>
<li>UNREPORTED: don&#8217;t consider m values when testing for curve closedness</li>
<li>NORMAL: Fix merge attributes tool sets skipped attributes to null (<a href="http://hub.qgis.org/issues/13231">#13231</a>)</li>
<li>NORMAL: Add skip all option to merge attributes dialog (<a href="http://hub.qgis.org/issues/6958">#6958</a>)</li>
<li>UNREPORTED: Fix QgsStatisticalSummary sometimes returning 0 for StDevSample stat</li>
<li>UNREPORTED: Fix storing string representations of doubles in an int field results in NULL rather than converting value to int</li>
<li>NORMAL: Fix merge attributes/features tool resets values to null for int fields and add a warning if merged attribute value is not compatible with field type (<a href="http://hub.qgis.org/issues/12842">#12842</a>)</li>
<li>Fix a LOT of leaks relating to geometry and GEOS operations, labeling</li>
<li>UNREPORTED: [pal] Fix regression in placement for free/horizontal polygon labels</li>
<li>Add tooltips to advanced digitizing dock</li>
<li>Fix a crash in filtered legends</li>
<li>Reviewed and merged several bug fix PRs</li>
<li><a href="http://hub.qgis.org/issues/13433">#13433</a>: Help text for rpad and lpad in field calculator are mixed up</li>
<li><a href="http://hub.qgis.org/issues/13417">#13417</a>: missing libqgis_app.so</li>
<li><a href="http://hub.qgis.org/issues/13420">#13420</a>: Strange behaviour of newly &#8216;saved as&#8217; project</li>
<li><a href="http://hub.qgis.org/issues/13463">#13463</a>: Identify Results panel always show newly created features in the list</li>
<li><a href="http://hub.qgis.org/issues/13538">#13538</a>: PostGIS tables containing MultiPolygonZ crash QGIS master</li>
<li><a href="http://hub.qgis.org/issues/13546">#13546</a>: qgis trying to update first empty text row with null in db</li>
<li><a href="http://hub.qgis.org/issues/13027">#13027</a>: Join by location does not work when layers have equivalent field names</li>
<li><a href="http://hub.qgis.org/issues/13032">#13032</a>: Save as&#8230; fails to populate fields if layer has similar names only different by case</li>
<li><a href="http://hub.qgis.org/issues/13052">#13052</a>: Problem with reshape</li>
<li><a href="http://hub.qgis.org/issues/10747">#10747</a>: Cannot copy/paste points features</li>
<li><a href="http://hub.qgis.org/issues/13506">#13506</a>: Processing help files for QGIS algs all dead now</li>
<li><a href="http://hub.qgis.org/issues/">#13274</a>: API combine method for geometry</li>
<li><a href="http://hub.qgis.org/issues/11755">#11755</a>: Real precision (Shapefile)</li>
<li><a href="http://hub.qgis.org/issues/9208">#9208</a>: QGIS crashes when using addAttributes on any vector data provider</li>
<li><a href="http://hub.qgis.org/issues/13579">#13579</a>: Crash Dump 2.11 with user defined expressions</li>
<li><a href="http://hub.qgis.org/issues/10515">#10515</a>: QGIS Crash when trying to load a point layer to georss file</li>
<li><a href="http://hub.qgis.org/issues/11276">#11276</a>: Setting radius units to meters produces incorrect results</li>
<li><a href="http://hub.qgis.org/issues/13641">#13641</a>: editing a feature in a PostGIS layer does not work when the PK contains NULLs</li>
<li><a href="http://hub.qgis.org/issues/13631">#13631</a>: when ELSE rule exists in Styling, all Labels are rendered regardless of styling groups being active/inactive</li>
<li><a href="http://hub.qgis.org/issues/13638">#13638</a>: Cannot load emptry Postgis views</li>
<li><a href="http://hub.qgis.org/issues/8255">#8255</a>: in edit mode changing primary key discards geometry modifications</li>
<li><a href="http://hub.qgis.org/issues/13594">#13594</a>: DB Manager &#8211; unable to add a Postgres/PostGIS raster as layer</li>
<li><a href="http://hub.qgis.org/issues/13446">#13446</a>: MYSQL Project File</li>
<li><a href="http://hub.qgis.org/issues/13310">#13310</a>: nightly build packages failing to install with grass error</li>
<li>(<a href="https://github.com/qgis/QGIS/pull/2378">PR#2378</a>: Allow postgis layers from queries to have multiple column primary keys)</li>
<li>(<a href="https://github.com/qgis/QGIS/pull/2376">PR#2376</a>: the test for uniqueness now also works for multiple columns by SebDieBln)</li>
<li>(<a href="http://hub.qgis.org/issues/13645">#13645</a>: ftools &#8220;line intersection&#8221; crashes qgis)</li>
<li>(<a href="http://hub.qgis.org/issues/13646">#13646</a>: Merge shapefiles from fTools crashes QGIS)</li>
<li>transifex updates &amp; german translation</li>
<li>attribute editing: don&#8217;t allow editing without ChangeAttributeValues capability</li>
<li>vector layer: avoid some crashs when methods are called on invalid layers</li>
<li>oracle provider: fix call of sdo_filter to verify a spatial index is present</li>
<li><a href="http://hub.qgis.org/issues/13641">#13641</a>: postgres provider: verify unique constraint if NOT NULL is not set on key columns (shortly after release)</li>
<li>Commit <a href="https://github.com/qgis/QGIS/commit/6a4544f">6a4544f</a> fix fetching of redirected wms capabilities (followup e95bf6d)</li>
</ul>
