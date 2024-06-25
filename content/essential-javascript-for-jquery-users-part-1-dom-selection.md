Title: Essential Javascript for Jquery users (Part 1 : DOM Selection)
Author: Vineet Naik
Date: 2010-08-24 12:07:11
Tags: jquery, HTML, web 2.0, javascript, web development
Category: javascript
Summary: 
Status: published

I remember when the first time I tried to learn some Javascript for
accomplishing basic form validation, it wasn't as simple as HTML and
CSS or even PHP for that matter. Plus being unfamiliar with stuff like
[Firebug](https://addons.mozilla.org/en-US/firefox/addon/1843/) in the
early days of programming, doesn't help. So there was a time when,
having not realized the power of the language yet, I looked to avoided
JS wherever possible. Then Jquery happened. And it was life
changing. Life changing because it not only made doing things easier,
but also eventually made me like the vanilla flavour of javascript.

Now usually there is a thing with frameworks and libraries that they
will work for you only if you know the basics clearly. After all
frameworks are build using the basics right. But in my opinion jquery
is an exception. People will disagree but let me put it this way - if
you have just started with jquery, after some initial copy pasting a
time will come when you will fairly undertand how 3 things work, the
jquery syntax, the methods, and how these two fit together. After that
you can easily make fancy things work without advanced javascript
knowledge until one of the readymade plugin breaks or your client
comes up with an insanely out of the box requirement. Then you will
have to go to vanilla and probably learn to use things like OOP,
patterns as well. And it will all be for the good. This is my personal
experience.

Okay, coming to the point, this blog post is the first one of the
series on some essential javascript knowledge you must have if your
case is similar to mine ie already doing pretty well with jquery but
not confident enough if that small file of minified code is taken away
for whatever reason. Apart from that, for me, being able to write long
and informative blog posts is going to be one of the motives behind
learning something I know I am hardly going to use in the presence of
jquery but which is very important.

The first few topics will cover basic things which are actually left
redundant by the awesomeness of jquery, but i guess it will be a good
starting point.

So lets get started with Part 1 : DOM selection. (I am assuming the
reader is familiar with the acronym
[DOM](http://www.w3schools.com/htmldom/default.asp).)

``$("selecter")`` in jquery makes selecting elements from the document
real easy right ? But how to do it using plain js ?  There are
different ways depending upon the element.

**Selecting by id**

```html
<div id="myid"></div>
```

```javascript

//select the first div by its id
$("#myid") //jquery
document.getElementById("myid"); //plain js

// note that plain js selector properties and methods cannot be
// applied in the first case as the plain js way returns an object
// while jquery returns an array of js objects. in this case the
// length will be 1 as we are getting it by id. To use it any way
$("#myid")[0].style;
```

**Accessing by Tag Name**

```javascript
document.getElementsByTagName("ul");
```

Notice the getElement**s** This will return an array of size equal to
number of ul elements in the document

**Accessing Children of elements**

In js all elements are referred to as nodes of the DOM tree.

```html
<div id="childtest">Hello world. Now check this <a href="">link</a></div>
```

```javascript
var arr = document.getElementById("childtest").childNodes;
```

The output if logged in firebug console will show an array of all
children of the element childtest selected. But it will be different
from what ``$("#childtest").children()`` will return.

**TextNode and accessing the text**

If you have already logged the above example to a firebug console, you
can see that apart from the actual child element ie anchor tag, it
also shows a Textnode (which is skipped by the jquery
``$("#childtest").children()`` code). To get its value just select
that particular child and get the property 'nodeValue'. This is how
the jquery ``.text`` method does the job.

```javascript
document.getElementById("childtest").childNodes[0].nodeValue;
```

**Accessing the siblings**

Jquery lets us get all siblings of an element as an array. Javascript
gives us only the next and the previous sibling Something like this

```javascript
document.getElementById("childtest").childNodes[0].nextSibling;
// or  ...childNodes[1].previousSibling
```

So how to get all siblings of an element? Well, to do this, first we
can traverse to an elements parent and then get all its childNodes.

**Accessing the parent element**

As simple as it can get

```javascript
document.getElementById("childtest").childNodes[0].parentNode;
```

So, this was pretty much about selecting the elements. In the next
part we will see how to manipulate them by dealing with css and also
how to make fancy things.
