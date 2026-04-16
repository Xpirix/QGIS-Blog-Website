---
title: "Reports from the winning grant proposals 2017"
date: "2018-05-08T19:45:24+00:00"
draft: false
authors: ["underdark"]
categories: ["QGIS Grant Programme"]
tags: ["grants"]
featured_image: "/wp-content/uploads/2017/01/qgis-icon_60px.png"
---

<p>While we are waiting for this year&#8217;s grant proposals to come in, it is time to look back at last year&#8217;s winning proposals and their results. These are the reports on the work that has been done within the individual projects:</p>
<h3>QGIS 3D &#8211; Martin Dobias</h3>
<p><a href="/wp-content/uploads/2018/05/qgis3d.jpg"><img loading="lazy" data-attachment-id="1974" data-permalink="http://blog.qgis.org/2018/05/08/reports-from-the-winning-grant-proposals-2017/qgis3d/" data-orig-file="/wp-content/uploads/2018/05/qgis3d.jpg" data-orig-size="2048,1084" data-comments-opened="0" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;}" data-image-title="qgis3d" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2018/05/qgis3d.jpg" class="alignnone size-large wp-image-1974" src="/wp-content/uploads/2018/05/qgis3d.jpg" alt="" width="780" height="413" srcset="/wp-content/uploads/2018/05/qgis3d.jpg 780w, /wp-content/uploads/2018/05/qgis3d.jpg 1560w, /wp-content/uploads/2018/05/qgis3d.jpg 150w, /wp-content/uploads/2018/05/qgis3d.jpg 300w, /wp-content/uploads/2018/05/qgis3d.jpg 768w, /wp-content/uploads/2018/05/qgis3d.jpg 1024w, /wp-content/uploads/2018/05/qgis3d.jpg 1440w" sizes="(max-width: 780px) 100vw, 780px" /></a></p>
<p>Results are included in the QGIS 3.0 release. As proposed in the grant, a new 3D map view has been added together with GUI for easy configuration of 3D rendering. The 3D view displays terrain (either from a DEM raster layer or a simple flat area) with 2D map rendered on top of the terrain. In addition to that, vector layers can be rendered as true 3D entities: points may be visualized as simple geometric shapes or as 3D models (loaded from a file), polygons and linestrings are tessellated into 3D geometries. 2D polygons can be turned into 3D objects using extrusion, possibly with data-defined height &#8211; an easy way how to display buildings, for example. Data with 3D coordinates have the Z values in geometries respected. Although the 3D view is still in its early stages, it is already usable for many use cases. Hopefully this functionality will help to attract even more users to QGIS!</p>
<p>More details: <a href="https://github.com/qgis/QGIS-Enhancement-Proposals/issues/105" rel="nofollow">https://github.com/qgis/QGIS-Enhancement-Proposals/issues/105</a></p>
<h3>Improvements to relations &#8211; Régis Haubourg</h3>
<p>Various improvements for deep relations with PostgreSQL were successfully added in QGIS 3.0:</p>
<ul>
<li>CTRL+Z is back in transaction group editing ! We restored the UNDO/REDO feature and all edits are temporarily saved inside PostgreSQL SAVEPOINTS. For more details, please jump here <a href="http://oslandia.com/en/2017/10/10/undo-redo-stack-is-back-qgis-transaction-groups/" rel="nofollow">http://oslandia.com/en/2017/10/10/undo-redo-stack-is-back-qgis-transaction-groups/</a></li>
<li>Transaction group allows now to play more easily with stored procedure calls. It is now possible to use &#8216;QgsTransaction.ExecuteSQL&#8217;, dirty the edit buffer to let user be able to save changes, and give a name to that action so that the UNDO/ REDO actions are more explicit. See the Pull requests for more details:
<ul>
<li><a href="https://github.com/qgis/QGIS/pull/5376" rel="nofollow">https://github.com/qgis/QGIS/pull/5376</a></li>
<li><a href="https://github.com/qgis/QGIS/pull/5628" rel="nofollow">https://github.com/qgis/QGIS/pull/5628</a></li>
<li><a href="https://github.com/qgis/QGIS/pull/5663" rel="nofollow">https://github.com/qgis/QGIS/pull/5663</a></li>
</ul>
</li>
<li>Trigger QGIS actions or layer refresh from PostgreSQL. Want to code a live dashboard and use QGIS to display messages, pictures, refresh map layers when PostgreSQL casts a NOTIFY signal? Read more at <a href="http://oslandia.com/en/2017/10/07/refresh-your-maps-from-postgresql/" rel="nofollow">http://oslandia.com/en/2017/10/07/refresh-your-maps-from-postgresql/</a></li>
</ul>
<h3>Add consistency to UI controls &#8211; Nyall Dawson</h3>
<p>We&#8217;ve unified all the various opacity, rotation and scale controls to use the same terminology and numeric scales. We&#8217;ve also updated ALL methods for setting opacity, rotation and scale within the PyQGIS API to use consistent naming and arguments, making the API more predictable and easy to use. Lastly, we&#8217;ve also added a new reusable opacity widget (QgsOpacityWidget) to the GUI library so that future code can (and 3rd party scripts and plugins) can follow the new UI conventions for opacity handling.</p>
<h3>Extend unit test coverage for geometry classes &#8211; Nyall Dawson</h3>
<p>We&#8217;ve extended the unit testing coverage for all the underlying geometry primitive classes (points, lines, polygons, curves, collections, etc) so that all these classes have as close to 100% unit test coverage as possible. In the process, we identified and fixed dozens of bugs in the geometry library, and naturally added additional unit tests to avoid regressions in future releases. <strong>As a result QGIS&#8217; core geometry engine is much more stable.</strong> Furthermore, we utilised the additional test coverage to allow us to safely refactor some of the slower geometry operations, meaning that many geometry heavy operations will perform much faster in QGIS 3.0.</p>
<h3>Processing algorithm documentation &#8211; Matteo Ghetta &amp; Alexander Bruy</h3>
<p>The new Help system is landed and already available: when opening a Processing algorithm and clicking on the Help button, the guide of the algorithm will be showed in the default browser.</p>
<p>Many of the QGIS Processing algorithm guides have been enhanced with pictures and new or enhanced descriptions. A consistency number of Pull Requests <a href="https://github.com/qgis/QGIS-Documentation/pulls?q=is%3Apr+author%3Aghtmtt+label%3A%22Processing+help%22+is%3Aclosed">have been already merged</a> and many others are <a href="https://github.com/qgis/QGIS-Documentation/pulls?q=is%3Apr+author%3Aghtmtt+label%3A%22Processing+help%22+is%3Aopen">in review</a>. Just a few descriptions need to be still enhanced.</p>
<p>Currently all the QGIS algorithms have been described and all the PR in the doc repository have been merged (kudos to Harrissou for all the reviews!).</p>
<p>Right now the Help button of each Processing dialog will open the related page of the algorithm, BUT:</p>
<ul>
<li>if the name of the algorithm is made by only ONE word (e.g. clip, intersection&#8230;), the help button will open the browser to also the correct section (that is, the user will see directly the description of the related algorithm)</li>
<li>if the name of the algorithm has &gt;1 words (e.g. split polygon with lines, lines to polygon, ecc.) the Help button will open the correct page (so the algorithm GROUP) but is not able to go to the correct algorithm anchor. This is because sphinx converts &#8220;split with lines&#8221; in &#8220;split-with-lines&#8221; while QGIS system will always cast the words &#8220;split-with-lines&#8221; in &#8220;splitwithlines&#8221;. Not a big deal, but IMHO a pity.<br />
We are really too close to the solution.</li>
</ul>
<p>So Processing Help system right now consists of:</p>
<ul>
<li>QGIS algs -&gt; documented</li>
<li>GDAL algs -&gt; documented</li>
<li>GRASS -&gt; documented (own docs)</li>
<li>Orfeo -&gt; documented (own docs)</li>
<li>SAGA -&gt; nothing documented</li>
</ul>
<p>Thanks to QGIS Grants to provide this chance to give a big improvement to the Processing framework even if not in a coding way!</p>
<hr />
<p>Last but not least, we had another project that was not part of the grant programme but was also funded by QGIS.ORG in 2017:</p>
<h3>Python API documentation &#8211; Denis Rouzaud</h3>
<p>QGIS Python API Documentation is created using Sphinx and this work is available on <a href="https://github.com/opengisch/QGISPythonAPIDocumentation">Github</a>. The repo is a fork of QGIS’ one and has been merged in the meantime. The docs are available at <a href="https://qgis.org/pyqgis/master/">qgis.org/pyqgis</a>. It uses a new theme (sphinx_rtd_theme aka ReadTheDocs theme). Some improvements were brought in (not exhaustive):</p>
<ul>
<li>QGIS theming with colors and icon</li>
<li>Foldable toctree</li>
<li>Summary of methods and attributes for classes</li>
<li>Module index (not available before)</li>
<li>Correct display of overloaded methods</li>
</ul>
<p><strong>Full Python signature in Docstring</strong></p>
<p>In former SIP versions, it was not possible to use the auto generated signature if a Docstring already existed. This means any documented method could not have a signature created. Unfortunately for this project, the vast majority of methods in QGIS API are documented!</p>
<p>The source code of SIP was modified and theses changes got merged upstream. See rev 1788 to 1793 in SIP changelog. It will be released in upcoming 4.19.7 version. QGIS source code was modified accordingly to prepend auto generated Python signatures to existing Docstrings. Using a CMake configuration file for each module (core.sip.in, gui.sip.in, etc.) was required to avoid syntax errors when using former version of SIP (since bumping minimum version is not realistic).</p>
<p><strong>Sipify adjustments </strong></p>
<p>Many things were fixed in sipify script :</p>
<ul>
<li>Creation of links to classes, methods</li>
<li>Handling/fixing of Doxygen annotations \see, \note, \param</li>
<li>Handling of code snippets: c++ vs Python. Only Python are shown.</li>
</ul>
<hr />
<p>Thank you to everyone who participated and made this round of grants a great success and thank you to all our sponsor and donors who make this initiative possible!</p>
<p>Anita</p>
