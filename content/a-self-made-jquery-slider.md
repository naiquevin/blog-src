Title: A self made Jquery slider
Author: Vineet Naik
Date: 2009-08-23 23:47:23
Tags: javascript, jquery, slider, web development, image slider
Category: javascript
Summary: 
Status: published

Now this post has been in the drafts section for quite some
time.. infact some posts which I started to write later made their way
to the blog before this one.. Anyway, here it is!

When one of our clients asked for a slider to show featured products
on his online store, I felt before going for the ready made plugins
available on the internet, I could try to create one on my
own. Although it would be wrong to call this a plugin, it did turn out
pretty well. Finally we decided to use JCarousal (as its obviously far
better), but thats a different story.

Anyways I am posting it here as its done by me. I would be glad if
anyone finds it helpful.

It is done using Jquery so you will need to download and include the
[jquery library](http://docs.jquery.com/Downloading_jQuery) to try it
out. Here is the code and a
[working demo](http://www.noiseokplease.com/slider/test.html)

JAVASCRIPT

```javascript
    var leftCount = 1;
    var rightCount = 1;
    var itemCount = 0;
    var stripCount= 5;
    var itemWid = 100;
    var itemPad = 10;
    var lastScr = itemWid + itemPad;
    $(function(){
        $('.item').each(function(){
            itemCount++;
        });
    });
    function moveRight() {
        if(rightCount <= (itemCount - stripCount) && rightCount <= 0) {
            $('#switcher').animate({left:120 * rightCount}, 'slow');        
            rightCount++;
            leftCount--;
        }
    }

    function moveLeft() {
        if(leftCount <= (itemCount - stripCount)) {
            $('#switcher').animate({left:-120*leftCount}, 'slow');
            leftCount++;
            rightCount--;
        }
    }
```

``moveLeft`` and ``moveRight`` are the functions that do the trick.

HTML

```html
    <body>
        <div id="container">
            <div id="switcher">
                <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
    	    <div class="item"></div>
            </div>
        </div>
        <div id="button">
            <a onclick="moveRight();">&laquo;Prev</a>
            &nbsp;
            <a onclick="moveLeft();">Next&raquo;</a>
        </div>
        <div id="dummy" style="display:none;"></div> 
    </body>
```

Finally, CSS

```css
    body {
        margin:0 auto;
        padding:0;
    }
    #container {
        margin:50px auto;
        width:590px;
        overflow:hidden;
        border:1px solid black;
        height:145px;
        -moz-border-radius:10px;
    }
    #switcher {
        position:relative;
        width:20000em;
        height:120px;
        padding:20px 10px;
        overflow:hidden;
        padding-left:10px;
    }
    .item {
        position:relative;
        width:100px;
        height:100px;
        float:left;
        margin-right:10px;
        border:1px solid black;
        background-color:#fad144;
    }
    #button {
        clear:both;
        margin:30px 340px;
        cursor:pointer;
    }
```

There are two important things to be noted in the CSS:

1. Position relative to the switcher and item and,
2. Overflow hidden to container and switcher

Another important thing to be noted is that moveRight is called
onClick of Previous button and moveLeft is called upon the click of
next button. This is because moveRight pulls the content to right
making the 'previous' content visible. Same logic goes for next
button.

Now the limitations. If you are a pro you might have already noticed
the super normal width given to the switcher div. It is to accomodate
more number of items. If the width is less, say 1000px and the items
are more, then the extra items will move down.

I am currently trying hard to find time for working on this defect :)
and also to turn this into an easy-to-use plugin.

Note: I admit its not a plugin, but I am posting this here anyway. In
case you are a pro web developer, this may not excite you as much as
it excites me. Your comments, suggestions etc. are always welcome.
