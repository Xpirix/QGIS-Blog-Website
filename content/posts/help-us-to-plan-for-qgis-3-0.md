---
title: "Help us to plan for QGIS 3.0"
date: "2016-01-17T21:47:22+00:00"
draft: false
authors: ["timlinux"]
categories: ["Uncategorized"]
---

<p>Many of you out there may be wondering &#8216;when are we going to release QGIS 3.0?&#8217;. Last year (2015) we started investigating when and how we would release QGIS 3.0. We promised (<a href="http://anitagraser.com/2015/05/31/qgis-3-0-future-plans/">see Anita Graser&#8217;s post about this</a>) that we would convey clearly to our users and developers our plans well before making the QGIS 3.0 release. In this post I will try to lay out some of the considerations for a QGIS 3.0 release and at the end of this post there is an opportunity for you to present your ideas.</p>
<p><strong>Why 3.0?</strong></p>
<p>Typically (when following <a href="http://semver.org">semantic versioning</a>) a major release is reserved for times when you break the API of your software. Breaking API is not a trivial decision for the QGIS project since we have hundreds of thousands of users out there who depend on QGIS to &#8216;just work&#8217;, and many developers who need to maintain third party software written on top of the QGIS API.</p>
<p>From time to time <strong>breaking the API</strong> is necessary to accommodate updating the architecture with improved approaches, new base libraries and fixes to sub-optimal decisions made in the past.</p>
<p><strong>What are the implications of breaking the API?</strong></p>
<p>One of the reasons we are hesitant about releasing an API breaking QGIS 3.0 release is that it will have a huge impact, potentially breaking the hundreds of plugins in the plugin repository. Plugins would no longer compatible with new API and plugin authors would be required to manually review their plugins to identify and update  the places in their plugins where the code is no longer compatible with the new API.</p>
<p>The breadth of the updates required depends largely on</p>
<ul>
<li>how many backwards incompatible changes we make to the API</li>
<li>how many places plugin authors have used parts of the API which have changed</li>
</ul>
<p>I will talk more about how we can mitigate API breaking changes  further on in this article.</p>
<p><strong>What will be the key changes for 3.0?</strong></p>
<p>There are four key areas that we are looking to change in 3.0:</p>
<ul>
<li><strong>Updating Qt4 to Qt5:</strong> This is the basic set of libraries on which QGIS is built and provides a high level, platform independent abstraction layer for building a graphical user application. Qt also provides libraries for carrying out disk i/o, networking operations, and graphics drawing operations (key functionality for QGIS). Qt4 (on which QGIS is currently based) is now not actively being developed by the Qt library maintainers and we are expecting to experience problems in the near future building Qt4 for some platforms (e.g. OS X) or having readily accessible binaries  (e.g. Debian Testing and the upcoming release of Debian &#8220;Stretch&#8221;). Making QGIS work with Qt5 has already been worked on (chiefly by Matthias Kuhn) who together with Marco Bernasocchi produce the Android &#8220;<a href="http://www.opengis.ch/android-gis/qfield/">QField</a>&#8221; port of QGIS which is based completely on Qt5. There are however some outstanding limitations in the newer Qt5 that impact on QGIS &#8211; in particular with the embedded web browser widgets (used chiefly in the QGIS composer but also a few other places in QGIS).</li>
<li><strong>Updating PyQt4 to PyQt5:</strong> These are the python language bindings for Qt which the QGIS python API relies on. When we shift to the Qt5 C++ library, we also want to shift to the updated PyQt5 python library so that we can benefit from the new Qt5 API within the python environment too.</li>
<li><strong>Updating Python 2.7 to Python 3:</strong> Currently we bundle in Python 2.7 in our windows installers and require 2.7 on other platforms where we do not co-bundle Python with QGIS. Python 3 is the latest version of python and is recommended by the Python project. Python 2 is slightly incompatible with Python 3 (in much the same way as QGIS 2 -&gt; QGIS 3 will be incompatible). The python developers have made Python 3 largely backwards compatible to Python 2, but the compatibility in the opposite direction is not as good.</li>
<li><strong>Improving the QGIS API itself:</strong> One of the issues with maintaining API compatibility between releases is that you have to live with your design choices for a long time. In QGIS we try our best not to break the API within a minor release series &#8211; not always with success as the more hard core developers will attest to. Releasing an API incompatible version of QGIS for 3.0 will give us an opportunity to &#8216;clean house&#8217; by fixing things in the API that we are unhappy with. You can see a provisional list of proposed API changes for 3.0 by looking at the <a href="https://github.com/qgis/qgis3.0_api/issues">3.0 API issues list</a>.</li>
</ul>
<p><strong>Mitigating 3.0 API breakages</strong></p>
<p>As I mentioned the 3.0 release will break API from the 2.x release of QGIS and there is the potential that many existing plugins, applications and other code that rely on the current API will be broken. So what can we do to mitigate the changes? Matthias Kuhn, Jürgen Fischer, Nyall Dawson, Martin Dobias and other core developers have been looking at ways to mitigate the number of API breaking changes whilst still advancing the QGIS codebase to be based on the next generation of libraries and its own internal API. During our last QGIS Project Steering Committee meeting we ran through various possibilities. Matthias Kuhn kindly joined the meeting to help clarify our options going forward which I have tried to summarise in the table below:</p>
<table>
<tbody>
<tr>
<td></td>
<td><b>QGIS 2.14 LTR</b></td>
<td><b>QGIS 2.16 ???</b></td>
<td><b>QGIS 3.0</b></td>
</tr>
<tr>
<td><b>Release date</b></td>
<td><span style="font-weight:400;">End Feb</span></td>
<td><span style="font-weight:400;">4 months after 2.14</span></td>
<td><span style="font-weight:400;">8 month cycle?</span></td>
</tr>
<tr>
<td><b>Notes</b></td>
<td></td>
<td><span style="font-weight:400;">Update python code of core QGIS to be Python 3 compatible and PyQt5 compatible (partial implementation for key functionality e.g. console, python core plugins etc.)</span></td>
<td></td>
</tr>
<tr>
<td><b>Qt4</b></td>
<td><span style="font-weight:400;">Yes</span></p>
<p><span style="font-weight:400;">Deprecated in Debian Stretch (due in a year)</span></p>
<p><span style="font-weight:400;">(webkit removed)</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">No</span></td>
</tr>
<tr>
<td><b>Qt5</b></td>
<td><span style="font-weight:400;">No</span></p>
<p><span style="font-weight:400;">Misses QWebView &#8211; new replacement not on all platforms. Also misses QPainter Engine.</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">Yes</span></td>
</tr>
<tr>
<td><b>PyQt4</b></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">No</span></td>
</tr>
<tr>
<td><b>PyQt5</b></td>
<td><span style="font-weight:400;">No</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">Yes</span></td>
</tr>
<tr>
<td><b>Python 2</b></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">No</span></td>
</tr>
<tr>
<td><b>Python 3</b></td>
<td><span style="font-weight:400;">No</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">Yes</span></td>
</tr>
<tr>
<td><b>API Cleanup</b></td>
<td><span style="font-weight:400;">No</span></td>
<td><span style="font-weight:400;">No</span></td>
<td><span style="font-weight:400;">Yes</span></td>
</tr>
<tr>
<td><b>Wrappers </b><b><br />
</b><span style="font-weight:400;">PyQt5 -&gt; PyQt4</span><span style="font-weight:400;"><br />
</span><span style="font-weight:400;">Provide ~90% backwards compatibility</span></td>
<td><span style="font-weight:400;">No</span></td>
<td><span style="font-weight:400;">Yes</span></td>
<td><span style="font-weight:400;">Yes</span></td>
</tr>
<tr>
<td><b>Mainstream Binary</b></td>
<td><span style="font-weight:400;">Qt4 Based</span></td>
<td><span style="font-weight:400;">Qt4 Based</span></td>
<td><span style="font-weight:400;">Qt5 Based</span></td>
</tr>
<tr>
<td><b>Funding priority</b></td>
<td></td>
<td><span style="font-weight:400;">Python wrappers</span></td>
<td></td>
</tr>
</tbody>
</table>
<p>There are two key things to note about Matthias&#8217; proposal:</p>
<ul>
<li>In the<strong> first phase,</strong> work would be done in the QGIS 2.x series to complete support for Qt5, PyQt5, Python 3.0 whilst still supporting Qt4, PyQt4 and Python 2.7. This implies that all changes made in the first phase would be backwards compatible with previous QGIS 2.x releases. Python wrappers will be introduced so that the old PyQt4 API can still <strong><em>mostly</em></strong> be used when compiling against Qt5, PyQt5, Python 3.0. When using QGIS compiled against Qt4, PyQt4 and Python 2.7 there would be <em><strong>no</strong></em> compatibility breakage.</li>
<li>In the <strong>second phase</strong>, we would work to produce QGIS 3.0 which introduces a number of API breaking changes, completely removing Python 2.7, Qt4 and PyQt4 support. <strong>The python wrappers produced in the first phase would be kept</strong> and relied on to ensure that a large proportion of python code (plugins, scripts etc.) developed for QGIS 2.x releases continue to work in QGIS 3.x releases. In this phase we would also introduce the QGIS API changes which may break some plugins. To address this we will provide a migration guide to try to ease the process for those moving from code depending on the QGIS 2.x releases to the QGIS 3.x releases.</li>
</ul>
<p><strong>Caveat emptor</strong></p>
<p>There are a couple of &#8216;gotchas&#8217; that we should raise at this point as the above makes the migration to QGIS 3.0 sound fairly painless.</p>
<ol>
<li>The first thing we should emphasise is that while the approach laid out above tries to minimise the amount of work python script and plugins writers have to do, this will not be a 100% effort free solution for python coders using QGIS. There will very likely be cases where code needs to be adjusted and in all cases at the very least it will probably need to be reviewed in order to ensure that it still functions properly.</li>
<li>There is no formal funding set aside to pay for developers to spend their time working on the migration process. Because of this it is going to be incredibly hard to give accurate timelines as to how long each part of the process will take. We need to take this uncertainty into account in our planning. Of course we <a href="https://www.qgis.org/en/site/getinvolved/donations.html">welcome donations</a> to help make this happen.</li>
<li>There may be developers and institutions out there funding new features for the QGIS 2.x series and this may affect your work. You should include in your project plans and budgets some allocation to cope with the migration to the QGIS 3.x platform.</li>
<li>If we do the work in the &#8216;master branch&#8217; there may be a protracted time during which our master branch is unstable and in flux due to ongoing updates towards QGIS 3.0.</li>
<li>If we do the work in a &#8216;3.0 branch&#8217;, we run the risk that the 3.0 development may drag on longer unless there is a devoted group of developers working on it and getting it ready to merge to master.</li>
</ol>
<p><strong>Proposals</strong></p>
<p>In the light of all the above information, we propose one of two courses of action:</p>
<p><b>Proposal 1:</b></p>
<p><span style="font-weight:400;">Do an interim release of 2.16 and then commence work on 3.0 in master with an 8 month development window. Work on 3.0 related stuff could already begin in 2.16  (see python3/pytq5), only incompatible changes have to be postponed to post 2.16.</span></p>
<p><b>Advantage</b><span style="font-weight:400;">: Main focus of work would be in master branch. Work scheduled for the near future can be released in expected timelines. Plugins will continue to work with master. People can start to write and test their code in a portable manner.</span></p>
<p><b>Disadvantage</b><span style="font-weight:400;">: Difficult to determine timelines as we don’t have funding </span></p>
<p>&nbsp;</p>
<p><b>Proposal 2:</b></p>
<p><span style="font-weight:400;">Create a long running 3.0 branch for the port to Qt5, Python 3.0 and PyQt5 and call for developers to get their 3.0 work in there. Continue with 2.x releases with the usual frequency until 3.0 is ready.</span></p>
<p><b>Advantage</b><span style="font-weight:400;">: We can release it ‘when it’s ready’. If there is no funding for 3.0 work subsequent releases are not jeopardised.</span></p>
<p><b>Disadvantage:</b><span style="font-weight:400;"> Duplication of effort as work in master coming in needs to be ported over to the 3.0 branch.</span></p>
<p><strong>Alternative proposals</strong></p>
<p>Do you have an alternative proposal? We would like to get all the proposals on the table so that we (the PSC in consultation with core developers) can make the best judgement of how to approach the nitty-gritty process of managing the QGIS 3.0 development process. If you wish to submit a proposal, please send it to me (<a href="mailto:tim@qgis.org">tim@qgis.org</a>) with the subject line &#8216;<strong>QGIS 3.0 Proposal</strong>&#8216;. Please keep your proposal very short and succinct as we just need the high level concepts.</p>
<hr />
<p>&nbsp;</p>
<p>Here is the proposal submitted by Matthias Kuhn that you can use as a reference of how we might like  a proposal to look:</p>
<p>QGIS 2.16 Release as usual in 4 months</p>
<p>-&gt; PyQt5 Support<br />
-&gt; Python 3 Support<br />
-&gt; Wrapper library for PyQt4/PyQt5<br />
-&gt; Maybe a helper transition script that does 80% of the rewrite<br />
-&gt; All old plugins still work<br />
-&gt; Some python code is updated (console, plugin manager, processing) to<br />
have some guidelines and experience how to update python code<br />
-&gt; For future debian, mac osx&#8230; versions there&#8217;s a qt5 version around<br />
(with almost no plugins working)</p>
<p>During the same time: make some noise that QGIS 3 is coming and we need<br />
everybody to put some money and dev time aside for it and that it&#8217;s<br />
going to be amazing.</p>
<p>&#8212;&#8212;&#8212;&#8212;&#8212;-</p>
<p>After that: 8 months break for 3.0 (maybe some betas after 4 months and<br />
every month after)</p>
<p>Back to normal, everybody happy &#8211; except the lazy plugin devs who didn&#8217;t<br />
update &#8211; 🙂</p>
