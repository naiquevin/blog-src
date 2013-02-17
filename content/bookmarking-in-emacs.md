Title: Bookmarking in Emacs
Author: Vineet Naik
Date: 2011-07-22
Tags: emacs, editing
Category: emacs
Summary:

Emacs allows bookmarking inside buffers so that you can quicky visit
those at a later time. And by later time I mean any time later, even
if its a new emacs session.

The commands are as follows :

Set bookmark ``C-X r m <bookmark_name>``

View bookmarks in the minibuffer ``C-X r b <up/down arrow>`` or ``C-s`` to
I-search (Sounds familiar?)

View a list of all bookmarks ``C-X r l``

Delete bookmark ``C-X r l`` (to view list) and then mark with ``D`` and delete
with ``x``

As you can see a nice thing with emacs is that a lot of old concepts
apply to the newly learned stuff for eg. in this case searching for a
bookmark can be related to searching for open buffers and deleting
bookmarks is to be done just the way we kill open buffers.

Also, if a bookmark is set, it persists in subsequent sessions as well
until its deleted. And to jump to any set bookmark, it doesn't require
the buffer to be open.

I never used bookmarks in my previous ide which was eclipse. But here
it seems quite useful to me. I personally don't like the open files in
previous ide session auto-opening up at startup. I prefer starting
with a clean slate. So I can just set a bookmark on the dired buffers
of the projects that I am working on currently or just set one before
wrapping up day's work so that I can start from there the next day.
