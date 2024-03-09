title: About this talk
class: nobackground

* `Why` should you care about Generators and Itertools in Python?

* `Focus`: Memory efficient and concise code.

* `Target Audience`: Knowledge of Lists, List comprehensions and
  Higher order functions.

* All examples in `Python 2.7`. We will see what changes for Python
  3.x at the end of the talk.

---

title: Some simple functions
class: nobackground

<pre class="prettyprint" data-lang="py">
def square(x):
    return x * x

def is_even(x):
    return x % 2 == 0

def digit_sum(x):
    """Sum of all digits of a number

       >>> digit_sum(45)
       9
       >>> digit_sum(10)
       1
    
    """
    return sum(map(int, str(x)))
</pre>

---

title: Some simple code
class: nobackground

<pre class="prettyprint" data-lang="py">
>>> nums = range(1, 11)
>>> squares = map(square, nums)
>>> squares
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
>>> evens = filter(is_even, squares)
>>> evens
[4, 16, 36, 64, 100]
</pre>

Effectively the same as,

<pre class="prettyprint" data-lang="py">
>>> squares = [square(x) for x in nums]
>>> evens = [x for x in squares if is_even(x)]
>>> evens
>>> [4, 16, 36, 64, 100]
</pre>

---

title: Let's do some memory profiling
class: nobackground

`Problem`: Successively calculate digit sums of squares of 100000
numbers twice using list comprehensions.

<pre class="prettyprint" data-lang="py">
from memory_profiler import profile

@profile
def ex1():
    squares = [square(x) for x in xrange(0, 100000)]
    dsums = [digit_sum(x) for x in squares]
    squares2 = [square(x) for x in dsums]
    dsums2 = [digit_sum(x) for x in squares2]
    return dsums2
</pre>

---

title: Let's do some memory profiling
class: nobackground

`Results`: Successively calculate digit sums of squares of 100000
numbers twice using list comprehensions.

<pre class="prettyprint" data-lang="py">
Line #    Mem usage    Increment   Line Contents
================================================
    16      6.2 MiB      0.0 MiB   @profile
    17                             def ex1():
    18      8.3 MiB      2.1 MiB       squares = [square(x) for x in xrange(0, 100000)]
    19      9.0 MiB      0.7 MiB       dsums = [digit_sum(x) for x in squares]
    20     10.2 MiB      1.2 MiB       squares2 = [square(x) for x in dsums]
    21     10.9 MiB      0.7 MiB       dsums2 = [digit_sum(x) for x in squares2]
    22     10.9 MiB      0.0 MiB       return dsums2
</pre>

---

title: Let's do some memory profiling
class: nobackground

`Problem`: Successively calculate digit sums of squares of 100000
numbers twice using `generator expressions`.

<pre class="prettyprint" data-lang="py">
from memory_profiler import profile

@profile
def ex2():
    squares = (square(x) for x in xrange(0, 100000))
    dsums = (digit_sum(x) for x in squares)
    squares2 = (square(x) for x in dsums)
    dsums2 = (digit_sum(x) for x in squares2)
    return list(dsums2)
</pre>

---

title: Let's do some memory profiling
class: nobackground

`Results`: Successively calculate digit sums of squares of 100000
numbers twice using `generator expressions`.

<pre class="prettyprint" data-lang="py">
Line #    Mem usage    Increment   Line Contents
================================================
    24      6.2 MiB      0.0 MiB   @profile
    25                             def ex2():
    26      6.2 MiB      0.0 MiB       squares = (square(x) for x in xrange(0, 100000))
    27      6.2 MiB      0.0 MiB       dsums = (digit_sum(x) for x in squares)
    28      6.2 MiB      0.0 MiB       squares2 = (square(x) for x in dsums)
    29      6.2 MiB      0.0 MiB       dsums2 = (digit_sum(x) for x in squares2)
    30      6.7 MiB      0.5 MiB       return list(dsums2)
</pre>

---

title: What did we change?
class: nobackground

List Comprehensions,

<pre class="prettyprint" data-lang="py">
def ex1():
    squares = [square(x) for x in xrange(0, 100000)]
    dsums = [digit_sum(x) for x in squares]
    squares2 = [square(x) for x in dsums]
    dsums2 = [digit_sum(x) for x in squares2]
    return dsums2
</pre>

Generator Expressions,

<pre class="prettyprint" data-lang="py">
def ex2():
    squares = (square(x) for x in xrange(0, 100000))
    dsums = (digit_sum(x) for x in squares)
    squares2 = (square(x) for x in dsums)
    dsums2 = (digit_sum(x) for x in squares2)
    return list(dsums2)
</pre>

---

title: So basically ..
class: nobackground

<img src="images/mind-blown.gif" alt="mind blown"/>

Using square brackets `[]` in place of parens `()` resulted in ~9.5
times lesser memory footprint!

Correct, but that's ridiculously insufficient knowledge to start using
generators. So let's understand them better ..

---

title: What are generators?
class: nobackground

<pre class="prettyprint" data-lang="py">
def g(a, b):
    for i in xrange(a, b):
        yield i*2
</pre>

* Function `g` is a `generator function`.

* When called, `g` will return a `generator object`.

<pre class="prettyprint" data-lang="py">
>>> a = g(1, 6)
>>> a
&lt;generator object g at 0x90136bc&gt;
</pre>

`Returns? WTF!`

---

title: What are generators?
class: nobackground

<pre class="prettyprint" data-lang="py">
def g(a, b):
    for i in xrange(a, b):
        yield i*2
</pre>

* When the `next` method of the generator object is called, the
  execution of code in generator function `suspends` and it produces a
  value.

<pre class="prettyprint" data-lang="py">
>>> a.next()
2
</pre>

* On calling `next` again, the execution inside generator function
  `resumes` (along with the state) and produces the *next* value.

<pre class="prettyprint" data-lang="py">
>>> a.next()
4
</pre>

---

title: What are generators?
class: nobackground

<pre class="prettyprint" data-lang="py">
def g(a, b):
    for i in xrange(a, b):
        yield i*2
</pre>

* This can go on until no more values can be produced at which point,
  a `StopIteration` exception is raised.

<pre class="prettyprint" data-lang="py">
>>> a.next()
6
>>> a.next()
8
>>> a.next()
10
>>> a.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
</pre>

---

title: Iterator protocol
class: nobackground

* Generator objects support iterator protocol ie. they provide `next`
and `__iter__` methods and raise `StopIteration`.

* So they can be consumed using `for loops`.

<pre class="prettyprint" data-lang="py">
>>> for x in g(1, 6):
...     print x
... 
2
4
6
8
10
</pre>

* Or by calling `list` on it

<pre class="prettyprint" data-lang="py">
>>> list(g(1, 6))
[2, 4, 6, 8, 10]
</pre>

---

title: A more verbose definition
class: nobackground

<pre class="prettyprint" data-lang="py">
class G(object):
    def __init__(self, a, b):
        self.curr = a
        self.up_limit = b

    def next(self):
        if self.curr < self.up_limit:
            result = self.curr * 2
            self.curr += 1
            return result
        else:
            raise StopIteration()

    def __iter__(self):
        return self
</pre>

<pre class="prettyprint" data-lang="py">
>>> g = G(1, 6)
</pre>

---

title: Generator expressions
class: nobackground

<pre class="prettyprint" data-lang="py">
>>> (i*2 for i in xrange(1, 6))
</pre>

<br/>

The original generator function for reference,

<pre class="prettyprint" data-lang="py">
def g(a, b):
    for i in xrange(a, b):
        yield i*2
</pre>

---

title: What caused the drop in memory needs?
class: nobackground

Let's try calculating the digit sums of squares again but with some
print statements.

<pre class="prettyprint" data-lang="py">
from __future__ import print_statement

def square(x):
    print('Square of {} ->'.format(x), end=' ')
    return x * x

def digit_sum(x):
    print('Digit sum of {} ->'.format(x), end=' ')
    return sum(map(int, str(x)))
</pre>

---

title: What caused the drop in memory needs?
class: nobackground

With list comprehensions,

<pre class="prettyprint" data-lang="py">
def ex3():
    numbers = xrange(1, 5)
    squares = [square(x) for x in numbers]
    dsums = [digit_sum(x) for x in squares]
    for n in dsums:
        print(n)
</pre>

Output:

<pre class="prettyprint" data-lang="py">
>>> ex3()
Square of 1 -> Square of 2 -> Square of 3 -> Square of 4 -> Digit sum \
of 1 -> Digit sum of 4 -> Digit sum of 9 -> Digit sum of 16 -> 1
4
9
7
</pre>

---

title: What caused the drop in memory needs?
class: nobackground

Now with generator expressions,

<pre class="prettyprint" data-lang="py">
def ex4():
    numbers = xrange(1, 5)
    squares = (square(x) for x in numbers)
    dsums = (digit_sum(x) for x in squares)
    for n in dsums:
        print(n)
</pre>

Output:

<pre class="prettyprint" data-lang="py">
>>> ex4()
Square of 1 -> Digit sum of 1 -> 1
Square of 2 -> Digit sum of 4 -> 4
Square of 3 -> Digit sum of 9 -> 9
Square of 4 -> Digit sum of 16 -> 7
</pre>

---

title: Ok. But what's the point?
class: nobackground

Let's extend the example to read the numbers from each line of a huge
file.

<pre class="prettyprint" data-lang="py">
def ex5():
    with open('huge_file_of_numbers.txt') as f:
        numbers = (int(x) for x in f)
        squares = (square(x) for x in numbers)
        dsums = (digit_sum(x) for x in squares)
        for n in dsums:
            print(n)
</pre>

---

title: Suspension/resumption of execution & state
class: nobackground

<pre class="prettyprint" data-lang="py">
import requests

def get_all_items(url):
    r = requests.get(url)
    assert r.status_code == 200
    for item in r.json():
        yield item
    next_page = None if 'next' not in r.links else r.links['next']['url']
    while next_page:
        r = requests.get(next_page)
        assert r.status_code == 200
        for item in r.json():
            yield item
        next_page = None if 'next' not in r.links else r.links['next']['url']
</pre>

<pre class="prettyprint" data-lang="py">
>>> for item in get_all_items(someurl):
...     print item
</pre>

---

title: Generator gotchas!
class: nobackground

* `Rule #0`: Use generators wisely. Don't use a generator expression
  only because the syntax is slightly different from list
  comprehensions.

* Generator object can be consumed only once.

* Watch out for variable scope during lazy evaluation.

<footer class="source"><a href="http://naiquevin.github.io/python-generators-and-being-lazy.html">Learn more</a> [shameless plug!]</footer>

---

title: Itertools
class: nobackground

A module in the Python standard library.

<pre class="prettyprint" data-lang="py">
import itertools
</pre>

From the docs,

<pre>
"This module implements a number of iterator building blocks inspired
by constructs from APL, Haskell, and SML. Each has been recast in a
form suitable for Python.
    
The module standardizes a core set of fast, memory efficient tools
that are useful by themselves or in combination. Together, they form
an “iterator algebra” making it possible to construct specialized
tools succinctly and efficiently in pure Python."
</pre>

---

title: Abstractions for infinite streams
class: nobackground

`Problem`: Get first n elements out of a generator.

A non-performant version,

<pre class="prettyprint" data-lang="py">
def firstn(xs, n):
    return list(xs)[:n]
</pre>

<br/>

`is_even` with print statements,

<pre class="prettyprint" data-lang="py">
def is_even(x):
    print('is_even called for {}'.format(x))
    return x % 2 == 0
</pre>

(cont ..)

---

class: nobackground

<pre class="prettyprint" data-lang="py">
>>> xs = (x for x in xrange(0, 16) if is_even(x))
>>> firstn(xs, 4)
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
[0, 2, 4, 6]
</pre>

---

title: Lazy slicing
subtitle: itertools.islice
class: nobackground

<pre class="prettyprint" data-lang="py">
def lazy_firstn(xs, n):
    return itertools.islice(xs, 0, n)
</pre>

<pre class="prettyprint" data-lang="py">
>>> xs = (x for x in xrange(0, 16) if is_even(x))
>>> ys = lazy_firstn(xs, 4)
&lt;itertools.islice at 0xac08f54&gt;
>>> list(ys)
is_even called for 0
is_even called for 1
is_even called for 2
is_even called for 3
is_even called for 4
is_even called for 5
is_even called for 6
[0, 2, 4, 6]
</pre>

---

title: Other i* functions of itertools
class: nobackground

besides islice,

* imap
* ifilter
* izip
* izip_longest

---

title: Counting infinitely
subtitle: itertools.count
class: nobackground

`Problem`: Find out the smallest 3 numbers greater than 1000 and powers of 2.

<pre class="prettyprint" data-lang="py">
def is_pow_two(x):
    return not(x & (x - 1))
</pre>

`itertools.count`: Make an iterator that returns evenly spaced values
starting with the argument.

<pre class="prettyprint" data-lang="py">
>>> from itertools import count, islice, ifilter
>>> count(10)
count(10)
>>> list(islice(count(10), 0, 2))
[10, 11]
>>> list(islice(ifilter(is_pow_two, count(1000)), 0, 3))
[1024, 2048, 4096]
</pre>

---

title: Grouping items from an iterator
subtitle: itertools.groupby
class: nobackground

`Problem`: Group list of numbers into even and odd.

<pre class="prettyprint" data-lang="py">
def groupby_even_odd(items):
    f = lambda x: 'even' if x % 2 == 0 else 'odd'
    g = itertools.groupby(items, f)
    for k, items in g:
        print '%s: %s' % (k, ','.join(map(str, items)))
</pre>

<pre class="prettyprint" data-lang="py">
>>> groupby_even_odd([1, 3, 4, 5, 6, 8, 9, 11])
odd: 1,3
even: 4
odd: 5
even: 6,8
odd: 9,11
</pre>

(cont ..)

---

title: Grouping items from an iterator (fixed)
subtitle: itertools.groupby
class: nobackground

`Problem`: Group list of numbers into even and odd.

<pre class="prettyprint" data-lang="py">
def groupby_even_odd(items):
    f = lambda x: 'even' if x % 2 == 0 else 'odd'
    g = itertools.groupby(sorted(items, key=f), f)
    for k, items in g:
        print '%s: %s' % (k, ','.join(map(str, items)))
</pre>

<pre class="prettyprint" data-lang="py">
>>> groupby_even_odd([1, 3, 4, 5, 6, 8, 9, 11])
even: 4,6,8
odd: 1,3,5,9,11
</pre>

---

title: Flatmap that shit!
subtitle: itertools.chain
class: nobackground

Flatmap is a commonly used pattern in functional programming where
mapping a function to a list results in a list of lists that then
needs to be flattened.

`Problem`: given a list of directories, get the names of all their
first level children as a single list.

<pre class="prettyprint" data-lang="py">
>>> import os
>>> dirs = ['project1/', 'project2/', 'project3/']
>>> map(os.listdir, dirs)
>>> [['settings.py', 'wsgi.py', 'templates'],
     ['app.py', 'templates'], 
     ['index.html, 'config.json']]
</pre>

(cont ..)

---

title: Flatmap that shit!
subtitle: itertools.chain
class: nobackground

<pre class="prettyprint" data-lang="py">
    from itertools import chain, imap

    def flatmap(f, items):
        return chain.from_iterable(imap(f, items))
</pre>

<pre class="prettyprint" data-lang="py">
    >>> list(flatmap(os.listdir, dirs))
    >>> ['settings.py', 'wsgi.py', 'templates', 'app.py', 
         'templates', 'index.html', 'config.json']
</pre>

---

title: Functional programming friendly abstractions
class: nobackground

`Problem`: Return first 5 numbers in the fibonacci sequence greater
than the 1000th number in it.

<pre class="prettyprint" data-lang="py">
def iterate(f, x):
    yield x
    while True:
        x = f(x)
        yield x

    
def take(n, xs):
    return itertools.islice(xs, 0, n)

    
def drop(n, xs):
    return itertools.islice(xs, n, None)
</pre>

(cont ..)

---

title: Functional programming friendly abstractions
class: nobackground

`Problem`: Return first 5 numbers in the fibonacci sequence greater
than the 1000th number in it.

<pre class="prettyprint" data-lang="py">
>>> from operator import itemgetter
>>> list(take(5,
              drop(1000,
                   imap(itemgetter(0),
                        iterate(lambda (a, b): (b, a+b),
                                [0, 1])))))
</pre>

<footer class="source">Credit: Example taken from <a
href="https://twitter.com/ghoseb">BG's</a> Clojure workshop.</footer>

---

title: Python 3.x
class: nobackground

* `map`, `filter`, `zip` are lazy.

* `imap`, `ifilter`, `izip` no longer in itertools.

* `itertools.izip_longest` is now `itertools.zip_longest`.

* The `next` method of iterators renamed to `__next__`.

---

title: More on this topic
class: nobackground

* <a href="http://www.dabeaz.com/generators/">Generator tricks for system programmers - David Beazley</a>

* <a href="http://www.ibm.com/developerworks/library/l-pycon/index.html">Iterators and simple generators - David Mertz</a>

* <a href="http://excess.org/article/2013/02/itergen1/">Iterables, Iterators and Generators - Ian Ward</a>

<br/>

`On my blog`:

* <a href="http://naiquevin.github.io/python-generators-and-being-lazy.html">Python generators and being lazy</a>

* <a href="http://naiquevin.github.io/a-look-at-some-of-pythons-useful-itertools.html">A look at some of Python's useful itertools</a>


