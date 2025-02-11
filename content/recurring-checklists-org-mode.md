Title: Recurring checklists using org mode in emacs
Author: Vineet Naik
Date: 2025-02-11
Tags: emacs, org mode
Category: emacs
Summary: How I manage recurring checklists in org mode using a hidden gem from the org-contrib package
Status: published

Based on my experience of building and maintaining professional and
personal/hobby projects, I've come to realize that I often tend to
prefer well documented checklists over automated scripts for recurring
workflows.

Let me be clear about what I mean by recurring checklists first. I
have a side project which is a web application that uses VueJS for the
frontend, Rust for backend, and
[tapestry](https://github.com/naiquevin/tapestry) for generating SQL
files from jinja templates. It runs behind nginx and is managed using
systemd on a VM. As you can see, there are many steps involved in
building and deploying the app and for that I have a checklist in the
same repository that comprehensively documents every single step. Even
though I have previous experience of automating such workflows, I
refrain from doing it here, because every time I have to build and
deploy the app, I am happy that it's a checklist and not a script.

As I began writing this article, I thought about the reasons behind
such a preference, but that part itself got so big that I felt it
deserves to be a separate post. It's sitting in my drafts folder now
and I hope to publish it soon. Today, I'll stick to how I manage such
recurring checklists in emacs using org mode thanks to a hidden gem
from the org-contrib package.

Now org mode supports checklists out of the box. You just have to
create a [plain list](https://orgmode.org/manual/Plain-Lists.html)
under an outline entry and prefix it with a
[checkbox](https://orgmode.org/manual/Checkboxes.html) i.e. `[ ]`.

A build checklist for the above app would look something like this:

```org
* Build
  - [X] Generate SQL files using tapestry
    #+begin_src bash
        cd <dir>
        tapestry render
        # etc.
    #+end_src
  - [X] Build backend
    #+begin_src bash
        cargo build --release
        # etc.
    #+end_src
  - [ ] Buiild frontend
    #+begin_src bash
        npm run build
        # etc.
    #+end_src
  - [ ] Create a tarball
    #+begin_src bash
        # tar czf ..
    #+end_src
  - [ ] Upload to s3
    #+begin_src bash
        # aws s3 sync ...
    #+end_src
```

The only problem is that these tasks need to be performed repeatedly
i.e.  every time I have to build and deploy the code. To address this,
the first thing I reached out to was
[(ya)snippets](https://github.com/joaotavora/yasnippet). In past, I've
used snippets quite effectively for recurring activities. For example,
I had a snippet that expanded to a template org tree for taking notes
during a meeting. There was another similar one for taking interviews.

But in case of build/deploy workflows, the expanded checklist is
practically of no use once all the items are checked off. In case of
meeting notes or interview notes, the information captured in the
expanded org tree during the meeting/interview is usually worth
retaining for future reference. Another problem with snippets was that
while performing the tasks if the checklist had to be updated due to
any deviation, I had to remember to update the snippet as well.

The next thing I tried out was to directly store the expanded
checklist in the repo with all items unchecked. Org being just plain
text, I can simply use `M-x query-replace` to uncheck all items again
after executing the checklist. When this worked well for me, I thought
it might be a good idea to wrap this into an interactive elisp
function and bind it to some key.

Now emacs has a funny way of always being one step ahead of you!
Whenever you find yourself thinking "wouldn't it be great if emacs
could do this?"  chances are it already can, or someone in the
community has already built a package for exactly that purpose. And
sure enough, there's
[org-checklist.el](https://orgmode.org/worg/org-contrib/org-checklist.html)
in org-contrib which does exactly what I want!

First you need to install the `org-contrib` package and require
`org-checklist` file in your `init.el`:

```elisp
(use-package org-contrib
  :ensure t
  :config
  (require 'org-checklist))
```

Then just set the property `RESET_CHECK_BOXES` to `t` in the org
tree. You may do this using `C-c C-x p` which will show a prompt for
property names and let you enter the value in the minibuffer. It will
also create the property tray if required.

Now my checklist looks something like this (individual tasks collapsed
for brevity),

```org
* TODO Build
  SCHEDULED: <2025-01-30 Thu .+1d>
  :PROPERTIES:
  :RESET_CHECK_BOXES: t
  :LAST_REPEAT: [2025-01-29 Wed 11:29]
  :END:
  - State "DONE"       from "TODO"       [2025-01-29 Wed 11:29]
  - [X] Generate SQL files using tapestry...
  - [X] Build backend...
  - [ ] Buiild frontend...
  - [ ] Create a tarball...
  - [ ] Upload to s3...
```

The org item is marked as `TODO` and a recurring schedule is set with
the `.+1d` cookie. When the state is changed to `DONE`, the following
things happen automatically:

1. all checkboxes get unchecked,
2. the time when the state was changed to `DONE` gets recorded,
3. the org item becomes `TODO` again and the scheduled date gets
   shifted to the next day

I may not actually end up running the workflow on the next day, but
the `.+1d` cookie ensures that even if it's repeated next after say 4
days, it won't consider the task as overdue for the previous 3 days <a
id="footnote-1-ref" href="#footnote-1"><sup>1</sup></a>.

The changes to the org files are committed in git, but I make it a
point do so only after the above side effects have taken place
i.e. the org entry is in `TODO` state and all items are unchecked
. This way the diff only contains the time when the checklist was last
executed.

With this workflow, there are no additional org entries created with
duplicate data that I'd have to archive later. If I have to update the
checklist during execution, I can do it there itself and commit the
changes in git. But more than anything this workflow feels so much
natural and native to org mode.

### Footnotes

<b id="footnote-1">1</b>. Not sure if I'm making sense here! Repeater
   cookies are explained with better examples in org mode
   [docs](https://orgmode.org/manual/Repeated-tasks.html). <a
   href="#footnote-1-ref">&#8617;</a>
