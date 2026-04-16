---
title: "Licensing requirements for QGIS plugins"
date: "2016-05-29T08:09:27+00:00"
draft: false
authors: ["timlinux"]
categories: ["QGIS Board"]
tags: ["licensing"]
---

<p>One thing we have been encountering lately in the QGIS project is plugin authors not understanding the licensing requirements for publishing their QGIS plugins. In this article I will try to clarify this a little:</p>
<p>QGIS is Open Source Software and provides a great platform for third parties to distribute additional functionality to users through our plugin system. QGIS is licensed under the GPL version 2 or greater. This license is provided with every copy of the QGIS and in the source code and is available on our web site here:</p>
<p><a class="" href="http://docs.qgis.org/2.0/en/docs/user_manual/appendices/appendices.html">http://docs.qgis.org/2.0/en/docs/user_manual/appendices/appendices.html</a></p>
<p>Under the terms of this license, it is a requirement that all plugins distributed via <a class="" href="http://plugins.qgis.org/">http://plugins.qgis.org</a> (or through other repositories that may be self-hosted) should comply with the GPL version 2 or greater license. In particular all code included in any plugin should be made clearly and easily available in source form. It has come to our attention that some plugin authors are distributing plugins that do not comply with this condition.</p>
<p>We ask you to consider the fact that many thousands of hours of work and large amounts of financial outlay from individuals and companies has gone into the creation of QGIS. This work is done under the basis that in-kind contributions raise the quality and capabilities of the platform for everyone. When you create a plugin, you only need to spend a minimal amount of effort to solve your specific requirements because we have done the rest of the work needed to provide an entire platform for you and our community of users. This is a key value proposition of Open Source: &#8216;a rising tide floats all boats&#8217;.</p>
<p>By publishing the source code for your plugin, others may inspect the underlying code of your plugin and learn from it and use that knowledge to further improve the platform. Not releasing your source code breaks this model. Besides being a contravention of the licensing conditions under which you received the QGIS software, withholding your source code does not advance the body shared knowledge, and does not embrace the spirit of sharing that has made the QGIS project such a success to date.</p>
<p>Thus if you are a plugin author who is distributing your plugin without the accompanying source code, you need to be aware that the source code needs to be made available to each person who receives the binary sources for your plugin.</p>
<p>One query that plugin authors have raised is whether the requirement to publish the sources of their plugin precludes their ability to sell or otherwise commercially benefit from their plugin work. This is not the case &#8211; you can sell you plugin as long as you make  the sources of your plugin available under the same license as QGIS to each purchaser.</p>
<p>Should you have any queries about how to better collaborate within the QGIS community we are available to you &#8211; please direct your queries to info@qgis.org</p>
