Title: How to get rid of searchportal.information.com redirection
Author: Vineet Naik
Date: 2010-02-14 12:18:28
Tags: malware, web 2.0, spyware
Category: webdev
Summary: 

*Important note before you read further: The other day i found out that this wasn't quite the solution.  But in case you are desperately trying to get rid of this thing, this article might still give you some clues.  Please find explanation at the end of this post.*

In case you encounter the problem of redirection to a website called ***searchportal.information.com*** then this article is for you. I was facing this problem where, whenever I tried to access this domain ie. www.noiseokplease.com, it redirected me to searchportal.information page which was full of links but having the heading 'Noiseokplease'!

And the worst part which actually gets you to your wits end is that the problem happens only on a specific machine, on all browsers, miraculously fixes itself after sometime and reappears again in a few days. It stays even after deleting all the cookies and a full system scan or a good anti-virus scan fails to fix it.

Here is the solution.

It appears that the TCP/IP network connection is in some way the cause. I got this hint while i was going through a certain message board. So just disable the connection and enable it again. If you need dialer to connect then just disconnecting and reconnecting will not work. You will have to disable the 'Local Area Connection' (it is the name on my pc, might be different on yours) and enable it again.

Its pretty much a superficial solution but it worked for me and so i decided to share it here. Hope it helps someone.

**Edit:** Yes, so the other day, whatever I have written above didn't work. Couldnt think of anything else but waiting. Today I tweaked some network connection settings and it started working again. But now I am not sure whether it was because of the changes or it fixed itself overtime as it has been happening in the past.
