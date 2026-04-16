---
title: "QGIS Phasing out 32-bit support on Windows"
date: "2020-10-15T06:05:18+00:00"
draft: false
authors: ["mbernasocchi"]
categories: ["QGIS Board"]
featured_image: "/wp-content/uploads/2017/04/logo_evolution.png"
---

<p class="wp-block-paragraph"><strong>QGIS will drop 32-bit support on Windows after the QGIS 3.16 release when we update our Qt dependencies to Qt 5.15. </strong></p>



<p class="wp-block-paragraph"><strong>The Plan</strong></p>



<p class="wp-block-paragraph">QGIS will drop 32-bit Windows support in the next few months. QGIS 3.16 LTR will still be available for 32-bit systems. 32-bit support will be dropped during the process of updating Qt to version 5.15. Due to the complexity of the involved tasks, there is no fixed date for when this update will happen.</p>



<p class="wp-block-paragraph"><strong>Reasoning</strong></p>



<p class="wp-block-paragraph">Over the last years, pretty much all new computers (including low-end machines) have been built with 64-bit processors. Our latest QGIS user survey (<a href="http://blog.qgis.org/2020/04/02/ltr-usage-survey/">http://blog.qgis.org/2020/04/02/ltr-usage-survey/</a>) confirmed that this move to 64-bit had been almost completed on the hardware side and only 7% of survey respondents indicated that they are still using 32-bit. Therefore, we have decided to phase out 32-bit support in QGIS since we have many libraries to update in the next months and we have only limited resources.</p>



<p class="wp-block-paragraph"><strong>Further roadmap</strong></p>



<p class="wp-block-paragraph">The update to Qt 5.15 is an important step towards staying in sync with Qt developments. Qt 5.15 is the minimum version that will provide forward compatibility with Qt 6. By updating to 5.15, we, therefore, ensure that QGIS is future proof.  </p>
