title: What is Emacs Lisp?
class: nobackground

- Dialect of the Lisp programming language
- Used by the Emacs text editor to implement most of the editing
  functionality
- Used to customize and extends emacs

Pretty much what makes emacs the programmer's editor

---

title: This talk
class: nobackground

Three parts

- Emacs Lisp as a programming language
- Editor related features of the language
- An example function to implement simple functionality

\+ Some live examples in between

---

title: One-slide intro to Lisp
class: nobackground

`L`ots of `I`rritating `S`illy `P`arentheses!

Or,

`LIS`t `P`rocessing

The syntax is entirely made up of lists, `almost` every expression
being a function call.

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (+ 1 2)
3
ELISP> (concat "hello" ", " "world")
"hello, world"
</pre>

The first element of the list evaluated to a function and applied to
the rest of the elements as arguments

---

title: Ways to evaluate expressions in Emacs
class: nobackground

- C-x C-e
- M-x {eval-buffer,eval-region,eval-defun}
- ielm (inferior emacs lisp mode)

---

title: Variable binding
class: nobackground

`set` and `setq` can be used for top-level bindings

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (set &#39;a 20)
20
ELISP> (setq a 20)
20
ELISP> (setq b 30 c 40)
40
</pre>

`setq` is a more convenient version of `set` which helps in two ways:

- takes care of quoting the symbol
- supports multiple bindings

---

title: Comments
class: nobackground

anything after semicolon is considered a comment (ie. ignored)

<pre class="prettyprint lang-lisp" data-lang="elisp">
; i am inside a comment
;; i am also inside a comment

(setq name "Vineet") ; me too a comment
</pre>

---

title: Primitive Datatypes
subtitle: [1/2..]
class: nobackground

- Numbers: 42, -100.05, 5e10, #b1010, #o37, #xabcd
- Boolean: `t`, `nil`
- Strings: "hello", "world"
- Symbols: `foo`

  Symbols are interned

  <pre class="prettyprint lang-lisp" data-lang="elisp">
  ELISP> foo
  \*\*\* Eval error \*\*\*  Symbol's value as variable is void: foo
  ELISP> 'foo
  foo
  </pre>

---

title: Primitive Datatypes
subtitle: [..2/2]
class: nobackground

- Cons Cells

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (setq p (cons 1 2))
(1 . 2)
ELISP> (car p)
1
ELISP> (cdr p)
2
</pre>

There are the most basic ones but there are many other primitive types
related to programming such as `vector`, `hash-table` etc. as well as
a few that are specific to emacs such as `buffer`, `frame`, `window`
etc.

---

title: Lists (Non primitive)
subtitle: 
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (1 2 3 4)
;; above will result in error
ELISP> (list 1 2 3 4)
(1 2 3 4)
ELISP> '(1 2 3 4)
(1 2 3 4)
ELISP> '() ; empty list 
ELISP> (equal &#39;() nil)
t
ELISP> (cons 1 '())
ELISP> (setq nums (cons 1 (cons 2 (cons 3 (cons 4 '())))))
(1 2 3 4)
ELISP> (car nums) ; first
1
ELISP> (cdr nums) ; rest
(2 3 4)
</pre>

---

title: Equality Predicates
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
;; comparing numbers
ELISP> (= 2 (+ 1 1))
t
;; checking for `same` objects
ELISP> (eq 1 1)
t
ELISP> (eq 'a 'a)
t
ELISP> (eq "hi" "hi")
nil
;; comparing objects with their content
ELISP> (equal (list 1 2 3) (list 1 2 3))
t
;; checking for string equality
ELISP> (string= "hi" (concat "h" "i"))
t
</pre>

---

title: Control Structures
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (if t "yes" "no")
"yes"
ELISP> (if (not t) "yes" "no")
"no"

ELISP> (when t "yes")
"yes"

ELISP> (cond ((> a b) 1)
             ((< a b) -1)
             ((= a b) 0))
</pre>

---

title: Local bindings
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (setq a 10)
10
ELISP> (let ((a 5)
             (b (+ a 1))
         (+ a b))
16
ELISP> a
10
</pre>

`let*` can be used if subsequent bindings need to use previous ones.

<br/>
<b>Note:</b> `set`, `setq`, `if`, `cond`, `let` etc. are <u>special forms</u> and
not functions

---

title: Doing stuff sequentially
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (progn
         (do-something)
         (do-something-else)
         (+ 1 2)
         (+ 3 4))
7
ELISP>
</pre>

usually code that uses `progn` involves side effects to be carried out
in order.

---

title: Function definitions
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (defun greet (greeting name)
         "Optional docstring"
         (concat greeting ", " name))
greet
ELISP> (greet "hello" "vineet")
"hello, vineet"
ELISP>

;; anonymous functions
ELISP> ((lambda (x) (+ 1 x)) 3)
4
</pre>

The result of the last expression of the function body is implicitly
returned

---

title: Dynamic Binding
subtitle: With support for Lexical Binding since v24.1
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (defun g (f)
         (lambda (x)
           (funcall f x)))
g
ELISP> (funcall (g (lambda (x) (+ 1 x))) 10)
*** Eval error ***  Symbol's value as variable is void: f

ELISP> (setq lexical-binding t)
t
ELISP> (defun g (f)
         (lambda (x)
           (funcall f x)))
g
ELISP> (funcall (g (lambda (x) (+ 1 x))) 10)
11
</pre>

---

title: Regex
class: nobackground

<pre class="prettyprint lang-lisp" data-lang="elisp">
(defconst sphinx-doc-fun-regex "^\s*def \\([a-zA-Z0-9_]+\\)(\\(.*\\)):$")

(defun sphinx-doc-fun-def (string)
  "Returns a pair of name of the function and list of the name of
  the arguments"
  (when (string-match sphinx-doc-fun-regex string)
    (list (match-string 1 string)
          (sphinx-doc-fun-args (match-string 2 string)))))
</pre>

<footer class="source">source: <a href="https://github.com/naiquevin/sphinx-doc.el/blob/master/sphinx-doc.el">sphinx-doc.el</a> [shameless plug]</footer>

---

title: Loading code
class: nobackground

`load-path`: list of paths where files to load are looked up

`eager loading`: load

`lazy loading`: autoload, "require"-ing provided features

---

title: Programming editor functionality
subtitle: Editor related types
class: nobackground

`buffer`, `frame`, `window` etc are editor related types

<pre class="prettyprint lang-lisp" data-lang="elisp">
ELISP> (current-buffer)
#&lt;buffer *ielm*&gt;
ELISP> (bufferp (current-buffer))
t
</pre>

---

title: Interactive functions
class: nobackground

Interactive functions can be called using `M-x <function-name>`.

They can also be associated to keys bindings.

When we type out a key sequence, emacs calls the bounded function.

<pre class="prettyprint lang-lisp" data-lang="elisp">
(defun some-function ()
  (interactive)
  ...)
</pre>

Evaluate the defun and then,

<pre class="prettyprint lang-lisp" data-lang="elisp">
M-x some-function
</pre>

---

title: Example
subtitle: Programmatically simulating user interaction
class: nobackground

Write the name of the current buffer with the message "Hi! You are
viewing the '&lt;buffer-name&gt;' buffer" on the next line with an indent of
8 spaces and then move the cursor back to the earlier position

---

title: Example
subtitle: What would the user do?
class: nobackground
build_lists: true

- goto next line
- type out 8 spaces from the beginning of the line
- type out the message along with the buffer name
- move to the older position

---

title: Example
subtitle: What will our function need to do?
class: nobackground
build_lists: true

- goto next line
- type out 8 spaces from the beginning of the line
- `get the name of the current buffer`
- type out the message with the name of the buffer
- move to the older position

---

title: Example
subtitle: Working Code
class: nobackground fill

<pre class="prettyprint lang-lisp" data-lang="elisp">
(defun buffer-greet ()
  (interactive)
  (let ((name (buffer-name (current-buffer))))
    (save-excursion
      (progn
        (next-line)
        (move-beginning-of-line 1)
        (insert "        ")
        (insert (format "Hi! You are viewing the '%s' buffer" name))))))
</pre>


