Title: HTML link color problem solved
Author: Vineet Naik
Date: 2009-05-14 17:21:00
Tags: hover, Chrome, IE6, HTML, link color, CSS
Category: IE6 issues
Summary: 

**Problem:** Some browsers show links in the default color in spite of being styled in CSS. On hover the CSS styling works.

**Problem faced in:** Google Chrome and IE6. No problem in FF

**Solution:**It is pretty simple by the way. There are two ways to resolve this ..

1. Dont use a:link ie. instead of

```css
    .menu a:link {...}
```

just use,

```
    .menu a {...}
```

And the other way is declare the colors for all the states of the link

```
    .menu a:link {...}
    .menu a:visited {...}
    .menu a:hover {...}
    .menu a:active {...}
```

Remember the order. Its very important .. (Mnemonic - LoVe HAte)

**Many thanks to:** A certain CSS freak at webmasterworld forums
