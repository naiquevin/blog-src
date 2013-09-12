Title: Does Firefox gets you into bad coding habits?
Author: Vineet Naik
Date: 2009-11-22 11:16:46
Category: firefox
Summary: 

We all know how good Firefox is and if something works in FF and
doesn't work in other browsers, we generally blame the others for not
being as good. Recently I have started to discover a downside of using
FF. I came across a few situations where FF was too lenient and I
could realize my mistake only upon (accidently) checking the code in
CHROME.

Let me give a few examples where FF covers your mistakes before I tell
you what I understood from it

1) Check out this
[example](http://www.noiseokplease.com/sampleCode/jqueryChrome). If a
certain element say 'A' is placed inside another element 'B' then FF
considers the parent-child relationship of A and B without giving a
damn about whether its a valid HTML markup or not.

So if I write some text directly inside a table tag, omitting the <tr>
and <td> tags it will blow up in any browser - even FF and the markup
will obviously not validate. But what if its an hidden input
field. You won't realize that its wrong unless you alert the value of
the the hidden field by using one of [jquery's](http://jquery.com/)
[DOM traversing mothods](http://docs.jquery.com/DOM/Traversing).. something
like,

```javascript
    $("#buttonInsideTD").click(function(){
        $(this).parent().parent().siblings().filter(':input').val();
    });
```

Please correct me if I am wrong, but logically its not valid
markup... because input cannot be a valid child of table. It fails the
[W3C validator](http://validator.w3.org/) (which says -- *document
type does not allow element "input" here*) and even eclipse throws
those annoying yellow coloured warnings .. But it makes no difference
to FF.

2) Ever tried parsing xml using jquery's
[$.find](http://docs.jquery.com/Traversing/find) method ? FireFox
parses it beautifully while Chrome and the others refuse to do it. I
once came across a message board where some one was cribbing of $.find
not working in chrome on an xml string. Infact I had come there in
search of exactly the same thing. Some briliant guy had answered it by
asking a counter question - *why should a browser parse xml if its
supposed to understand only html?* Sounds right!  But FF parses it and
without letting you know even one bit that what you are doing is
wrong. (The solution to make it work is by writing a separate function
that makes the xml suitable for parsing .. but that would be a topic
for another blog post)

3) Firefox doesnt have any problem with the following mark up

```html
    <a href=""><li></li></a>
```

But again, its wrong as per the standards.

So what I can understand from these examples is that Firefox treats
html like xml and doesnt care if html rules are obeyed or not. If
there are incorrectly coded elements in your document and the final
result doesn't show up in the browser, they will pass as valid html
and can only be detected if the source is tested for compatibility
with standards or some dom methods are used on them and that too if
checked in some other browser. (I am sure there is more to it than
just this and I might be wrong as well. So any corrections are
welcome.. )

So from now on its going to be simultaneous development and testing on
both Firefox and chrome. But Firefox still remains my default browser
for the firebug, the echofon, the frequent updates and every thing
that makes Firefox exemplify the true open source spirit.
