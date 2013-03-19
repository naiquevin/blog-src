Title: Python generators and being lazy
Author: Vineet Naik
Date: 2013-03-01 12:00:00
Tags: python, generators
Category: tutorials
Summary: A post/tutorial on Python generators with examples


This is going to be a rather long post (call it a tutorial if you
wish), but in case you are a beginner I hope it will help you
understand generators in Python and lazy evaluation and your time will
be well spent. I usually take notes while learning any new stuff and
now I am trying to experiment converting the notes into blog
post/tutorials as I feel it will be a good way for me to revisit and
revise the concepts while being helpful to others at the same time.

And no, please don't grab a cup of coffee for this one
;-) Instead fire up a Python shell and have your favourite editor
ready because we will be trying out stuff.

#### A simple example

The good news is that, to work with Python generators it doesn't
require us to learn much additional syntax. Here is a simple
generator.

```python
    def gen():
        for i in range(1, 6):
            yield i
```

```pycon            
    >>> g = gen()
    >>> type(g)
    <type 'generator'>
```

`g` is a generator here. What's happening is that the function `gen`
when invoked returns a generator object which is assigned to `g`. If
you think I am crazy to say it _returns_ a generator object, I don't
blame you because it's not immediately clear. After all there is no
`return` keyword used. Instead, we see a new keyword `yield`. A
function with yield statement will magically return a generator
object.

The call to the function will not execute any code inside it yet. For
that we need to call the generator object's `next` method,

```pycon
    >>> g.next()
    1
    >>> print 'Hello'
    Hello
    >>> g.next()
    2
    >>> g.next()
    3
```

At the time of the first call to the `next`, the yield statement will
be executed once and a value will be returned. At the same time, the
control will also be returned back to the calling code. On the next
call to the `next` method, the control goes back to the function and
it can resume the execution from where it left with full access to the
local variables again.


#### Iterator protocol and Generator expressions

Generators support the
[iterator protocol](http://docs.python.org/2/library/stdtypes.html?highlight=iterator#iterator-types)
i.e. they implement the `next` and `__iter__` methods and raise
``StopIteration`` exception when no more values can be yielded. Hence
we can use a for loop to generate values from a generator instead of
calling the next method manually. ``for`` will implicitly handle
``StopIteration`` and when that happens, will end the loop.

```python
    for i in g:
        print i
```

In fact there also exist list comprehensions equivalent for generators
called generator expressions. The syntax again is ridiculously
similar, the only change being, round brackets ``()`` instead of
square ``[]``. The difference is that it will give us an iterator (a
generator object) instead of an iterable (a list in memory).

```pycon
    >>> squares = [i*i for i in range(1, 11)] # list    
    >>> type(squares)
    <type 'list'>
    >>> gen_squares = (i*i for i in range(1, 11)) # generator object
    >>> type(gen_squares)
    <type 'generator'>
    >>> iter(gen_squares) is gen_squares
    True    
```


#### Why generators?

Now you may ask how does this differ from an ordinary list and what is
the use of all this anyway? The key difference is that the generator
gives out new values on the fly and doesn't keep the elements in
memory. Turns out, our earlier example was not quite apt for
understanding the concept as we used `range` to build a list in memory
upfront. As a practical example, let's define a function to give us
incremental values infinitely.

```python
    def infinitely_incr(start=0):
        n = start
        while True:
            n += 1
            yield n
```

```pycon            
    >>> iinf = infinitely_incr()
    >>> iinf.next()
    1
    >>> iinf.next()
    2
    >>> iinf.next()
    3
```

We can call ``iinf.next()`` as many times as we want to get an
incremented number each time without having a list in memory. This is
pretty cool.

Let's consider another example. What if we have huge data in some file
and need to process each of it's lines by calling one or many
functions on them,

```python
    def gen1():
        with open('hugedata.txt') as f:
            for line in f:
                yield line    
    g = gen1()    
    g2 = (process(x) for x in g)
    for x in g2:
        print x
```

In python, a file object can be iterated over to obtain one line at a
time. In the above example, since the `process` function is called
inside a generator expression, it will not be executed until the for
loop starts consuming the generator. That is when the `process`
function will execute for each value. Don't worry if all this sounds
confusing at the moment since the next example will clarify
things. But if you think about it, the cost of loading all data from
the huge file into memory is avoided. On the other hand, it also means
that the file cannot be closed until all the lines are processed.

Also, not keeping the elements in memory implies that a generator
object can be looped through or consumed only once. So it is obviously
not a good choice if the sequence of items need to be reused in which
case a normal list would be suitable.

```pycon
    >>> g = gen()
    >>> squares = (i*i for i in g)
    >>> list(squares)
    [1, 4, 9, 16, 25]
    >>> cubes = (i*i*i for i in g)
    >>> list(cubes)
    []
```

But if you have a series of functions, that need to be executed one
after another on each line of a file, then the laziness of generator
expressions can be tremendously useful.


#### Understanding the 'lazy' using a <s>concrete</s> contrived example

So, what does being lazy mean after all? Imagine our hugedata.txt
contains some 100000 lines with 1 random number on each line and we
want to find out the digit sum of the square of each number and print
out the results in the shell. Here is an example that uses list
comprehensions and hence will build and keep lists in memory.

For the sake of an example and to make sense out of the results, let's
assume that our hugedata.txt is actually a tiny file of just 5 lines
containing the first 5 positive integers :-)

```python
    def square(x):
        print 'Square of %d ->' % x,
        return x*x        
    def digit_sum(x):
        print 'Digit Sum of %d ->' % x,
        return sum(map(int, str(x)))
    numbers = gen()
    squares = [square(n) for n in numbers]
    dsums = [digit_sum(n) for n in squares]
    for n in dsums:
        print n
```

Running the above snippet of code will produce an output as follows,

```
    Square of 1 -> Square of 2 -> Square of 3 -> Square of 4 -> Square
    of 5 -> Digit Sum of 1 -> Digit Sum of 4 -> Digit Sum of 9 -> Digit
    Sum of 16 -> Digit Sum of 25 -> 
    1
    4
    9
    7
    7
```

First all squares will be calculated, then their digit sums and then
the results will be printed one by one.

Now with generator expressions just see what we get,

```
    numbers = gen1()
    squares = (square(n) for n in numbers)
    dsums = (digit_sum(n) for n in squares)
    for n in dsums:
        print n
```

Output:

```
    Square of 1 ->  Digit Sum of 1 ->  1
    Square of 2 ->  Digit Sum of 4 ->  4
    Square of 3 ->  Digit Sum of 9 ->  9
    Square of 4 ->  Digit Sum of 16 ->  7
    Square of 5 ->  Digit Sum of 25 ->  7
```

Every item is processed by each function sequencially similar to how
it would have been if there was just one ``for`` loop and all
functions were called progressively on the derived values of the item
in each iteration. This is quite awesome if you can imagine numbers
flowing through functions similar to signals flowing through various
stages of a signal processor.

It's called lazy because the numbers are getting consumed late, at the
time of iteration. The implicit call to ``next`` by the `for` loop
asks for `digit_sum` of `1` from `dsums` which asks for the `square`
of `1` from `squares` which asks for `1` from `numbers`. This
continues till `numbers` can yield a value. Nothing is evaluated
unless it is asked for.


#### Common traps and things to watch out for

Just like in case of many other cool language features, there are a
few gotchas and things that we need to watch out for when using
generators as it's very easy to screw things up.

Rule #0 is - Use generators wisely. Don't use a generator expression
only because the syntax is slightly different from list
comprehensions.

Also, as we saw earlier, if the sequence needs to be reused then
simply use a list. Keeping stuff in memory is not bad after all (we do
that all the time while caching values, don't we?)
  
Another important thing to watch out for is the scope of the variables
that are going to be used by functions when they execute in a lazy
manner. This needs a bit more explanation so here is an example.

Suppose we have a generator that yeilds alphabets and we need to add
two suffixes to each alphabet for eg. we have alphabet ``a``. First
it's suffixed with `x` which makes it `ax` and then with `y` which
makes it `axy`. We need to do this with multiple alphabets and we
choose to use a generator object to yield each alphabet.

```python
    def add_suffix(s, suffix):
        return '%s%s' % (s, suffix)        
    def gen():
        for i in ['a', 'b', 'c', 'd']:
            yield i            
    ns = gen()
    suffixes = ['x', 'y']
    for s in suffixes:
        ns = (add_suffix(i, s) for i in ns)
    print list(ns)
```

What do you think will be output of the above program? If your mind
tells you `['axy', 'bxy', 'cxy', 'dxy']` then it's wrong. Just run it
and see it for yourself that the output we get is
`['ayy', 'byy', 'cyy', 'dyy']`. What's happening here?

A generator can remember the local variables when it gets back the
control on the call of `next` method. The local scope here is actually that of
the `for` loop. By the time the generator is consumed upon call to
`list(ns)`, the value of `s` in local scope is `y`. The value `x` in
the previous iteration of suffixes is simply lost.

To fix this, we just define another function wrapping over the call to
the `add_suffix` function that will return a generator object

```python
    def gen1(s, sfx):
        for x in s:
            yield add_suffix(x, sfx)            
    for s in suffixes:
        ns = gen1(ns, s)
```

```pycon
    >>> list(ns)
    ['axy', 'bxy', 'cxy', 'dxy']
```


#### This is by no means all about generators

I know there is lot more to generators than what this post covers. You
should only consider this as a starting point for digging deeper into
them. It would also be worth mentioning about the use of generator as
co-routines where it can accept values from the calling code besides
yeilding to it. Co-routines are pretty advanced and mind bending to
understand and I am still trying to explore this topic. I got
interested in it after attending a talk on 'Data processing pipelines'
by Ami Tavory at SciPy India 2012 where he also showed
[Dagpype](http://code.google.com/p/dagpype/) - A framework written by
him for data processing and preparation.


#### References:

- [Generator Tricks for system programmers](http://www.dabeaz.com/generators/) by David Beazley 
  (particularly a must read)
- [Iterators and simple generators](http://www.ibm.com/developerworks/library/l-pycon/index.html) by David Mertz
- [Core Python Programming Book](http://www.amazon.com/Core-Python-Programming-Wesley-Chun/dp/0132269937) by Wesley Chun
- I would also like to recommend this recently published
  [article](http://excess.org/article/2013/02/itergen1/) by Ian Ward.
  

#### If you are curious about co-routines, also see,

- [A Curious Course on Coroutines and Concurrency](http://dabeaz.com/coroutines/)
  (again by David Beazley) 
- [Part II](http://excess.org/article/2013/02/itergen2/) of the above
  article by Ian Ward


#### People who helped improve the post by pointing out errors and bugs. Thanks!

- [Jimit Modi](http://twitter.com/jimymodi)
- Sanjay Bhangar

