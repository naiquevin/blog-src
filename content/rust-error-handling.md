Title: Handling Rust errors elegantly
Author: Vineet Naik
Date: 2026-03-08
Tags: rust
Category: programming
Summary: What I wish I had known earlier about some of Rust's convenience features for elegant error handling
Status: published

Rust doesn't have exceptions. Instead, functions and methods have to
return a special type to indicate failure. This is the `Result` type
which holds either the computed value if everything goes well, or an
error otherwise. Both, the value and error have types. So it's
definition is `Result<T, E>`, an enum that can be instantiated using
one of it's two variants `Ok` and `Err`.

```rust
let r1: Result<bool, String> = Ok(true);
let r2: Result<bool, String> = Ok(false);
let r2: Result<bool, String> = Err("No clue".to_string());
```

When a function returns a Result, it becomes mandatory for the caller
to handle it, otherwise it's impossible to extract the value it holds,
which is what the caller is interested in most of the time <a
id="footnote-1-ref" href="#footnote-1"><sup>1</sup></a>. The easiest
way to get the value out of a `Result` is to call it's `unwrap`
method, but there will be a panic in case of an error. It can be
thought of as an equivalent of an "unhandled" exception.

Calling `unwrap` is not necessarily a bad thing though. If there's
really no way to handle an error, it's better to let the process crash
than behave unpredictably. Arguably, "let it crash" is a valid
strategy to handle an unexpected error. But if your code is full of
`unwrap` calls (or it's close cousin `expect`), it's probably out of
laziness than intent.

A more respectable approach is to pattern-match the `Result` enum and
handle both cases.

```rust
let res = Ok(true);
match res {
    Ok(x) => println!("Value is {x}"),
    Err(e) => {
        // log a warning or do something else
        println!("Error: {e}")
    },
}
```

As a beginner, you may find pattern matching clearer and easier to
understand. But soon it gets tedious to write and verbose to
read. Much of the real world rust code written by experienced devs
will use convenience features that rust provides to make error
handling less tedious, which is essentially the topic of this post,
but we will get to that in a bit.

Like me, if you're coming to rust from a dynamic languages background,
the first issue you'll probably run into is figuring out how to return
different types of errors from the same function. For example, suppose
you're writing a function to read a file and parse it's contents, you
may have to propagate two types of errors to the caller:

1. An `std::io::Error` in case of failure to read the file
2. A custom error, indicating failure to parse a line into some
   internal data structure (let's take `u64` for the sake of this
   example)

As a beginner, you may be tempted to convert both errors into `String`
and use it as the error type.

```rust
use std::{fs::File, io::{BufRead, BufReader}, path::Path};

fn parse(path: &Path) -> Result<Vec<u64>, String> {
    let file = match File::open(path) {
        Ok(f) => f,
        Err(_) => return Err("Error reading the file".to_string()),
    };
    let reader = BufReader::new(file);
    let mut result = vec![];
    for line in reader.lines() {
        let num_str = match line {
            Ok(l) => l,
            Err(_) => return Err("Error reading the file".to_string()),
        };
        let num: u64 = match num_str.parse() {
            Ok(n) => n,
            Err(_) => return Err("Error parsing string to u64".to_string()),
        };
        result.push(num)
    }
    Ok(result)
}
```

Now any one who has written any serious software would most certainly
get a bad feeling about this. There's often a need to be able to
classify errors eventually, and doing that with strings is a terrible
idea, especially in a typed language. A good example of the need to
classify errors is a typical web app. Based on the reason for failure,
you want to respond with an appropriate HTTP status code: A validation
error must result in a 400 while failure to connect to the database
must be a 5xx. Imagine having to match strings againstg regular
expressions in order to take this decision.

I first ran into this problem in mid 2023, when LLMs had yet to gain
popularity as search engines. So I googled the old-fashion way and
landed on this gem of a post -
[https://burntsushi.net/rust-error-handling/](https://burntsushi.net/rust-error-handling/). In
particular, defining a single enum that can wrap over multiple error
types was an eye opener for me.

Here's the same code with a custom defined error type:

```rust
enum AppError {
    Io(std::io::Error),
    ParseInt(std::num::ParseIntError),
}

fn parse(path: &Path) -> Result<Vec<u64>, AppError> {
    let file = match File::open(path) {
        Ok(f) => f,
        Err(e) => return Err(AppError::Io(e)),
    };
    let reader = BufReader::new(file);
    let mut result = vec![];
    for line in reader.lines() {
        let num_str = match line {
            Ok(l) => l,
            Err(e) => return Err(AppError::Io(e)),
        };
        let num: u64 = match num_str.parse() {
            Ok(n) => n,
            Err(e) => return Err(AppError::ParseInt(e)),
        };
        result.push(num)
    }
    Ok(result)
}
```

I've intentionally written it in a tedious way, by pattern-matching
every single result value so that you can clearly see what's going
on. It doesn't have to be this verbose. There are two features of
rust that we can use to elegantly trim down this code.

1. the `map_err` function combinator helps convert error, if any, from
   one type to another and,
2. the question mark operator (`?`) helps with error propagation

```rust
fn parse(path: &Path) -> Result<Vec<u64>, AppError> {
    let file = File::open(path).map_err(AppError::Io)?;
    let reader = BufReader::new(file);
    let mut result = vec![];
    for line in reader.lines() {
        let num_str = line.map_err(AppError::Io)?;
        let num: u64 = num_str.parse()
            .map_err(AppError::ParseInt)?;
        result.push(num)
    }
    Ok(result)
}
```

The use of enums for wrapping multiple error types into a single error
type and then converting specific errors to it using `map_err` was an
_aha_ moment for me. IIRC, I may not have read the rest of that post
by burntsushi with as much attention afterwards. Having found a
workable solution, I stuck to it for quite some time without realizing
that I was missing out by not using the convenience features rust
provides for dealing with the `Result` and `Error` types more
elegantly.

And that's what this post is about. Thank you for reading this far but
here is where this post actually begins! If you're just starting with
rust or still getting used to it, hope you will find it useful.

### Errors and Iterators

Before picking up rust, I wrote Clojure professionally for 9 years and
dabbled in several flavours of lisp such as scheme, racket, emacs
lisp. Naturally I was quite happy to learn about iterators and the
familiar functional abstractions they provide - `map`, `filter`,
`fold` etc. But, soon I realized that error propagation from inside
the fn closure passed to
[Iterator::map](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.map)
is directly not possible as it expects a closure that returns `T` and
not `Result<T, E>`. For example, the following doesn't compile:

<div class="code-container">
<div class="rs-compile-error"><img src="theme/images/does_not_compile.png" alt="Does not compile" title="Does not compile"/></div>
```rust
#[derive(Debug)]
enum AppError {
    ...,
    Custom,
}

fn process(x: u8) -> Result<u8, AppError> {
    println!("..... x = {x}");
    if x == 2 {
        return Err(AppError::Custom);
    }
    Ok(x)
}

fn main() -> Result<(), AppError> {
    let input = vec![1, 2, 3, 4];
    let result: Vec<u8> = input.into_iter()
        .map(|x| {
            process(x)?
        })
        .collect();
    println!("Result = {result:?}");
    Ok(())
}
```
</div>

```
error[E0277]: the `?` operator can only be used in a closure that returns `Result` or `Option` (or another type that implements `FromResidual`)
  --> src/main.rs:21:23
   |
20 |         .map(|x| {
   |              --- this function should return `Result` or `Option` to accept `?`
21 |             process(x)?
   |                       ^ cannot use the `?` operator in a closure that returns `u8`
```

This one compiles but an error gets collected in the result and not
propagated immediately when it's encountered. Often that's not what we
want.

```rust
fn main() -> Result<(), AppError> {
    let input = vec![1, 2, 3, 4];
    let result: Vec<Result<u8, String>> = input.into_iter()
        .map(process)
        .collect();
    println!("Result = {result:?}");
    Ok(())
}
```

```
..... x = 1
..... x = 2
..... x = 3
..... x = 4
Result = [Ok(1), Err(Custom), Ok(3), Ok(4)]
```

So I gave up and preferred using simple for-loops in such cases,

```rust
fn main() -> Result<(), AppError> {
    let input = vec![1, 2, 3, 4];
    let mut result = Vec::with_capacity(input.len());
    for i in input {
        result.push(process(i)?);
    }
    println!("Result = {result:?}");
    Ok(())
}
```

Turns out, there's a way to stop iteration upon encountering an error
and propagate it up the call stack.

```rust
fn main() -> Result<(), AppError> {
    let xs = vec![1, 2, 3, 4];
    xs.into_iter()
        .map(process)
        .collect::<Result<Vec<u8>, AppError>>()?;
    Ok(())
}
```

This may feel like magic at first but once you understand the
`FromIterator` trait, it makes perfect sense. This trait is already
implemented for the `Result` type. The
[doc](https://doc.rust-lang.org/std/result/enum.Result.html#impl-FromIterator%3CResult%3CA,+E%3E%3E-for-Result%3CV,+E%3E)
explains it quite nicely.

> Takes each element in the Iterator: if it is an Err, no further
> elements are taken, and the Err is returned. Should no Err occur, a
> container with the values of each Result is returned.

So the call to `collect` returns exactly what's specified as the type
declaration - `Result<Vec<u8>, AppError>` and the question mark
operator can be used immediately to extract the value or propagate the
error.

### Errors and Option

Similarly, when using the `.map` method on an `Option` type, it's not
possible to propagate the result directly from inside the closure.

<div class="code-container">
<div class="rs-compile-error"><img src="theme/images/does_not_compile.png" alt="Does not compile" title="Does not compile"/></div>
```rust
fn main() -> Result<(), AppError> {
    let x = Some(1);
    let y = x.map(|i| process(i)?);
    println!("{y:?}");
    Ok(())
}
```
</div>

Sure, explicit pattern-matching works:

```rust
fn main() -> Result<(), AppError> {
    let x = Some(1);
    let y = match x {
        Some(i) => Some(process(i)?),
        None => None
    };
    println!("{y:?}");
    Ok(())
}
```

But with `Option` values, you may end up repeating such code many times. A
more concise way is to have the closure return a `Result`, so you'd
get `Option<Result<T, E>>` which can then be converted to
`Result<Option<T>, E>` by calling the `transpose` method.

```rust
fn main() -> Result<(), AppError> {
    let x = Some(1);
    let y: Option<Result<u8, AppError>> = x.map(process);
    let z: Result<Option<u8>, AppError> = y.transpose();
    println!("{:?}", z.unwrap());
    Ok(())
}
```

Here I'm using multiple steps with explicit type declarations for
clarity but the same can be expressed as a one-liner too -
`x.map(process).transpose()?`. An experienced rust programmer should
easily be able to recognize this pattern and understand what's going
on.

My general observation is that anytime one of the arms of a `match`
block is `None => None` or `Err(e) => Err(e)`, there must be a more
concise and elegant way to write it.

### Implementing the Error trait

Initially it wasn't clear to me why the `Error` trait was important. I
never had to define it for any of my custom error types. Like any
other trait, the rust compiler wouldn't complain if an error type
doesn't implement it. It's only when a certain part of code requires
it through trait bounds, that you need to be implemented for the code
to compile. It's more of a convention that strictly enforced
requirement.

I didn't care about the `Error` trait for many months, until I
attended a deep dive session about the `anyhow` crate at the [Rust
Bangalore](https://hasgeek.com/rustbangalore) meetup where the speaker
[Dhruvin Gandhi](https://dhruvin.dev/) explained it in great detail.

Good news is that the `Error` trait provides all the methods as long
as `Debug` and `Display` traits are implemented, so all you need to
implement is these two traits.

Let's modify the `AppError` so that it implements the `Error` trait

```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    ParseInt(std::num::ParseIntError),
    Custom,
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::Io(e) => write!(f, "IO error: {e}"),
            AppError::ParseInt(e) => write!(f, "Parsing error: {e}"),
            AppError::Custom => write!(f, "Something went wrong"),
        }
    }
}

impl std::error::Error for AppError {}
```

As you can see, in case of the `Io` and `ParseInt` variants we could
assume that the underlying error types would have the `Display` trait
implemented, so we could directly use it for string interpolation.

Similarly, we could directly annotate `AppError` with
`#[derive(Debug)]` only because `std::io::Error` and
`std::num::ParseIntError` implement `Debug`.

Finally, the impl block for the Error trait remains empty because, as
mentioned above, all the trait methods have default implementation
already provided.

Essentially, implementing the `Error` trait makes it easy for multiple
error types to work well with each other. You'll see a concrete
example towards the end of this post.


### Implementing the From trait

Software is written in layers. Often, error types defined in high
level code have variants wrapping over the low level error
types. We've already come across this in the `AppError` example
above - The `AppError::Io` variant is a wrapper for the low level
`std::io::Error` type.

In such cases, you'll often notice the same `.map_err` expression
repeated multiple times in high level functions. Here's an example:

```rust
enum AppError {
    ...,
    Db(sqlx::error::Error),
}

fn web_app_handler() -> Result<HttpResponse, AppError> {
    let x = run_query_1().map_err(AppError::Db)?;
    ...
    let y = run_query_2().map_err(AppError::Db)?;
    ...
    run_query_3().map_err(AppError::Db)?;
    ...
}
```

The repetition can be avoided by implementing the `From` trait for the
higher level error

```rust
impl From<sqlx::error::Error> for AppError {
    fn from(e: sqlx::error::Error) -> Self {
        AppError::Db(e)
    }
}

fn web_app_handler() -> Result<HttpResponse, AppError> {
    let x = run_query_1()?;
    ...
    let y = run_query_2()?;
    ...
    run_query_3()?;
    ...
}
```

As the return type of the function is known, the `?` operator takes
care of converting to it by calling the corresponding `From`
implementation.

### thiserror

That brings us to the [thiserror](https://crates.io/crates/thiserror)
crate. When I was first searching how to return two types of errors
from a single function, I came across many resources that suggested
the `thiserror` and `anyhow` crates. As a beginner I felt a bit
overwhelmed by both at that time. Specially since the custom enum
approach worked and seemed elegant enough, why bother including
additional dependencies?

But once I started implementing `Error` trait for my custom error
types, `thiserror` began to make sense.

With `thiserror` the above `AppError` definition along with the
`Display` and `From` implementations can be compressed into:

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(std::io::Error),
    #[error("Parsing error: {0}")]
    ParseInt(std::num::ParseIntError),
    #[error("Something went wrong")]
    Custom,
    #[error("Database error: {0}")]
    Db(#[from] sqlx::error::Error),
}
```

As you can see, the `Display` trait is generated from the annotations
with "inline" error messages. And the `From` trait implementation is
generated for variants that have the `#[from]` attribute. This is
incredibly convenient. Implementing `Error` traits for all error types
doesn't feel like a chore any more. I use `thiserror` in all my
projects.

I am still not convinced about `anyhow` though. It feels a bit too
much convenience for my comfort, where you stop caring about the
individual error types altogether. I have never used it in a serious
project, so I could be wrong.

### Error handling for library authors

If you are implementing a library or a crate that others use in their
code, there are a few things you might want to take care of. These are
also applicable to error types exposed by low level code and not just
external dependencies.

Always implement the `Error` trait for the error types that are
publicly exposed by the crate. Had `std::io::Error` not implemented
the Error trait, it wouldn't have been possible to use `thiserror` for
the `AppError` enum.

In most cases, a low level error type gets converted to a higher level
error type as we've seen in previous examples in this post. But
sometimes it's possible that a high level error type (defined in an
app for example) has to be converted to a low level type (defined in a
library). This happens especially when the library exposes a trait
requiring a method that returns a low level error type.

I encountered this when implementing
[plectrum](https://github.com/naiquevin/plectrum) - a crate that helps
with mapping lookup/reference tables in a database with rust enums. It
requires the user to implement a `DataSource` trait, the definition of
which is:

```rust
pub trait DataSource {
    type Id: std::hash::Hash + Eq + Copy;
    fn load(
        &self,
    ) -> impl std::future::Future<Output = Result<HashMap<Self::Id, String>, plectrum::Error>> + Send;
}
```

Notice the return type of the `load` method has `plectrum::Error`
type. In the initial version of the crate, I had provided a
`Sqlx(sqlx::Error)` variant in the `plectrum::Error` enum as `sqlx` is
my preferred SQL library. But what about those who use other libraries
or ORMs?

In a later version, I added a generic `DataSource` variant<a id="footnote-2-ref" href="#footnote-2"><sup>2</sup></a>:

```rust
pub enum Error {
    ...
    #[error("Error when loading data from the data source: {0}")]
    DataSource(#[source] Box<dyn std::error::Error + Send + Sync>),
    ...
}
```

Plectrum users can now wrap any error type in
`plectrum::Error::DataSource` variant as long as it implements the
`Error` trait as well as the `Send` and `Sync` marker traits.



This is a good example of why implementing the `Error` trait is
important for your custom error types.

### Footnotes

<b id="footnote-1">1</b>. Sometimes the caller doesn't really care
about the returned value, but if the result is not "used", which
essentially means handled, the compiler shows a warning. That's
because the `Result` enum is annotated with the `#[must_use]`
attribute. Refer [Result must be
used](https://doc.rust-lang.org/std/result/index.html#results-must-be-used). <a
href="#footnote-1-ref">&#8617;</a>

<b id="footnote-2">2</b>. Note that here we're annotating the inner
type with `#[source]` instead of `#[from]` that we saw earlier. This
is because `Box<dyn Error>` is a generic catch-all, not a specific
type we'd want auto-converted from. <a
href="#footnote-2-ref">&#8617;</a>

