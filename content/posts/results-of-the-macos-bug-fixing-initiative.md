---
title: "Results of the MacOS bug fixing initiative"
date: "2018-11-19T20:24:44+00:00"
draft: false
authors: ["neumannandreas"]
categories: ["Uncategorized"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>Thanks to your donations, we were able to hire core developers to focus on solving Mac OS specific issues for QGIS. More than 30 MacOS QGIS users donated a little more than 3000 € for this bug fixing round.</p>
<p>After an effort of triage and testing, here is what has been achieved:</p>
<ul>
<li>The <strong>map canvas is now in HiDPI</strong> (<a href="https://issues.qgis.org/issues/17773">https://issues.qgis.org/issues/17773</a>).<br />
The issue was that Mac OS handles differently high DPI scaling by providing a scaling ration to scale graphics output. For more information, read <a href="http://doc.qt.io/qt-5/scalability.html#high-dpi-scaling-on-macos-and-ios">http://doc.qt.io/qt-5/scalability.html#high-dpi-scaling-on-macos-and-ios</a> and for even more info <a href="http://doc.qt.io/qt-5/qpainter.html#drawing-high-resolution-versions-of-pixmaps-and-images">http://doc.qt.io/qt-5/qpainter.html#drawing-high-resolution-versions-of-pixmaps-and-images</a>. You may not have noticed, but the scale shown under the canvas was wrong in former QGIS 3.x versions. It has been fixed too.</li>
<li><strong>Zooming with trackpad is now fluent</strong> (<a href="https://issues.qgis.org/issues/18418">https://issues.qgis.org/issues/18418</a>) The track pad is apparently sending more events than the scrolling and are now discarded to avoid scale jumps.</li>
<li><strong>Size of mouse cursors with map tools has been fixed</strong> (<a href="https://issues.qgis.org/issues/19092">https://issues.qgis.org/issues/19092</a>). The scaling previously introduced could be removed thanks to the HiDPI fixes, and this has fixed by the same occasion the active point of the cursor being misplaced.</li>
<li>The <strong>size of the map canvas at startup</strong> was not an issue in QGIS in itself and has been fixed by upgrading to a newer Qt version (<a href="https://issues.qgis.org/issues/19524">https://issues.qgis.org/issues/19524</a>)</li>
<li><strong>Rendering slowness issue</strong> *should* also have been fixed by an upgrade of Qt version (<a href="https://issues.qgis.org/issues/19546">https://issues.qgis.org/issues/19546</a>)</li>
<li>At the moment, the &#8220;default&#8221; theme of QGIS (as opposed to the &#8220;Night Mapping&#8221; theme), has a few glitches when used in Mojave with &#8220;Dark&#8221; theme activated. Mainly text in widgets cannot be read since they are white on white. This is a Qt issue (<a href="https://bugreports.qt.io/browse/QTBUG-68891">https://bugreports.qt.io/browse/QTBUG-68891</a>) and the upcoming Qt 5.12 released by the end of november should fix it. In the mean time, the QGIS &#8220;Night Mapping&#8221; theme is automatically applied when running on Mojave with Dark theme. While the theme is probably not perfect, it allows to work properly and the situation will be evaluated again when Qt 5.12 is released.</li>
</ul>
<p>Unfortunately, some issues remain. Mainly, the <strong>text being rendered as outlines in PDF export</strong> (<a href="https://issues.qgis.org/issues/3975">https://issues.qgis.org/issues/3975</a>) remains for now. It might be fixed in a following effort.</p>
<p>Thanks to all donors who helped in this effort and to Denis Rouzaud as a core developer who spent a lot of time investigating and fixing these issues!</p>
