Title: Tapestry 0.2.0 and 0.2.1
Author: Vineet Naik
Date: 2024-09-18
Tags: release, tapestry
Category: programming
Summary: Tapestry versions 0.2.0 and 0.2.1 released with fixes and new features
Status: published

The first working version of
[tapestry](https://github.com/naiquevin/tapestry) was released a few
months ago. Since then, I have been working on implementing features
beyond my own requirements and use cases. The version `0.2.0`, which
includes some of the new capabilities was released last
week. Yesterday, a patch version `0.2.1` was released fixing a
regression (that originated in `0.1.0`).

## Bug fixes

- The
  [status](https://naiquevin.github.io/tapestry/user-guide/commands/#status)
  command has been fixed to work correctly with `one-file-all-queries`
  [layout](https://naiquevin.github.io/tapestry/user-guide/layouts/)
  and
  [name-tagging](https://naiquevin.github.io/tapestry/user-guide/query-tags/). It
  was broken ever since both these features were implemented.

## Features

- Tapestry now comes with a builtin SQL formatter based on the
  `sqlformat-rs` crate. This removes the dependency on `pg_format` for
  SQL formatting, although it can still be used optionally (see next
  point).

- Besides the builtin formatter, three external SQL formatting tools
  are now supported -
  [pg_format](https://github.com/darold/pgFormatter),
  [sql-formatter](https://github.com/sql-formatter-org/sql-formatter),
  [sqlfluff](https://sqlfluff.com/).

## What's next?

- As mentioned earlier, I don't use some of the newer features
  myself. So I believe there are still some edge cases that need to be
  handled. The plan is to write more unit tests and aim for decent
  coverage, specially for such features.

- I am happy to add support for other external SQL formatters. If
  there's a particular formatter that you'd like to see supported,
  feel free to create an issue on github.

- A command for generating boilerplate code for pgTAP tests. I
  occasionally miss this feature myself, so it's definitely high on my
  list.

- I recently found out that an equivalent of pgTAP exists for MySQL -
  [mytap](https://github.com/hepabolu/mytap). It also seems to be
  (originally) [written
  by](https://justatheory.com/2010/07/introducing-mytap/) David
  Wheeler, the author of pgTAP. I think it makes a lot of sense for
  tapestry to support it.
