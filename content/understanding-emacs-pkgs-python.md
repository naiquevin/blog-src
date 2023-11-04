Title: Understanding Emacs packages for Python
Author: Vineet Naik
Date: 2023-11-04
Tags: emacs, python
Category: programming
Summary: An overview of emacs packages for Python, including a mild rant about confusing package names.
Status: published

Revisiting emacs config after a long gap can be challenging. There
might be some packages deprecated or no longer actively maintained
and/or replaced by newer ones. There are also chances that you don't
remember much about your own config, which is not uncommon. Often
elisp code gets copy-pasted from some where without complete
understanding of the packages.

Revisiting Python related setup can be even more unpleasant,
particularly due to a multitude of options with similar, confusing
names and overlapping functionalities. Well, that was my recent
experience while getting my existing config to work on a personal
laptop.

It's worth noting that my existing config, while functional on my
office laptop, had fallen behind by a few years. Meanwhile, the emacs
ecosystem has evolved and adopted new technologies such as [Language
server protocol
(LSP)](https://microsoft.github.io/language-server-protocol/)
etc. Additionally, the Python language itself has evolved in the
recent years. As there was no urgency to get the personal laptop up
and running, it was the perfect opportunity to commit to some
[yak-shaving](http://www.catb.org/~esr/jargon/html/Y/yak-shaving.html)!

The first puzzle was to understand how the config worked on the other
laptop in the first place. The second task was to evaluate the newer
packages and decide whether it'd be better or worse to switch to them.

Having done this exercise of _modernizing_ the config, I believe I
have a decent understanding of the different emacs packages for
python, at least the ones I've used or evaluated. In this blog post, I
want to give an overview of the emacs ecosystem for python and clarify
some of the confusion around packages with similar names. My intention
is to keep it informative rather than coming across as a rant.


### Python modes

Let's first talk about the Python major mode variants. There couldn't
be a better example of _"multiple packages with confusing names"_.

The default mode for python built into emacs (since version 24.2 and
as of 29.1) is called `python-mode`. Not to be confused with (wait for
it!)
[python-mode](https://gitlab.com/python-mode-devs/python-mode). The
latter claims to be "the longest continuously maintained Emacs major
mode for editing Python code".

Before 24.2, the python major mode packaged with emacs was called
`python.el`. After it was replaced, it was extracted out into a
separate package, [python-el](https://github.com/leoliu/python-el).

As far as I remember, I have always used whatever mode that emacs came
with at any given point in time. I could never tell any difference, so
it's OK for me to stick to the default. That's one less thing to
manage.

### Jedi

[Jedi](https://jedi.readthedocs.io/en/latest/) is python
package/library that provides auto-completion, static analysis and
refactoring utilities. Plugins specific to different editors and IDEs
can be built on top of it. It's `jedi` that does the heavy lifting in
most of the emacs+python tooling that I've come across.

### jedi.el

[jedi.el](https://github.com/tkf/emacs-jedi) is a Python
auto-completion package for emacs that uses `jedi` (the python
library) under the hood. Bad choice of name considering that the
underlying `jedi` provides much more than just auto-completion.

Another source of confusion is that the name of the repository on
github is `emacs-jedi` but everywhere in the README it's referred to
as `jedi.el`. In other words, `jedi.el` and `emacs-jedi`
are essentially the same. Henceforth in this post, the emacs package
will be referred to as `jedi.el` and the python package as `jedi`.

`jedi.el` uses `EPC`, an RPC protocol for emacs lisp, to communicate
with a python process for retrieving completion candidates. This is
implemented using two transitive dependencies:

1. The emacs package
   [emacs-epc](https://github.com/kiwanami/emacs-epc) which is used by
   `jedi.el` to implement the EPC client in emacs.
   
2. The python package [python-epc](https://github.com/tkf/python-epc)
    which is used to implement the server side <a id="footnote-1-ref"
    href="#footnote-1"><sup>1</sup></a>.
    
To display the auto-completion candidates, `jedi.el` uses the
[auto-complete](https://github.com/auto-complete/auto-complete)
package.

`auto-complete` and `epc` are not actively maintained at present which
is one of the reasons I was considering alternatives. That brings us
to..

### company-mode

[company-mode](https://github.com/company-mode/company-mode) is a
generic auto/text completion framework for emacs. It has "backends"
for retrieving completion candidates and "frontends" for displaying
them. It supports extensibility via pluggable backends and frontends.

An important distinction between `auto-complete` and `company-mode` is
that the former is used like a library whereas the latter is more like
a framework. For example, `jedi.el` calls functions from the
`auto-complete` package. Whereas, a company backend can be implemented
as an elisp function which when "registered" in the list of global
backends, will be invoked by `company-mode` at the right time and
place.

```elisp
    (add-to-list 'company-backends 'my-company-backend)
```

Most importantly, company mode is actively maintained, has good
support for different languages and seems better in terms of
extensibility.

### company-jedi

[company-jedi](https://github.com/emacsorphanage/company-jedi) is an
emacs package that implements a company backend for Python using
`jedi`.

I had briefly installed `company-jedi` until I realized<a
id="footnote-2-ref" href="#footnote-2"><sup>2</sup></a> that `eglot`
also comes with a company backend to support auto-completion out of
the box.

### LSP and eglot

In today's date if you're not using LSP, I'd highly recommend you
do. I procrastinated for too long.

Just like EPC, LSP also requires client and server components. There
are two popular LSP clients for emacs: 

1. [eglot](https://github.com/joaotavora/eglot)
2. [lsp-mode](https://github.com/emacs-lsp/lsp-mode)

I have tried both with python and rust so far<a id="footnote-3-ref"
href="#footnote-3"><sup>3</sup></a> and decided to settle with eglot.
It covers most of my use cases and to me felt faster and actually
light weight as advertised. Additionally, the latest version of emacs
29.1 comes with eglot built-in.

eglot's documentation lists 4 server implementations for python
(there could be more). Following the _confusing-names_ tradition, they
are:

1. [python-language-server](https://github.com/palantir/python-language-server)
   (_alias `pyls`_): Supports python 2.7 but not actively maintained
   since 3 years.
2. [python-lsp-server](https://github.com/python-lsp/python-lsp-server)
   (_alias `pylsp`_): Seems like an actively maintained fork of
   python-language-server but only for Python 3.8+.
3. [pyright](https://github.com/microsoft/pyright): It's actually a
   static type checker for python by Microsoft but includes a language
   server as well.
4. [jedi-language-server](https://github.com/pappasam/jedi-language-server):
   Actively maintained.
   
Interestingly `pyright` is written in Typescript/Javascript while rest
of them use `jedi`.

I am using `jedi-language-server`. It's the first one I tried and it
feels adequate<a id="footnote-4-ref"
href="#footnote-4"><sup>4</sup></a>. 

At first, `eglot` does feel a bit magical as a lot of things will
start working out of the box. It has "soft dependency" on some popular
packages such as `company-mode`, `flymake`, `yasnippet` i.e. if these
packages happen to be installed and enabled then `eglot` will
automatically upgrade to provide those functionalities. Thankfully
it's possible to opt out of these. For e.g. I prefer `flycheck` to
`flymake`, so I can opt out of `flymake` as follows,

```elisp
    (add-to-list 'eglot-stay-out-of 'flymake)
```

### virtualenvwrapper

I was a long time user of the python tool
[virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) but I
don't use it anymore since moving to the
[venv](https://docs.python.org/3/library/venv.html) module that comes
with Python 3.3+.  However I continue to use the emacs package
[virtualenvwrapper](https://github.com/porterjamesj/virtualenvwrapper.el). Although
it is feature compatible with the underlying python tool, today my use
of it is limited to just activating and deactivating envs.

With minor workarounds, I have managed to get it working with
virtualenvs created using the built-in `venv` module in python.

As `virtualenvwrapper` (the emacs package) sets the correct env vars
in the context of the emacs process, it plays well with eglot too<a
id="footnote-5-ref" href="#footnote-5"><sup>5</sup></a>.

Besides this, I just know one other alternative for virtualenv
functionality inside emacs,
[pyvenv](https://github.com/jorgenschaefer/pyvenv) which I haven't
tried.

The whole package management ecosystem too has evolved in the recent
years with advanced tools such [poetry](https://python-poetry.org/). I
don't use poetry but there must be an emacs mode for it.

### Other packages

Besides these, I am only using 2 other packages for python development
in emacs: 

1. [pytest-el](https://github.com/ionrock/pytest-el) which is pretty
   minimal and works perfectly.
   
2. [sphinx-doc](https://github.com/naiquevin/sphinx-doc.el) for
   generating docstrings and which I'm the author of. I am ashamed
   that it's not actively maintained. It still works for untyped and
   unformatted (by black etc.) python code.
   
### Final thoughts

So that was my renewed understanding of the different emacs packages
for python development. It is specific to my config (which can be
found
[here](https://github.com/naiquevin/emacs-config/blob/master/config/python-config.el))
and not exhaustive by any means. But I believe I've covered most of
the functionality you'd ask from a Python IDE. I hope it helps any one
in a similar situation.

One observation I have is that while emacs is known for its
stability, the ecosystem of third party packages is quite fast
moving. So like me, if you update your config only after a few years,
there is a lot to catch up with. Many alternatives providing
overlapping functionality and confusing package names don't help.

But in the end, there's not much to complain. It's incredible that all
this software is free and open source and it works if you put some
efforts from time to time. Also, yak-shaving is extremely satisfying!

---

### Footnotes

<b id="footnote-1">1</b>. The `python-epc` package actually provides
both server and client implementations<a href="#footnote-1-ref">&#8617;</a>

<b id="footnote-2">2.</b> It took me a better part of the day to
figure out that `company-jedi` was not actually being used and it was
`eglot` that was doing the auto-completion. This can be a separate
blog post but I'm adding it here to preserve the context.

Before adding `company-jedi` to my config, I had uninstalled `jedi.el`
along with its (now) unused dependencies namely `emacs-epc` and
`python-epc`. From the name, it's reasonable to believe that
`company-jedi` must be depending on `jedi`. So I was curious about how
it worked in the absence of `epc`.

Looking at the source code and dependencies lead to more questions!
`company-jedi` depends on a package named `jedi-core` having the
description (as displayed on melpa) "Common code of jedi.el and
company-jedi.el". Interestingly, there's no repo named `jedi-core` on
github or anywhere else. The link on melpa points to the same repo as
`jedi.el` and this is the only place where you can find a file named
`jedi-core.el` with a heading comment same as the above
description. With `jedi.el` definitely not installed, where was the
source for `jedi-core.el` coming from?

The answer is hidden in its [melpa recipe
file](https://github.com/melpa/melpa/blob/master/recipes/jedi-core). `jedi-core`
is built using selected files from the `jedi.el` repo. That still
doesn't answer the original question - how did `company-jedi` work
without `epc`.

So I uninstalled `company-jedi` but while still initializing
`company-mode` in the `after-init-hook` of `python-mode`. Auto
complete continued to work. Turned out that `eglot` was providing auto
completion with the help of `company-mode` and
`jedi-language-server`. Even though find this out was painful, overall
it was a #win to avoid a bunch of packages. <a
href="#footnote-2-ref">&#8617;</a>

<b id="footnote-3">3</b>. I haven't tried eglot with Clojure
yet. Earlier I had attempted to use `lsp-mode` with Clojure but
discarded that config due to collisions with `cider-mode` which is
indispensable to my workflows. Another reason is that I haven't
written any Clojure on my personal laptop yet. <a
href="#footnote-3-ref">&#8617;</a>

<b id="footnote-4">4</b>. Not having used typed python much, I'm not
sure how `jedi-language-server` compares with `pyright` in that
respect. <a href="#footnote-4-ref">&#8617;</a>

<b id="footnote-5">5</b>. With some configuration and the requirement
that the virtualenv is activated before the eglot process
starts. Perhaps a topic for another blog post <a
href="#footnote-5-ref">&#8617;</a>
