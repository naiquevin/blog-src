Title: Own the Editor
Author: Vineet Naik
Date: 2012-05-11 23:28
Category: emacs
Summary: On getting the most out of the editor of your choice
Status: published


Recently I have noticed a changing trend in the choice of text editor/IDE among my
colleagues. From 100% Eclipse users a few months back, today we have -

6 [Sublime Text 2](http://www.sublimetext.com/) Users  
3 [Eclipse](http://www.eclipse.org/projects/) Users  
1 [Vim](http://www.vim.org/) User  
1 [Emacs](http://www.gnu.org/software/emacs/) User  

I am the lone emacs user which you would already guessed from the
tagline of this blog. This post is not about emacs though.  I used
Eclipse for a long time until I discovered Emacs which was about 1
year ago. I don't regret switching to emacs, but looking back, I admit
that I wasn't a good eclipse user then because I never really used it
beyond writing code and using it's subversion client for version
control.  So, while it's good to see people moving to Sublime Text2 (a
fine editor) and Vim (an awesome editor) from IDEs which I personally
hate, it's important to realize that an editor will work wonders for
your productivity only when you learn to use it to it's full potential
and it's only then that you can appreciate the awesomeness of it.

The point I am trying to make here is that whichever editor/IDE you
choose to use, you must use it like YOU OWN IT! If you are a
programmer, then the editor is your primary toolkit because you spend
more than 60% of your time inside it and so there is no reason for not
trying to master it.

This post is about what you must look for in an editor for efficient
and enjoyable editing and it will also try to cover some of the must
know tricks irrespective of which editor you use.  Your editor may not
support all these features but there is a good chance that they do and
you haven't yet had the time or reason to discover them.  So if you
think that you are only complacently using your editor and not getting
the most out of it, I think this post will show you some direction.

### A few important points first

Firstly, I don't claim to be an emacs guru although I am a passionate
user.  Secondly, in this post, you will find that I have mentioned
emacs a lot of times although having said that the post is not about
it. The intention is not to annoy the readers. Wherever applicable, I
have mentioned how to do a particular thing in emacs or the term used
for it so you can then easily google it up for some other editor as in
"abc equivalent of emacs in X editor" or "How to do abc in editor X?".

### Terminology

Like many other things, before you can dive deep into something, it's
very important to have an understanding of the terms that other folks
in the community use to describe different things related to the
editor.  Unless you are familiar with the terms and their meanings you
will not be able to communicate on mailing lists and forums where
there are a lot of people with talent and readiness to help you out.
So get yourself familiar with atleast some of the basic terminology
first.

### Shortcuts and mouse-less editing

Knowing and using shortcuts is a key to faster editing. As a quick
example, it's obviously faster to type ctrl-s than clicking on File >
Save. A killer thing about text editors such as vim and emacs is
economy of motion, which means that the shortcuts and key sequences
are specifically designed in such a fashion that it's easier and
faster for the fingers to type. Well this makes them time consuming to
learn and get used to initially, but if you make a determined effort
then very soon they are registered into muscle memory and you hardly
have to think while using them.

Another thing is that using mouse is not particularly efficient while
writing code so you should avoid that as much as possible.  Learning
shortcuts fixes this.  In the rest of this post, when I say "learn how
to do x" I always mean learn the shortcut or the command to do it.

### Moving around

Imagine how much time you could save if you were able to go back to
the line of code where you want to paste stuff that you just copied or
open the file where a particular function is defined. Invest some time
in learning how to move across code and files fast and with minimum
effort.

### Searching

If you are using vim or emacs, then you will quickly realize that
searching is an efficient way of moving around. A good editor treats
files, directory listing, configuration interface etc consistently
which means that you can move around these interfaces in the same way
as you do in files. Search in files (rgrep in emacs) is a handy tool
as well.

### Cut/Copy/Paste and the "kill ring"

It's indeed convenient if the editor remembers what all things were
cut or copied in current session and doesn't lose them the moment
something else is copied to the clipboard. It's also important that
you are able to quickly move around the clipboard contents. In emacs
there is a kill ring where anything that's *cut* or *killed* goes and
anything that's *pasted* or *yanked* comes from.

### Lines

As programmers we deal with lines of code, so we must know how to work
with lines.  For eg. deleting to end of line, deleting a line (moving
up the next one), adding a line after the current one (from any
position in the current line) taking the cursor there ready to type,
adding a line before the current one and moving to it to quickly add a
doc string, going to the next line respecting the indent (electric
return), swapping two lines and a lot of other things.

### Region

It helps to know how to work on a region of code or text. For
eg. indenting a region to right/left, Commenting/uncommenting a region
and doing things that you normally do in files only on this region
such as search/replace in region, undo/redo in region (yes this is
possible in emacs)

### File Browsing

Do you have to click on File > Open > Select > Open to open a file in
the editor? If yes, you should change your editor!  Other file
operations such as new file, delete, move, delete directory
recursively are similarly important.  Added bonus if it also allows
chmod and chown. In emacs, all these things are possible in the dired
buffer.

### Screen Splitting

Often we need to go back and forth between many files to refer to
function definitions, example usage, tests, shell sessions etc.  A
handy feature to have in this case is to be able to view many files at
a time on the screen. Most editors support screen splitting in a
number of ways.  Find out which one works for you and use it to reduce
effort of moving between files.

### Jump to function definition

Most editors provide a better and faster way for this than searching
in files. In emacs this can be achieved by generating a TAG table
which is basically just a file that acts as an index.

### Autocomplete

In a single editor, there can be many types of autocompletion
implementations and most of them are very handy and would probably be
the most used in day to day editng. For eg. in emacs we can define
abbreviations which are stored in files and can be expanded by TAB
key. Then there are dynamic abbreviations (M-/) or more sophisticated
Yasnippets which are capable of expanding to commonly used code
templates. I am not a Yasnippets user although I use the other two
types all the time.

### Polyglot friendliness

If you use multiple languages, learn how to configure the editor
differently for various languages for eg. I use 4 spaces indent for
python, php and javascript whereas 2 spaces for ruby and html.

### Source Control from editor

As a Git user, I am happy with the command line and don't use any
emacs git mode myself. But I think it is something worth learning and
considering trying out [Magit](https://github.com/magit/magit) since a
long time but haven't had the time yet.

### Running Shell inside the editor

This is a powerful and must have feature for any editor. I personally
use it a lot when I am trying out stuff in python or scheme. You can
even evaluate a region.

### Plugins and Extending the editor

Usually, editors have a good plugin ecosystem. If you use an
opensource editor, you can even search github repositories for plugins
that you wouldn't have imagined could exist. Learn how to install or
set them up and also aim towards learning how to write them yourself
and give back to the community.

### Syntax Checking and Lint

Any decent editor supports on the fly syntax checking of code. This
would typically be packaged as a plugin or a mode. There are also
tools that help you find out on the fly whether your code is code
style compatible for eg. whether your python code is
[PEP 8](http://www.python.org/dev/peps/pep-0008/) compliant or not.

### Support for non-programming formats

Chances are that your editor has support for editing files other than
programming languages. For eg. markdown or restructured text.  It's
very handy to have such a feature as it makes editing documentation
convenient.

### Macros

Macros provide a way to record a set of actions so that they can be
replayed again. As an example, the first non-trivial macros I had used
was for converting a paypal integration form in html to a python
dictionary of parameters to be posted to paypal. It took me around 5
mins to record it and 1 min to repeat it on all the form fields
clearly saving me a lot of time and shit work.

### Have fun

It's fun to be able to use your editor for a things for which other
people use softwares that flood the screen with popouts such as email,
irc or even twitter clients, note taking apps or even games.

So this is all I can think of right now. It's definitely by no means
an exhaustive list but I hope this helps you get started with fast,
efficient and enjoyable editing.
