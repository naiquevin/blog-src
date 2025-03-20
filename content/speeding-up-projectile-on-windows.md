Title: Speeding up projectile on Windows
Author: Vineet Naik
Date: 2025-03-20
Tags: emacs
Category: programming
Summary: How to configure projectile in emacs to fix the sluggishness on Windows
Status: published

Last few months, I've occasionally needed to run emacs on Windows. In
a previous [post]({filename}/emacs-config-debt.md) I wrote about how I
got my emacs config to work on Windows, which initially seemed
sufficient. But every time I switch from Linux (or even MacOS) to
Windows, I notice new sluggishness in some or the other component!
Most recently, it was projectile.

Have you ever experienced typing a command on a remote server over a
slow SSH connection? Muscle memory doesn't just involve your fingers
recalling commands and key bindings&mdash;it works on the entire
sequence of actions you intend to perform. When I press the keybinding
to find file in a project, my fingers have already moved on to the
next steps i.e. quickly filtering the results and hitting enter. I
anticipate the file list to appear almost instantaneously, and if
there's a lag of even a few seconds, it's frustrating and not a mere
inconvenience.

To make it worse, the project I was working on had a large number of
files. The delay in displaying the file list was a bit too much to
deal with. I had to drop everything else and fix it on priority!

After going through the projectile documentation and some tinkering I
was able to solve it rather quickly (all thanks to the well written
docs). The answer lies in projectile's default config for indexing
files on Windows v/s Unix-like platforms. Here indexing means
compiling the list of files from the project that the user may want to
open. You can inspect the `projectile-indexing-method` variable to
check which method is currently in use.

The default indexing method is `alien` on all operating systems,
except on Windows where it's `native`. The `native` indexing is
implemented in emacs lisp and hence is portable i.e. works on all
platforms. The `alien` indexing method on the other hand shells out to
external tools such as `git` or `find` to obtain the list of files
from the project. For e.g. if your project uses git for version
control, it asks git to provide the list of files. An advantage of
this method is that your `.gitignore` file will be automatically
considered.

`native` indexing can be much slower on projects that contain many
files and deeply nested directories and setting it to `alien` can
speed it up significantly in those cases. But the problem is that
`alien` requires Unix tools that are not expected to be installed
Windows, which is the reason why it's not set as the default.

But that doesn't mean you can't use `alien` on Windows. You can
install [Cygwin](https://www.cygwin.com/) or something similar which
provides the required Unix and GNU tools for Windows.

```powershell
choco install Cygwin
```

Here I am using [Chocolatey](https://chocolatey.org/) to install
Cygwin.

Make sure that the binaries are accessible on `PATH`. In my case
Cygwin was already installed but wasn't on `PATH`. To do so, you may
permanently edit the `PATH` environment variable from Advanced System
Settings. But I prefer to set it inside emacs itself:

```elisp
(setenv "PATH"
        (concat
         (getenv "PATH")
         ";"
         "C:\\tools\\cygwin\\bin"))
```

Notice that the delimiter on Windows is a semicolon `;` and not colon
`:` as in case of Linux.

All that remains now is to set the indexing method to `alien`:

```elisp
(setq projectile-indexing-method 'alien)
```

And that should fix the sluggishness. But there is scope for further
optimization through caching. When the indexing method is `native`,
projectile implicitly enables caching. This means by changing it to
`alien` we've also unintentionally disabled caching. So enable it
explicitly.

```elisp
(setq projectile-enable-caching t)
```

If your project has an unusually large number files, you may also set
it to `persistent` which will persist the cache on disk so that it can
be used across emacs sessions.

If you use the same config on multiple OSs, you may add all
this windows specific code conditionally as follows,

```elisp
(when (eq system-type 'windows-nt)
  (setenv "PATH"
          (concat
           (getenv "PATH")
           ";"
           "C:\\tools\\cygwin\\bin"))
  (setq projectile-indexing-method 'alien)
  (setq projectile-enable-caching 'persistent))
```

---

### References

- [Projectile documentation](https://docs.projectile.mx/projectile/configuration.html)
