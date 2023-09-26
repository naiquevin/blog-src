Title: Killing buffers
Author: Vineet Naik
Date: 2011-07-19
Tags: emacs, editing
Category: emacs
Summary:
Status: published

In emacs, as we open files, a lot of dired buffers get accumulated. I
personally find them a nuisance after a while specially during longer
emacs sessions. Killing them one by one using ``C-X k`` would be quite
tedious. Fortunately there is better way to kill many buffers at a
time.

For this we list all the buffers using ``C-X C-b``. The list opens in
a new buffer so we need to switch to this buffer using ``C-x o``. Now
we need to mark all the buffers that we wish to kill by typing
``d``. As we mark, a capital ``D`` appears alongside the buffers'
names. After all buffers to be killed are marked, just press ``x`` and
all the buffers will get killed.
