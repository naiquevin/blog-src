Title: Identifying clicked mouse button in IE &amp; other browsers
Author: Vineet Naik
Date: 2010-07-28 23:37:34
Category: javascript
Summary: 
Status: published

Last month I spent some hours coding the popular game
[minesweeper](https://github.com/naiquevin/mines) in javascript. It
was a fun project. And as it has always been, fun projects are the
best ways to learn something new. Add to that the universal reach of
web applications. So apart from coding, putting it up on the server
and getting your friends and their friends to play the game <del
datetime="2010-07-26T17:47:42+00:00">while frequently checking the
analytics</del> was an equally enjoyable experience.

But after putting it up, just when the game was getting its share of
attention and people were liking it, one of my friends informed that
it didn't work in IE8. Now IE has always been infamous for its ways
and usually its just the IE6. But in this case even IE7 and IE8 had
joined the party.

Getting to the central idea of this blog post - Identifying which
mouse button was clicked is essential in minesweeper as it is played
using the mouse :) and there are three possible moves for a player at
any given time, which are, left click, right click and both buttons
clicked at the same time.

Jquery makes identifying the clicked button very easy with the event
object being passed to the callback functions of the mouse events
by-default.

```javascript
$(".cell").bind('mouseup',function(e){
    var button = e.button; //this will return the mouse button as int</p>
});
```

When I checked, the problem was with mouse button detection. As I
said, e.button will return an integer. Sadly, it means different
things in IE and other browsers.

For smarter ones:  
0 = left button; 1 = both buttons or the scroll wheel ; 2 = right button

For IE:  
1 = left button ; 2 = right button ; nothing for both buttons :|

Obviously the solution was having different conditions for IE and the
other browsers. Now comes the best part. Detecting the browser. This
is the most compact and insane hack I have ever come across for
IE-detection (courtesy:
[http://dean.edwards.name/weblog/2007/03/sniff/](http://dean.edwards.name/weblog/2007/03/sniff/)
)

```javascript
var IE = /*@cc_on!@*/false;
```

In all IE versions, the ``/*@cc_on!@*/`` part will evaluate to ``!``
(not) and thus the value of IE will be true while in other browsers it
will be false.

comments closed as some bastards are at work.
