---
title: "QGIS 3.0 plans"
date: "2016-02-10T07:38:13+00:00"
draft: false
authors: ["timlinux"]
categories: ["QGIS Board"]
---

<p>&nbsp;</p>
<p><img loading="lazy" data-attachment-id="339" data-permalink="http://blog.qgis.org/2016/02/10/qgis-3-0-plans/qgis-icon-60x60/" data-orig-file="/wp-content/uploads/2016/02/qgis-icon-60x60.png" data-orig-size="60,60" data-comments-opened="0" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;}" data-image-title="qgis-icon-60&amp;#215;60" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2016/02/qgis-icon-60x60.png" class="alignnone size-full wp-image-339 aligncenter" src="/wp-content/uploads/2016/02/qgis-icon-60x60.png" alt="qgis-icon-60x60" width="60" height="60" /></p>
<p>Ok so quick spoiler here: there is no QGIS 3.0 ready yet, nor will there be a QGIS 3.0 for some time. This article provides a bit more detail on the plans for QGIS 3.0. A few weeks ago I wrote about some of the considerations for the 3.0 release, so you may want to <a href="http://blog.qgis.org/2016/01/17/help-us-to-plan-for-qgis-3-0/">read that first</a> before continuing with this article as I do not cover the same ground here.</p>
<p>A <strong>lot</strong> of consideration has gone into deciding what the approach will be for the development of QGIS 3.0. Unfortunately the first PSC vote regarding which proposal to follow was a <a href="https://www.loomio.org/d/5MCdPwoL/vote-to-approve-the-process-for-qgis-3-0">split</a> decision (4 for, 3 against, 1 abstention and 1 suggestion for an alternative in the discussion). During our PSC meeting this week we re-tabled the topic and eventually agreed on Jürgen Fischer&#8217;s proposal (Jürgen is a QGIS PSC Member and the QGIS Release Manager) by a much more unanimous margin of 8 for, 1 neutral and 1 absent. Jürgen&#8217;s proposal is largely similar to the Proposal 2 described in my <a href="http://blog.qgis.org/2016/01/17/help-us-to-plan-for-qgis-3-0/">previous posting</a>. I want to make some special notes here about our discussion and subsequent decision which will hopefully help to clarify the thinking behind our decision for other interested observers.  First let me lay out Jürgen&#8217;s plan in his own words:</p>
<p><span style="font-weight:400;">&#8220;</span><span style="font-weight:400;">My preferred approach would still be:</span></p>
<ul>
<li style="font-weight:400;"><span style="font-weight:400;">Do a Qt5/PyQt5/Python3 branch in parallel, actually work on it until it&#8217;s ready, make it master and release it as 3.0</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">Meantime keep working on master (2.x) and keep releasing them every 4 months as usual</span></li>
</ul>
<p><span style="font-weight:400;">Everyone can work on the branch (s)he wants (or is hired to), but needs to consider if (s)he want to do it (or spend funds on):</span></p>
<ul>
<li style="font-weight:400;"><span style="font-weight:400;">only for 2.x: knowing that it will be released soon; but might become unusable because platforms drop support for stuff it depends on sooner or later</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">only for 3.x: not knowing when that will ever release or</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">for both: knowing that work needs to be done twice.</span></li>
<li style="font-weight:400;"><span style="font-weight:400;">People adding features to the master branch will be responsible to ensure that their work gets merged to 3.0 branch.</span></li>
</ul>
<p>As PSC we should maintain the environment for people to do something for QGIS &#8211; but we cannot tell them to &#8211; so we don&#8217;t have resources we can actually plan with and that means we can either release something when the big thing is ready or what we have in fixed intervals.&#8221; &#8211; Jürgen Fischer</p>
<p>What follows are some further details and clarifications to our preferred approach:</p>
<p><strong>Why do parallel development?</strong></p>
<p>Parallel development of 3.0 maintaining our master branch with 2.x code in it has advantages and disadvantages. First the advantages:</p>
<ul>
<li>If we encounter major technical difficulties / release blockers in the 3.0 branch, it will not impact on our normal 3 monthly release cycle.</li>
<li>Our binary build systems (Linux, Windows and OSX binaries) will be unaffected until 3.0 is ready.</li>
<li>It is very likely that building 3.0 binaries on different platforms is going to have difficulties for each platform. For example OSGEO4W has no Python3 and Qt5 packages yet. Someone needs to see to the creation of the required package as a separate exercise from the actuals development of a version of QGIS that will take advantage of these updated libraries. We don&#8217;t yet know what problems may be in countered in preparing these.</li>
<li>&#8220;Don&#8217;t break what already works&#8221;: we have a working and relatively stable master branch and we don&#8217;t want to do a &#8216;cowboy stunt&#8217; and break it. We prefer to wait until the 3.0 branch is mature, has passing tests and is known to work well before merging it into master and treating it as our &#8216;best we currently have&#8217; master branch.</li>
</ul>
<p>Of course nothing in life is completely easy, there are also some disadvantages<strong>:</strong></p>
<ul>
<li>Some developers may feel that running two mainstream branches is dilution of effort. To counter this, our public recommendation is that after 2.16 comes out, all QGIS contributors are <strong>strongly encouraged</strong> to provide their patches against the 3.0 branch. Any features applied to the master branch is <strong>not guaranteed</strong> to be part of the 3.0 release.</li>
<li>Regular merging of master to the 3.0 branch may prove more and more difficult over time as the two branches diverge more. Again we will strongly encourage that developers submitting new features after the 2.16 release do so against the 3.0 branch.</li>
<li>3.0 branch won&#8217;t have auto build system for nightly binaries in the beginning. Since we expect that the initial branch of 3.0 will break these anyway, Having a separate branch is actually an advantage here as it will give binary packages some time to get their build systems up to speed.</li>
</ul>
<p><em>To clarify</em> things for developers wondering where to commit their work: we discourage people from writing new features<strong> in master after 2.16 is released</strong> and rather ask them to make their changes in the 3.0 branch. Only those who really need to see their features in the next 2.18 release would have to dual commit.</p>
<p><strong>Isn&#8217;t it better to work on 3.0 in the master branch?</strong></p>
<p>Some queries have been raised about whether it would be better to rather work on 3.0 in the &#8216;master branch&#8217; and relegate the 2.x code base to a side branch (instead of our intended approach which is to keep master tracking 2.x until 3.0 is ready and then merge it to master). We feel that keeping master tracking the 2.x code base is more conservative &#8211; it will not break existing packaging / build systems and if there is any major hitch in 3.0 development the release process will continue unabated based on the 2.x code set. While 3.0 is under development, package builders will have time to figure out the packaging process while still keeping the regular nightly builds against 2.x running. The implication of this is that 2.18 may contain only bug fixes which were applied to the 2.x branch and no significant new features.</p>
<p><strong>The schedule will not be fixed</strong></p>
<p>One thing that we want to make really clear (and was a key point in our many discussions) is that there will be no fixed release date for QGIS version 3.0. There are several reasons for this:</p>
<ul>
<li>As a steering committee, we can only set the QGIS ship pointing in a given direction, our power to actually make work happen is extremely limited. This is because we are a community made up largely of volunteer developers or developers working on a commission basis for third party clients. We have no say in how these contributors spend their time.</li>
<li>We do not yet know which (if any) major technical issues will be encountered during the development of 3.0. Any such issues could very well delay the roll out of QGIS 3.0.</li>
</ul>
<p>Instead our plan is to make the 2.16 release and then effectively move all developer effort to the 3.0 branch as best we can (through close liaison with our developer community).</p>
<p><em>To clarify things for those wondering when they will give 3.0 to their users:</em> The actual release date for 3.0 its interterminate, but the general aim is still to try to encourage everyone to get it ready for 1 year from now. Remember that as an open source community we cannot directly ensure that project timelines are met since our developer force is largely volunteer based or work according to their own companies agendas.</p>
<p><strong>Will 3.0 be a Long Term Release (LTR)?</strong></p>
<p>It is our recommendation that we <strong>wait until 3.2 is ready</strong> before designating it an LTR &#8211; there are going to be large changes in the code base for 3.0 and we would rather stabilise things a bit before applying the LTR label to the release.</p>
<p>&nbsp;</p>
<p><strong>Looking forward to 3.0</strong></p>
<p>Personally I am very much looking forward to the release of QGIS 3.0 &#8211; it represents another huge milestone in our project, it affords us a great opportunity to get rid of a lot of cruft out of our code base and API&#8217;s and it will arm us with a set of modern, new libraries that will see us through the next several years. Rock on QGIS 3.0!</p>
<p><img loading="lazy" data-attachment-id="124" data-permalink="http://blog.qgis.org/2015/11/03/introducing-the-qgis-board/timsutton/" data-orig-file="/wp-content/uploads/2015/10/timsutton.png" data-orig-size="336,191" data-comments-opened="0" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;}" data-image-title="timsutton" data-image-description="" data-image-caption="" data-large-file="/wp-content/uploads/2015/10/timsutton.png" class="alignnone size-full wp-image-124" src="/wp-content/uploads/2015/10/timsutton.png" alt="timsutton" width="336" height="191" srcset="/wp-content/uploads/2015/10/timsutton.png 336w, /wp-content/uploads/2015/10/timsutton.png 150w, /wp-content/uploads/2015/10/timsutton.png 300w" sizes="(max-width: 336px) 100vw, 336px" /></p>
<p>QGIS PSC Chairman</p>
