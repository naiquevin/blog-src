Title: Reduce testing while writing code
Author: Vineet Naik
Date: 2009-09-13 23:38:17
Tags: ajax, php, web development
Category: javascript
Summary: 

Very often it happens that more time goes into testing than writing code. Particularly when ajax is involved.

For example, imagine this scenario.. you are working on an online store and you want to allow a user to remove items from the cart using ajax. ie. when the 'remove from cart' button is clicked the item must disappear from the cart...<!--more-->

When the code is run for the first time, nothing happens! (Yes, it happens with me a lot of times :P). Thanks to tools like Firebug, it is confirmed that some silly javascripting mistakes are the cause..you try to fix and refresh the page to see if its working now. But the thing has now gone from the cart as there is no problem with the server side script. So, you have to  go back to the product page, add a few products, and come back to the cart to test. If it fails this time as well, repeat the same thing again. Loss of time.

I recently started using a reverse approach to avoid all this drama. In cases like these, I start with writing an action that only returns true to the call back function of the ajax request without making a server trip. If anything doesnt work at this stage then its definitely javascript at fault. Only when its fixed, that I write the remaining code. This way I have experienced that a considerable amount of time is saved for other activities like tweeting!

I have found this approach extremely effective when some irreversible effect is involved, mostly deleting something or in other cases such as adding an email address (or any other field) in a table where the email column accepts only unique values.