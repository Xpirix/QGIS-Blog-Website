---
title: "Call for applications: QGIS API Documentation Improvement"
date: "2015-08-19T19:41:40+00:00"
draft: false
authors: ["timlinux"]
categories: ["Uncategorized"]
---

<div class="ss-form-desc ss-no-ignore-whitespace" dir="ltr">
<p>Dear QGIS DevelopersIn the last few years we have been steadily improving the amount of funding we are able to accumulate in the QGIS project. Our goal in obtaining funding is always to &#8216;make QGIS better&#8217;. Up until now we have focussed funding on high profile aspects of the project: Funding regular hackfests, paying for bug fixing work prior to releases, funding infrastructure such as servers, domain name registrations etc.</p>
<p>With improved funding levels we now have the opportunity to also start addressing some of the many less obvious components of QGIS that badly need attention, but often don&#8217;t attract volunteers. In our July 2015 PSC meeting it was agreed that we would start this initiative by funding one or more developers to improve the python documentation in QGIS. Here, briefly, is the vision:</p>
<p>Lets take our inspiration from Qt. As a foundational library for QGIS, I have always loved the fact that Qt4 is so well documented. Take a look at this for example &#8211; <a href="http://www.google.com/url?q=http%3A%2F%2Fdoc.qt.io%2Fqt-4.8%2Fqlabel.html%23details&amp;sa=D&amp;sntz=1&amp;usg=AFQjCNGvKW_ZalYsbA4WUReMC-q2DWWYog">http://doc.qt.io/qt-4.8/qlabel.html#details</a></p>
<p>The Qt4 documentation provides a readable narrative explaining the purpose (with images and illustrations if needed) of each class. It also provides a code snippet, which in many cases you can simply cut and paste into your code and then tweak to get started.</p>
<p>As a PyQGIS programmer you have two main resources: The QGIS Python cookbook and the QGIS C++ API documentation. The cookbook is an excellent resource, but it is hard to keep it synchronised with the code base &#8211; so examples often run the risk of being out of date, or don&#8217;t leverage new functionality that makes its way into the code base. The C++ documentation is good in terms of coverage, but it often lacks detail and as a python programmer you may find it a bit off putting since the text is littered with examples using pointers. Also, the C++ documentation isn&#8217;t always a one to one match for python users, and doesn&#8217;t explain python specific behaviour such as how ownership is passed around with returning objects.</p>
<p>Wouldn&#8217;t it be nice if the C++ API documentation also included the content that is in the python cookbook? And wouldn&#8217;t it be nice if the C++ documentation became the C++ *and* Python API documentation &#8211; catering for users of both programming languages and providing for a single point of reference and maintenance? Even better the python documentation would live right in the C++ code, so that anytime someone touches the code base they can easily maintain the documentation without needing to jump through a lot of hoops.</p>
<p>For this funded effort we are thus seeking one or more individuals to lay the foundation for this work:</p>
<ul>
<li>establish norms and guidelines for improving the doxygen API docs so that each documented resource can include both python and C++ documentation.</li>
<li>port the cookbook content over to the API documentation</li>
<li>create doxygen pages to provide a starting point for python programmers to be able to carry out common activities they need</li>
<li>populate the API docs with Python examples and improved descriptions</li>
<li>do these in a nice clear and concise writing style, again taking inspiration from the fine work that Qt has done</li>
<li>perhaps do something really smart to generate docs from the SIP API and incorporate it into our doxygen doctree?</li>
</ul>
<p>If you think this is something you are able to do, please contact the QGIS PSC using this form and let us know!</p>
</div>
<p><a href="http://goo.gl/forms/WRGSvWHkBb">Click here to apply here if you are interested in this work</a></p>
