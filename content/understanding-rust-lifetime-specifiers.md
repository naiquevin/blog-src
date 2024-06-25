Title: Understanding lifetimes in Rust
Author: Vineet Naik
Date: 2024-06-21
Tags: rust
Category: programming
Summary: A tutorial to understand the concept of lifetimes in Rust using practical examples. 
Status: published

This post is a tutorial on Rust lifetimes. It's meant for those who
have some familiarity with the language. I don't claim to be an expert
on this topic. I am new to rust, but at this point I feel comfortable
reading and writing code with lifetimes and it doesn't hinder my
productivity.

The idea for this post came to me while working on
[tapestry](https://github.com/naiquevin/tapestry). I encountered a
situation where I wanted to make a small change to a function and that
necessitated the use of explicit lifetimes. It seemed like a perfect
example to demonstrate the concept of lifetimes. In this post, I'll be
using an example similar to the one in the project.

Let's say we are implementing a static site generator of sorts, in
which the user can write different kind of posts using different
predefined templates. There are two main entities in our code:

1. Templates: Each template has two fields &mdash; `id` and
   `supported_tags`. Consider that templates are "static data"
   i.e. list of templates are hard coded. We'll assume that for all
   templates in the list the `id` fields are unique.

2. Posts: Each post has three fields &mdash; `title`, `template`,
   `tags`. Think of posts as user input. The `template` field refers
   to one of the templates in the static list.

In a real static site generator, templates and posts will likely have
more fields such as `body`, `date` etc. but I'll skip them for
conciseness.

Let's start by implementing structs to represent the above two
entities.

```rust
struct Template {
    id: String,
    supported_tags: HashSet<String>,
}

impl Template {
    fn new(id: &str, supported_tags: Vec<&str>) -> Self {
        Self {
            id: String::from(id),
            supported_tags: supported_tags.iter().map(|s| String::from(*s)).collect(),
        }
    }
}

#[derive(Debug)]
struct Post {
    title: String,
    template: String,
    tags: HashSet<String>,
}

impl Post {
    fn new(title: &str, template: &str, tags: Vec<&str>) -> Self {
        Self {
            title: String::from(title),
            template: String::from(template),
            tags: tags.iter().map(|s| String::from(*s)).collect(),
        }
    }
}
```

We've defined `new` methods for both structs which will come handy
while instantiating them.

Since posts represent user input, they need to be validated. We'll
verify two simple constraints:

1. the `template` field of a post must match the `id` of one of the
   predefined templates.

2. `tags` field of a post must be a subset of the `supported_tags`
   field of the associated template

Let's represent the above validation errors using an enum. Because the
term "error" is conventionally used to name `Error` types in rust, I
am using "mistake" to avoid confusion.

```
#[derive(Debug)]
enum Mistake {
    TemplateRefNotFound {
        title: String,
        template_id: String,
    },
    UnsupportedTags {
        title: String,
        tags: HashSet<String>,
    },
}
```

Now let's define a `validate` method in the `Post` struct.

```rust
impl Post {
    fn validate(&self, templates: &Vec<Template>) -> Vec<Mistake> {
        let mut mistakes = vec![];
        match templates.iter().find(|x| x.id == self.template) {
            Some(tmpl) => {
                if !self.tags.is_subset(&tmpl.supported_tags) {
                    let m = Mistake::UnsupportedTags {
                        title: self.title.clone(),
                        tags: self.tags.clone(),
                    };
                    mistakes.push(m);
                }
            }
            None => {
                let m = Mistake::TemplateRefNotFound {
                    title: self.title.clone(),
                    template_id: self.template.clone(),
                };
                mistakes.push(m);
            }
        }
        mistakes
    }
}
```

We can now try out a few examples in the main function. We'll also
define a helper function to validate a post and print the "mistakes"
i.e. validation errors to `stdout`.

```rust
fn validate_post(post: &Post, templates: &Vec<Template>) {
    let mistakes = post.validate(&templates);
    println!("{} mistakes found for {post:?}", mistakes.len());
    if mistakes.len() > 0 {
        for mistake in mistakes {
            println!("  {mistake:?}");
        }
    }
}

fn main() {
    let templates = vec![
        Template::new("blog", vec!["opinion", "report", "personal"]),
        Template::new(
            "announcement",
            vec!["new project", "update", "security", "urgent"],
        ),
    ];

    let post = Post::new(
        "Major security update",
        "announcement",
        vec!["security", "update", "urgent"],
    );

    validate_post(&post, &templates);

    let post = Post::new("A day at the beach", "blog", vec!["personal", "song"]);
    validate_post(&post, &templates);
}
```

Running it prints the following to `stdout`.

```shell
$ cargo run
0 mistakes found for Post { title: "Major security update", template: "announcement", tags: {"urgent", "update", "security"} }
1 mistakes found for Post { title: "A day at the beach", template: "blog", tags: {"personal", "song"} }
  UnsupportedTags { title: "A day at the beach", tags: {"personal", "song"} }
```

Here is [Rust playground link]() if you wish to try it. I'll refer to
this version as the first iteration.

### Using references instead of cloning

The above code works but is not memory efficient. Notice that in the
`Post.validate` method, we're cloning the `String` objects. Rust is a
low level language that's designed for writing memory efficient
code. Instead of cloning data, it's possible to refer to the existing
data in memory by using references.

What if we define the `Mistake` enum in terms of reference type `&str`
instead of owned type `String`?

```rust
#[derive(Debug)]
enum Mistake {
    TemplateRefNotFound {
        title: &str,
        template_id: &str,
    },
    UnsupportedTags {
        title: &str,
        tags: HashSet<&str>,
    }
}
```

It fails with a compilation error.

```rust
error[E0106]: missing lifetime specifier
  --> examples/itr2.rs:45:18
   |
45 |     item_id: &str,
   |              ^ expected named lifetime parameter
```

The error says `missing lifetime specifier`. Great! So we've finally
encountered the term `lifetime`.

The fix is to specify lifetime parameter when defining the `Mistake`
enum as follows,

```rust
#[derive(Debug)]
enum Mistake<'a> {
    TemplateRefNotFound {
        title: &'a str,
        template_id: &'a str,
    },
    UnsupportedTags {
        title: &'a str,
        tags: &'a HashSet<String>,
    },
}
```

Then modify the definition of the `Post.validate` method to explicitly
specify the lifetime.

```rust
impl Post {
    fn validate<'a>(&'a self, templates: &Vec<Template>) -> Vec<Mistake<'a>> {
       // Body of the fn remains the same
    }
}
```

Now it compiles. All we've done is redefine the enum and the method
with weird looking syntax `<'a>` and `&'a`. What do these tokens mean
and how does it work?

First, let's step back a bit and understand why references make the
code memory efficient. If you're familiar with low level languages
such as C, C++, you may skip the next paragraph.

A reference is nothing but a pointer to a memory location. Since the
data that we want to store in `title`, `template_id` and `tags` fields
of a `Mistake` instance already exists in memory (as fields of a
`Post` instance), we can just store the reference to those same memory
locations in a `Mistake` instance instead of cloning the data. That
way, an instance of `Mistake` enum returned by `Post.validate` method
will not require additional memory.

But rust has a concept of ownership. The data that we want to "reuse"
in `Mistake` is owned by a `Post` instance. In creating references to
that data, we are "borrowing" from that `Post` instance. The compiler
will allow this only if it can statically check that the owner
outlives (or lives as long as) the borrower i.e. the `Post` instance
gets dropped only after `Mistake` instance is dropped. This is to
prevent dangling references.

The specifier `'a` used in the enum definition is to say that an
instance of the enum will live only as long as lifetime `'a`. The
value of lifetime `'a` is not something that you, the author of the
code is supposed to know. It depends on the code that calls the
`Post.validate` method and will be figured out by the borrow checker
during compilation.

### Generics

This post is about lifetimes and not generics, so I won't spend much
time on this topic. However lifetimes are similar to generics and the
syntax is also the same. Unlike lifetimes, the concept of generics is
not unique to Rust[FN]. Hence comparing the two concepts may help those
who are experienced in other languages that have generics.

Generics help us avoid code duplication e.g. to define a single
function that works for multiple concrete data types. But how does it
actually work?

Consider following function that's generic over type `T`.

```rust
fn max<T>(xs: &[T]) -> &T {
    // ...
}
```

At compile time, the compiler will look at code that calls this
function and substitute the value `T` with the actual data types that
it's called with. Think of it like how a function argument gets
substituted by the actual value at runtime.

Coming back to lifetimes, it kinda works the same way. The syntax is
also similar. Before using a generic type, it's name is declared using
the `<T>` syntax. Similarly, before we can use a lifetime parameter,
it's name is declared as `<'a>`. At compile time, `'a` will be
substituted by the actual lifetime of the object from where the `&'a`
references are borrowed. Based on that the borrow checker will check
whether the owner outlives the borrower. I am simplifying a lot here
so all this may not accurately represent the actual implementation of
the borrow checker.

Let's try to call `validate` such that the lifetime check is not
satisfied. Add the following lines to the `main` function.

```rust
let post = Post::new("A day at the beach", "blog", vec!["personal", "song"]);
validate_post(&post, &templates);

let mistakes = {
    let post = Post::new("A day at the beach", "blog", vec!["personal", "song"]);
    post.validate(&templates)
};
println!("{} mistakes found for {post:?}", mistakes.len());
```

It doesn't compile. The error is:

```rust
error[E0597]: `post` does not live long enough
   --> examples/itr2.rs:147:9
|
145 | let mistakes = {
|         -------- borrow later stored here
146 |     let post = Post::new("A day at the beach", "blog", vec!["personal", "song"]);
|             ---- binding `post` declared here
147 |     post.validate(&templates)
|         ^^^^ borrowed value does not live long enough
148 | };
|     - `post` dropped here while still borrowed
```

The error message itself does a great job of explaining what's
happening. But the point is, the compiler can enforce this because of
the lifetime parameter specified in the enum definition.

Before proceeding with the next example, what if I told you that the
change we did to the `Post.validate` method definition was not
required? Remove the lifetime specifiers from the method definition
and try compiling.

```rust
impl Post {
    fn validate(&self, templates: &Vec<Template>) -> Vec<Mistake> {
       // Body of the fn remains the same
    }
}
```

It does compile. That's because of [lifetime
elison](https://doc.rust-lang.org/reference/lifetime-elision.html). Just
like rust's compiler can infer types, it can also infer lifetimes in
certain situations.

Here is [Rust playground link]() for the second iteration.

### Borrowing from multiple owners

Now let's try to make a trivial improvement to the validation code. We
can make the `Mistake::UnsupportedTags` validation error/mistake more
helpful to the user by mentioning which tags are supported. For this,
we'll need to define one more field for the `UnsupportedTags` variant
and modify the `validate` method to populate it with a reference to
the `supported_tags` field of the corresponding template.

```rust
#[derive(Debug)]
#[allow(unused)]
enum Mistake<'a> {
    TemplateRefNotFound {
        title: &'a str,
        template_id: &'a str,
    },
    UnsupportedTags {
        title: &'a str,
        tags: &'a HashSet<String>,
        supported_tags: &'a HashSet<String>,
    },
}

// ...

impl Post {
    fn validate(&self, templates: &Vec<Template>) -> Vec<Mistake> {
        let mut mistakes = vec![];
        match templates.iter().find(|x| x.id == self.template) {
            Some(tmpl) => {
                if !self.tags.is_subset(&tmpl.supported_tags) {
                    let m = Mistake::UnsupportedTags {
                        title: &self.title,
                        tags: &self.tags,
                        supported_tags: &tmpl.supported_tags,
                    };
                    mistakes.push(m);
                }
            }
            None => {
                let m = Mistake::TemplateRefNotFound {
                    title: &self.title,
                    template_id: &self.template,
                };
                mistakes.push(m);
            }
        }
        mistakes
    }
}
```

Our code doesn't compile any more.

```rust
error: lifetime may not live long enough
   --> examples/itr3.rs:110:9
|
89  | fn validate(&self, templates: &Vec<Template>) -> Vec<Mistake> {
|                 -                 - let's call the lifetime of this reference `'1`
|                 |
|                 let's call the lifetime of this reference `'2`
...
110 |     mistakes
|         ^^^^^^^^ method was supposed to return data with lifetime `'2` but it is returning data with lifetime `'1`
```

The `Mistake::UnsupportedTags` instance now borrows from two owners
&mdash; the two arguments `self` and `templates` of the
`Post.validate` method. The borrow checker cannot infer the lifetimes
any more. The compilation error indicates the presence of two
lifetimes. To fix this, we can explicitly specify two lifetime
specifiers and establish a relationship between them.

```rust
impl Post {
    fn validate<'a, 'b>(&'a self, templates: &'b Vec<Template>) -> Vec<Mistake<'a>>
    where 'b: 'a {
        // Body of the fn remains the same
    }
}
```

The `where 'b: 'a` is called `lifetime bound` which is similar to a
[trait
bound](https://doc.rust-lang.org/reference/trait-bounds.html). It
means that lifetime `'b` lasts at least as long as `'a`. We need to
tell this to the borrow checker because the lifetime associated with
the return type of the method is `'a` (notice the `<'a>` in the return
type). Hence the borrow checker will allow it only if the condition
that `'a` is the shorter of the two lifetimes is satisfied. Using
lifetime bounds we're making that explicit.

Actually, I lied again! It's possible to define the `validate` method
using just one lifetime specifier. In fact, the compiler error we saw
earlier exactly shows how to do it but I intentionally omitted that
part because I wanted to show a verbose version, which I believe is
explicit and hence easier to understand.

The following definition of `validate` also compiles.

```rust
impl Post {
    fn validate<'a>(&'a self, templates: &'a Vec<Template>) -> Vec<Mistake<'a>> {
        // Body of the fn remains the same
    }
}
```

Why does it work? Remember that the lifetime specifier in function
definition `'a` is abstract and the borrow checker will substitute it
with the actual lifetimes of the function arguments from where the
references are borrowed by the returned value. If the actual lifetimes
of the function arguments happen to be different, the borrow checker
is smart enough to use the shorter of the two lifetimes as `'a`.

We can try out the error case again and it won't compile.

```rust
let templates = vec![
    Template::new("blog", vec!["opinion", "report", "personal"]),
    Template::new(
        "announcement",
        vec!["new project", "update", "security", "urgent"],
    ),
];

// ...

let mistakes = {
    let post = Post::new("A day at the beach", "blog", vec!["personal", "song"]);
    post.validate(&templates)
};
println!("{} mistakes found for {post:?}", mistakes.len());
```

The borrow checker will substitute `'a` with the lifetime of `post`
because it's shorter than the lifetime of `templates`. When we try to
use the returned value (`mistakes`) in the `println!` macro, `post` is
already dropped. That's why the code doesn't compile.

### That's all

Here's a recap of what we did:

- We started with an inefficient implementation by cloning Strings
- In the second iteration, we used references by defining lifetime
  specifiers in the enum. We also found out that specifiers were not
  needed in this case due to lifetime elison.
- In the third iteration, we made the validation error message user
  friendly. In doing so, we had to bring back the lifetime specifiers
  in the function definition. We also found out that it was not
  necessary to use two lifetime parameters even though the data being
  returned was borrowed from two different args. The borrow checker is
  smart enough to "plug-in" the shorter of the two lifetimes.

### Summary

- Whenever a data structure holds a reference, it's borrowing a value
  from some owner.
- When a function returns a reference, it borrows from one or more of
  the args (also references).
- As rust is a _gc-less_ language, a value gets automatically dropped
  when it goes out of scope. So the compiler has to ensure that the
  owner of a value lives at least as long as the borrower.
- When the compiler can't infer where a value is being borrowed from,
  it also can't infer it's lifetime. In such cases, we need to use
  explicit lifetime specifiers.

Note that the above summary is grossly oversimplified but I believe it
helps understand and remember the concept of lifetimes. You should
refer to the the Rust book for accurate information.
