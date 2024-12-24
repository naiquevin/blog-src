Title: Repaying emacs configuration debt
Author: Vineet Naik
Date: 2024-12-24
Tags: emacs
Category: programming
Summary: Lessons learnt from getting my emacs config to work on Windows
Status: published

I have been using emacs since 2011 and if git commit history is to be
believed, I started customizing it almost immediately.  Occasionally,
I've been guilty of blindly borrowing elisp code from other peoples'
config.

Last week I had to set up <s>emacs</s> my emacs config on a Windows
machine, during which I experienced the same sinking feeling that comes
when tech debt begins to slow you down.

The following two lines in my config were the culprits:

```elisp
(setq buffer-file-coding-system 'utf-8)
(setq coding-system-for-write 'utf-8)
```

These tell emacs what coding system to use when saving the buffers. I
don't remember when or why they were added, so most likely I must have
copy-pasted them from somewhere without fully understanding what they
do or giving too much thought about whether or not they are really
required to be configured.

It turned out that these two lines were the root cause of almost all
problems I had encountered during the setup,

1. When I had eval'd my `init.el` file for the first time, there were
   errors while parsing the autoloads files. I found [one
   bug](https://lists.gnu.org/archive/html/bug-gnu-emacs/2022-01/msg01721.html)
   that was reported but already fixed 3 years ago. I was able to
   identify the problematic code and for a moment thought that I had
   discovered a bug in emacs! I also wrote some [elisp
   code](https://github.com/naiquevin/emacs-config/blob/master/win-regen-autoloads.el)
   for regenerating the autoloads files which fixed that particular
   issue.

2. Then, when I opened a file from the project I was working on, it
   showed `^M` characters at line endings. Everything else seemed to
   be working fine so it felt like a minor inconvenience. I quickly
   found a [code snippet](https://stackoverflow.com/a/750933) on
   Stackoverflow to hide these chars and moved on.

3. At the time of committing my changes to git, it showed
   modifications to the entire file because the line endings had
   changed. Initially it seemed git was the culprit until tweaking
   github's `core.autocrlf` config whichever way wouldn't help. I
   again searched for and copied more config, which kinda worked but
   not for all files.

4. A couple of hours later, I came across some files in which emacs
   couldn't indent code properly because it had mixed line endings!

Until I had encountered the last problem, I was trying to deal with
every obstacle by adding more and more config. Only when I came across
files with mixed line endings did I realize that copy-pasting random
config from the internet wasn't going to work.

It was time to think from the first principles. How do we want the
editor to behave?

- If an editor like emacs is available on all platforms, shouldn't it
  know how to deal with different line endings for the respective
  platform?

- And isn't it reasonable to expect the editor to take care of files
  worked upon by multiple contributors, possibly using different
  platforms and OSs.

These led to the question that I should started out with - What does
emacs do by default?

So I tried running emacs without loading the init file, and indeed it
does the right thing. Whatever line endings it finds in an existing
file, it preserves those. For new files, it uses what makes sense for
the platform i.e. DOS (CRLF) for Windows and Unix (LF) for
Linux/MacOS.

After going through the documentation on [Coding
systems](https://www.gnu.org/software/emacs/manual/html_node/emacs/Coding-Systems.html)
and doing a bit of trial and error on different OSs, it became clear
that the there was no need to set those two variables. I also tried to
freshly install packages with the two variables removed, and it worked
without any parsing errors. In other words, I had wasted my time
writing code to regenerate the autoloads files.

In retrospect, this experience felt like a small-scale demo of how
tech debt builds up and hampers progress in a real project.

1. It begins with making hasty, uninformed decisions to save time -
   like copying configurations without understanding their underlying
   assumptions
2. At some point, the assumptions don't hold and the system breaks -
   e.g. having to set up on Windows along with Linux/Unix
3. Our first response is to resort to workarounds to _quickfix_ the
   problem, because repaying the tech debt seems like a lot of
   effort - like hiding the `^M`s and writing code to regenerate the
   autoloads files
4. Often such workarounds end up taking up similar time and effort and
   additionally introduce more assumptions

Arguably, my emacs config is a real project too&mdash;it's going on
for last 14 years, affects my day-to-day productivity and has at least
one invested user! I'm happy to have paid back some of the
configuration debt through this exercise even though it felt like an
ordeal.
