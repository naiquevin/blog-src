Title: Speedy navigation across the buffer in emacs
Author: Vineet Naik
Date: 2011-07-15
Tags: emacs, editing
Category: emacs
Summary:
Status: published


Okay. So here goes the first one. Very often I find myself searching
for a line of code in the same file so that I can copy it over into
some other function or a method. This whole process of moving to the
desired line of code, copying it over, coming back to where you
started the search and yanking it can be done unbelievably fast in
emacs. This is because emacs keeps setting marks for you automatically
while you navigate through the lines of code (noticed the words "Mark
Set" in the minibuffer ?). In other words it keeps saving your
previous positions. So all you need to master is how to move back to
the previous position quicky after copying. To move to the previous
mark the command is C-u C-SPC

So for the above scenario the command sequence would be,

* C-s or C-r (search forward or backward)

* C-m or RET (after finding the desired line)

* C-a  (moving to the start of the line)

* C-SPC (to set the mark)

* C-e (move to the end of the line thereby selecting a region)

* M-w (copy region)

* C-u C--SPC * 2 (to return back to the initial mark)

Looks like too much work for the fingers but its definitely faster
than the right click scroll thing one would have to do with a mouse.

Just think as if you are driving a racing car. It can go from 0-60 in
3.5 secs, _provided_ you can shift gears fast enough :)

