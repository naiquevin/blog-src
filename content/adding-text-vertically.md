Title: Adding text vertically on multiple lines (region)
Author: Vineet Naik
Date: 2011-08-04
Tags: emacs, editing
Category: emacs
Summary:

Ok. Finally a new emacs trick. Actually I had come across this a while
back but then I went on a short vacation and later picked up a John
Grisham book (one of the hard-to-put-down types) and so the delay.

This one is about adding stuff vertically in a line in the buffer. It
might seem to be a bit vague and useless at first but it perfectly
fits a problem I face everyday in php-mode.

Now php-mode is not all that great if compared to the rest of the
emacs awesomeness.

The problem is that when I try to comment a region, it wraps each line
of the region in block comments ie. ``/* */`` which looks kind of ugly
and may be objectionable by fellow team members too.

So I started using this command as a work around to comment out a
region in php by prefixing each line with ``//``

The way I do this is as follows:

Set the mark at the required position on the starting line (in my case
column 0 or the start of the line)

Then move the cursor to the ending line using C-n normally.

Then type, ``C-x r t``

``String Rectangle : `` will appear in the mini buffer.

Type ``//`` to comment out each line and press ``RET``.
