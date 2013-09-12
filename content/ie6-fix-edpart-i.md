Title: IE6 FIX-ed......Part I
Author: Vineet Naik
Date: 2009-05-06 03:44:44
Tags: IE6 fix, web development languages, CSS
Category: ie6
Summary: 

Imagine a scenario,

For past one and a half month you have been working hard on your
website, creating graphics in Ps, accurately positioning them along
with all the other components using CSS and adding 100 lines of new
code everyday... and then one day you read something about cross
browser compatibility issues and open the website in IE6 just to see
how it works there.

The feeling will be nothing less than what you will experience when
you forget to use Ctrl+S and power cut occurs..

Two weeks back, I had a similar feeling when I noticed that IE6
doesn't like my neatly made PNG images that use transparent
backgrounds.

So I 'googled' to see if I can get any help and to my surprise it
showed 368,000 results.

But only one fix yielded results. The one I found last night at
[http://www.twinhelix.com/css/iepngfix/demo/](http://www.twinhelix.com/css/iepngfix/demo/)

It was pretty easy, just paste the code in the header and it works
beautifully. Although someday I would like to take a look at what the
.htc file actually does, I guess this is not the right time to get
into such details.

But now I realize that this was just one of the problems...

Other than PNG,

1. Browser doesn't respond to links styled using CSS properly.

2. And the biggest blow is that the login script doesn't work! It
   calls the same .php file but nothing happens.. not even an error msg..

Hope, I ll be able to fix these problems soon. Off to 'google-ing'
fixes now.

Edit: Both of the above mentioned problems are solved. Please check
the 'CROSS BROWSER' page of this blog for the fixes.
