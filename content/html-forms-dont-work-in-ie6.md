Title: HTML forms problem in IE6 solved
Author: Vineet Naik
Date: 2009-05-12 17:28:55
Tags: $_POST['submit'], images as buttons, HTML, form, IE6
Category: IE6 issues
Summary: 

Ah relieved!... finally my website works on IE6. A big problem
solved

**Problem:**

Login and signup script not working in IE6. (works fine in FF &
Crome). On clicking the submit button, nothing happens, not even an
error msg.

**What was wrong? **

The problem was that I was using images as submit buttons in the HTML
forms and not checking form submission as per IE6's liking!

**Solution: **

HTML allows us to use images as submit buttons

In FF and Chrome (and may be other browsers as well which I dont use),
if we want to check if submit button is clicked and run a specific
code, then this serves the purpose

```php
    <?php
    if(isset($_POST['submit'])) {
        // code to be executed
    }
```

But IE passes the co-ordinates of click as ``submit_x`` and ``submit_y``
instead of just submit=parameter..

so to make sure that the form functions in IE, change the above code
to

```php
    <?php
    if(isset($_POST['submit_y']) || isset($_POST['submit_x'])) {
        // code to be executed
    }
```

This solved the problem in my case

Doing some more G tells me that even if we check just one co-ordinate
its fine.  But now I have already changed it, and I am too tired to
change it back again to something else... so I'll let that be.. :)

**Thanks to:** 

Webmasterworld forums, Google
