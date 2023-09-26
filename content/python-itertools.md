Title: A look at some of Python's useful itertools
Author: Vineet Naik
Date: 2013-05-23
Tags: python
Category: python
Summary: .. with examples and use cases
Status: published


Couple of months back I enrolled for the
[Functional Programming Principles in Scala](https://www.coursera.org/course/progfun)
course taught by Martin Odersky on Coursera. While solving one of the
early assignments, I remember searching for "Scala equivalent to
Python's range". By the end of the course, I was searching for python
equivalents for some of the methods and operations on scala
collections. There is no doubt that learning new and different
languages help you as a programmer in more than one way. Ok, I am
digressing, but what that search led me to was the insanely useful
[itertools](http://docs.python.org/2/library/itertools.html) module
and it left me wondering - why didn't I take a _real_ look at it
earlier!

In this article I am going to show some of the must-know itertools
that will make your everyday code more memory efficient, elegant and
concise. Instead of focusing on one function/class from the module at
a time, it would be helpful to see some real world (and not so real
world) use cases and examples of itertools.

But before that, I should mention that I have tried the examples on
Python 2.7.3 and would recommend you use 2.7.x to follow along,
although they should _mostly_ work on Python 3.x too.

### Taking "lazy" to the next level

In an
[earlier blog post](http://naiquevin.github.io/python-generators-and-being-lazy.html),
I had covered generators and how lazy evaluation can be used to write
memory efficient code. Itertools let you do more with the lazily
evaluated objects.

You may already know that the ``map`` and ``filter`` BIFs can accept
not just a list but any iterator in general, which means we can also
pass them a generator. But doing so doesn't give us truly lazy
behaviour. Let's see an example to understand this.

```python

    def is_even(x):
        print 'is_even called for %d' % (x,)
        return x % 2 == 0
        
    def even():
        return filter(is_even, xrange(20))
```

_**Edit**: Thanks to many comments, I replaced the redundant generator
expression ``(i for i in xrange(20)`` with just ``xrange`` in all
examples._

The above code defines a function ``is_even`` to check if an integer
is even. In ``even``, we pass ``is_even`` as a predicate to ``filter``
thus returning all even integers between 0 to 20. To get first four of
such integers, we can use the slice operator.

```pycon

    >>> even()[:4]
    is_even called for 0
    is_even called for 1
    is_even called for 2
    is_even called for 3
    is_even called for 4
    is_even called for 5
    is_even called for 6
    is_even called for 7
    is_even called for 8
    is_even called for 9
    is_even called for 10
    is_even called for 11
    is_even called for 12
    is_even called for 13
    is_even called for 14
    is_even called for 15
    is_even called for 16
    is_even called for 17
    is_even called for 18
    is_even called for 19
    >>> [0, 2, 4, 6]
```

While the result that we obtained is correct, our code is doing a lot
of unnecessary work. We can see this from the statements that are
getting printed every time ``is_even`` is called (20
times). Wait.. but we just need first 4 items right, why is it even
getting called that many times?  The problem is that although we
started with a generator, ``filter`` needs to run each item through
the predicate and so the generator ends up getting consumed. Finally,
we get a list from which we slice out the first 4 items.

```pycon

    >>> type(even())
    <type 'list'>
```

How can we do better? The idea is, we need a way to delay the
application of filter on the generator. ``itertools.ifilter`` does
exactly that by returning a lazy object instead of a list. Items will
be filtered whenever some other function or a for loop consumes
them. Lets define another function ``lazy_even``,

```python

    import itertools
    
    def lazy_even():
        return itertools.ifilter(is_even, xrange(20))
```

```pycon
   
    >>> nums = lazy_even()
    >>> type(nums)
    <type 'itertools.ifilter'>
```

Ok, this gives us a lazy object. But the problem now is, we still need
a way to slice out the first 4 items without converting the entire
thing to a list. Itertools provides ``islice`` for this which takes
the iterator, a start index and a stop index.

```pycon
   
    >>> first_four = itertools.islice(nums, 0, 4)
    >>> type(first_four)
    <type 'itertools.islice'>
    for i in first_four:
    ...     print i
    ... 
    is_even called for 0
    0
    is_even called for 1
    is_even called for 2
    2
    is_even called for 3
    is_even called for 4
    4
    is_even called for 5
    is_even called for 6
    6
```

As you can see, now ``is_even`` is called only while it's required.


### Counting infinitely

Let's take another example. This time we need to find out 3 smallest
numbers that are greater than 1000 and powers of 2. In the eariler
blog post on generators, there was an example of counting infinitely
using the ``yield`` keyword. Here we need to do something similar to
count integers and test whether or not each one is a power of 2. The
catch is that since we need to return 3 such numbers, we don't know
when to stop counting. Ok, probably in this case it's easy to
pre-calculate or guess, but what if the predicate function is a bit
more complex for eg. a check for primality? With itertools, we can use
the same technique as in the previous example. As a bonus, the module
comes with a ``count`` function so we don't need to write our own.

```pycon

    >>> import math
    >>> from itertools import count, islice, ifilter
    
    >>> def is_pow_two(x):
    ...     ln = math.log(x, 2)
    ...     return math.floor(ln) == ln
    
    >>> list(islice(ifilter(is_pow_two, count(1000)), 0, 3))
    [1024, 2048, 4096]
```

``is_pow_two`` will be called no more than 4096 times = win!


### Grouping things in style

If you often use Python to write scripts for extracting data,
eg. scraping web pages or parsing log files, then you may have come
across this common pattern -- reading content from some source,
extracting useful data out of it and saving the extracted data in some
other form (or directly using it). And quite often, we need to group
data into parts say for eg. parsing web server access logs and group
incoming requests by their response status
codes. ``itertools.groupby`` makes this very easy. It takes an
iterable and a ``key`` function. The ``key`` function is used to group
items with _consecutively_ similar key values together. Here is an
example where given a list of integers we separate them into "even"
and "odd" groups.

```python

    from itertools import groupby
    
    def groupby_even_odd(items):
        f = lambda x: 'even' if x % 2 == 0 else 'odd'
        gb = groupby(items, f)
        for k, items in gb:
            print '%s: %s' % (k, ','.join(map(str, items)))
```

```pycon
   >>> groupby_even_odd([1, 3, 4, 5, 6, 8, 9, 11])
   odd: 1,3
   even: 4
   odd: 5
   even: 6,8
   odd: 9,11
```

But something is strange, isn't it? The integers are indeed grouped
but there are many "even" and "odd" groups. The reason behind this is,
it only groups _consecutive_ items together. To get around this, we
can simply provide it a sorted iterable.

```python

    def groupby_even_odd(items):
        f = lambda x: 'even' if x % 2 == 0 else 'odd'
        gb = groupby(sorted(items, key=f), f)
        for k, items in gb:
            print '%s: %s' % (k, ','.join(map(str, items)))
```

```pycon

    >>> groupby_even_odd([1, 3, 4, 5, 6, 8, 9, 11])
    even: 4,6,8
    odd: 1,3,5,9,11
```

And now the grouping happens the way we want it. An important thing to
note is that the key function used to sort the list must be same as
the one which is going to be passed to ``groupby``.


### Just flatmap that shit!

Flatmap is a commonly used pattern in functional programming where
mapping a function to a list results in a list of lists that then
needs to be flattened. For eg. given a list of directories, we want to
get the names of all their first level children as a list.

```pycon
    
    >>> import os
    >>> dirs = ['project1/', 'project2/', 'project3/']
    >>> map(os.listdir, dirs)
    >>> [['settings.py', 'wsgi.py', 'templates'],
         ['app.py', 'templates'], 
         ['index.html, 'config.json']]
```

This gives us a list of lists and we still need to flatten it. There
are of course many ways to do this, one way is to use ``reduce``. But
here is an elegant way using ``itertools.chain``. ``chain`` takes many
iterables as arguments and chains or appends them at ends.

_**Edit**: As correctly pointed out by
[masklinn on hacker news](https://news.ycombinator.com/item?id=5767462),
it's better to use ``imap`` instead of ``map`` and also the alternate
``chain`` constructor ``chain.from_iterable`` to avoid passing the
lazy object as \*args since unpacking with \*args will result in eager
evaluation._

Let's define a function ``flatmap`` that will map a function to a list
of items and flatten the resulting list of lists.

```python

    from itertools import chain, imap

    def flatmap(f, items):
        return chain.from_iterable(imap(f, items))
```

And now we replace the call to ``map`` with ``flatmap``,

```pycon

    >>> list(flatmap(os.listdir, dirs))
    >>> ['settings.py', 'wsgi.py', 'templates', 'app.py', 
         'templates', 'index.html, 'config.json']
```

### Itertools for everything (for fun and learning!)

As a final example, let's see how we can compose an elegant solution
entirely using our newly acquired utility belt. The problem is to find
a set of <s>common</s> (Thanks
[wcyee](http://naiquevin.github.io/a-look-at-some-of-pythons-useful-itertools.html#comment-908642009))
factors of a list of integers.

```python

    from itertools import ifilter, takewhile, count

    def factors(n):
        return ifilter(lambda x: n % x == 0, takewhile(lambda y: y <= n, count(1)))        
```        

```pycon

    >>> set(flatmap(factors, [9, 15, 16, 23, 76, 101]))
    set([1, 2, 3, 4, 5, 38, 8, 9, 76, 15, 16, 19, 23, 101])
```

That's all for now. If you reached this far, thanks for reading and
hope you found it helpful. Itertools obviously has many more useful
functions and classes. I just skipped them since I failed to come up
with good examples and use cases for them. May be I will do a part II
some time later.

### References

- [Itertools docs](http://docs.python.org/2/library/itertools.html)
  (Particularly, check the Recipes section)

