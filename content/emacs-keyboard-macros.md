Title: Keyboard macros in emacs
Author: Vineet Naik
Date: 2011-07-16
Tags: emacs, editing, macros
Category: emacs
Summary:

Just learnt how to set and use Keyboard Macros in emacs. This looks
pretty useful and something I feel will come in handy while
refactoring code.

Firstly, to set a keyboard macros means recording a sequence of
actions (keystrokes) and saving them. Later you can ask emacs to just
repeat them for you whenever you want using a single command.

Setting macros is quite simple,

``C-X (``  ......begin a macro definition

``...<do some keystrokes that you want to record>...``

``C-X )``  ......end the macro definition

Now to "play" your recording anywhere, all you need to do is ``C-X e``

Lets imagine a screnario:

In a php class (say a controller in an MVC application) the following
expression is written a number of times to get a particular request
param and assign it to a variable

```php
    <?php
    $id = $this->request->param('id') .............. $user_id = $this->request->param('user_id');    
```

Suppose I want to pass a second optional parameter of value ``0`` to 
all of the function calls ie change them such as,

```php
    <?php
    $this->request->param('id', 0);
```

To do this using a macro, 

move to the beginning of the buffer by typing ``M-S-<``. 

Begin the macro definition ``C-X (``

Incremental search for ``$this->request->param`` using ``C-s`` and then ``RET``

end of line ``C-e``

backward twice ``C-b * 2``

type ``, 0``

end macro definition ``C-X )``

Now keep doing ``C-X e`` till all the method calls are modified.

(This was somewhat a vague example but I hope you get the idea :-))
