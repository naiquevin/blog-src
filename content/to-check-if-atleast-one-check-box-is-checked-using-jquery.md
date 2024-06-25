Title: To check if atleast one check box is checked using Jquery
Author: Vineet Naik
Date: 2009-08-04 23:32:45
Category: jquery
Summary: 
Status: published

It happens so many times that I need to code something to make the UI
fool proof. While I have the logic clear in my mind, i often find that
javascript is of little or no help at all.... Whats amazing is that
99% of the time jquery does the trick with minimum code and the
'why-didnt-i-look-up-the-docs-first' feeling strikes!!

Jquery can be used as follows to check if at least one checkbox (any
input field actually) from a number of checkboxes is selected before
submitting the form on the client side. I came across this when I was
trying to figure out a way for similar validation when the number of
check boxes was driven by the database and it was not possible to have
a common className for them.

```javascript
function validateCheckbox() {
    var n = $("input:checked").length;
    if(n == 0) {
        return false;
    } else {
        return true;
    }
}
```

``input:checked`` matches all the check boxes which are checked.
