---
title: "🎉 Changes Ahead: QGIS Is Moving to Qt6 and Launching QGIS 4.0!"
date: "2025-04-17T07:17:00+00:00"
draft: false
authors: ["mbernasocchi"]
categories: ["Public Service Announcement", "QGIS Board"]
featured_image: "/wp-content/uploads/2025/10/blog-qgis40-soon.png"
---

<p class="wp-block-paragraph">We’re happy to share some major updates coming to the QGIS platform over the next few months. These changes are part of a long-planned technical migration that will bring new possibilities and ensure QGIS stays modern, fast, and future-ready.</p>



<h3 class="wp-block-heading">🚀 QGIS Is Migrating to Qt6</h3>



<p class="wp-block-paragraph">Qt6 is the latest version of the cross-platform application framework that QGIS is built upon. Moving to Qt6 allows us to:</p>



<ul class="wp-block-list">
<li>Future-proof the QGIS codebase.</li>



<li>Take advantage of modern libraries with significant performance and security improvements.</li>



<li>Simplify long-term maintenance and development.</li>
</ul>



<p class="wp-block-paragraph">While most of the migration is complete, a few final tasks remain, especially around Continuous Integration (the automated processes that run on each change to the QGIS code base to help reduce bugs), layout rendering, and PDF output. The core team is actively working on these and making significant progress.</p>



<h3 class="wp-block-heading">🌟 Enter QGIS 4.0</h3>



<p class="wp-block-paragraph">To mark this significant backend shift, we’ve decided to align the Qt6 migration with a new major release: <strong>QGIS 4.0</strong>, which will arrive after <strong>QGIS 3.44</strong>, in <strong>October 2025</strong>.</p>



<p class="wp-block-paragraph">Here’s what you need to know:</p>



<ul class="wp-block-list">
<li><strong>QGIS 4.0 will be Qt6-only</strong></li>



<li>It <strong>will not</strong> be an LTR (see release strategy below for details)</li>



<li>To ease the transition, it <strong>will retain deprecated APIs</strong>, so plugin developers will only need minimal work to ensure compatibility with Qt6 and prepare for future QGIS versions.</li>
</ul>



<p class="wp-block-paragraph">This strategy allows us to modernise QGIS without forcing a major rewrite of existing plugins. Some adjustments will be needed to ensure QGIS 4.0 compatibility.</p>



<p class="wp-block-paragraph"><strong>Note on Features:</strong> While QGIS 4.0 marks a major version jump, it’s essential to understand that this release will include only a few new user-facing features. The primary focus is on the transition to Qt6, which involves significant changes under the hood. <br>In the QGIS project, a major version number doesn&#8217;t necessarily mean a flood of new features—it signals a break in the API. This ensures that developers are aware of potential compatibility updates needed for their plugins or integrations, even if the visible functionality remains largely unchanged.</p>



<h3 class="wp-block-heading">💡 Why This Matters</h3>



<p class="wp-block-paragraph">This isn’t just about upgrading for the sake of it — it’s about keeping QGIS secure, modern, and maintainable.</p>



<ul class="wp-block-list">
<li><strong>Qt 5.15 enters Extended Support (EOS)</strong> in <strong>May 2025</strong>, with continued security updates available only under commercial terms</li>



<li>Staying on Qt5 would limit our ability to access upstream fixes and improvements</li>



<li><strong>Qt6 is already a proven platform</strong> — projects like <strong>QField</strong> and <strong>Mergin Maps</strong> have been using it successfully in production for quite some time</li>



<li>Migrating to Qt6 ensures QGIS stays aligned with a supported, modern framework</li>
</ul>



<h3 class="wp-block-heading">📆 Release Strategy</h3>



<p class="wp-block-paragraph">To ensure a smooth transition for users and developers, we’re taking a phased approach:</p>



<ul class="wp-block-list">
<li><strong>QGIS 3.40 LTR</strong> will be extended by <strong>4 months</strong>, until <strong>May 2026</strong>, giving plugin developers and organisations extra time to adapt</li>



<li><strong>QGIS 4.0</strong>, scheduled for <strong>October 2025</strong>, will be a regular release</li>



<li><strong>QGIS 4.2</strong>, scheduled for <strong>February 2026</strong>, will follow as the next <strong>official LTR</strong></li>
</ul>



<p class="wp-block-paragraph">This gradual rollout ensures users who depend on stable environments can continue with 3.40 LTR, while early adopters and plugin developers move forward with Qt6 in 4.0.</p>



<h3 class="wp-block-heading">🔌 What About Plugins?</h3>



<p class="wp-block-paragraph">We’re making it easier than ever for plugin developers to prepare:</p>



<ul class="wp-block-list">
<li>The QGIS Plugin Repository will begin accepting <strong>4.x-compatible plugins</strong></li>



<li>The plugin site will <strong>inform users if a plugin is Qt6-compatible</strong></li>



<li>A comprehensive <strong>migration guide</strong> is in the works to support developers during the transition</li>
</ul>



<p class="wp-block-paragraph">If you maintain a plugin, now’s the perfect time to start testing and preparing for Qt6 compatibility!<br>👉 See:</p>



<ul class="wp-block-list">
<li><a href="https://github.com/qgis/pyqgis4-checker">pyqgis4-checker</a></li>



<li><a href="https://github.com/qgis/QGIS/wiki/Plugin-migration-to-be-compatible-with-Qt5-and-Qt6">Plugin migration guide</a></li>
</ul>



<h3 class="wp-block-heading">🧪 Try Qt6 Today</h3>



<p class="wp-block-paragraph">The migration to Qt6 isn’t just theoretical — it’s already happening and ready for testing:</p>



<ul class="wp-block-list">
<li><strong>Windows</strong>: Qt6 builds of <strong>all release branches and master</strong> are available now via the <a href="https://trac.osgeo.org/osgeo4w/">OSGeo4W installer</a></li>



<li><strong>Linux (Debian)</strong>: Qt6 support is <strong>almost there</strong> — packaging work is underway to support <strong>both Qt5 and Qt6</strong> side by side</li>



<li><strong>macOS</strong>: Qt6 packages will start building as soon as <strong>QGIS 3.44.0 is released</strong> and the <strong>QGIS 4.0 development cycle begins</strong></li>
</ul>



<p class="wp-block-paragraph">Start exploring Qt6 builds today and help us shape the future of QGIS.</p>



<h3 class="wp-block-heading">🤝 Get Involved</h3>



<p class="wp-block-paragraph">We’ll share more updates in the coming weeks. In the meantime:</p>



<ul class="wp-block-list">
<li>Try the Qt6 builds</li>



<li>Test your plugins for compatibility</li>



<li>Stay tuned on <a href="https://qgis.org">qgis.org</a> and community channels</li>
</ul>



<p class="wp-block-paragraph">A massive thank you to all contributors, developers, testers, and organisations supporting this transition.<br><strong>QGIS 4.0 is shaping to be a big leap forward, and we can’t wait to share it with you!</strong></p>



<pre class="wp-block-preformatted"><br>Edited on 24.04.25<br>- Removed leftover texts<br>- Added a note on new features in QGIS 4.0<br></pre>
