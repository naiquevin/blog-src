"""Script to overwrite html files that are hosted at
naiquevin.github.io with html that will indicate canonical url and
redirect to it (hosted at the new location www.naiquev.in)

Usage:

  cd naiquevin.github.com/

  # First execute in dry run
  python ../blog-src/canonical_redirect.py . 1 index.html

  # Test for 1 file (without dry-run)
  python ../blog-src/canonical_redirect.py . 0 index.html

  # Find all html files and run the script for each
  find . -type f -name "*.html" \
       | sed 's/\.\///g' \
       | xargs -n 1 -P 8 python ../blog-src/tools/canonical_redirect.py . 0

"""

import os
import sys

rd = os.path.expanduser("~/blog/naiquevin.github.com")


template = """<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0;url=https://www.naiquev.in/{path}" />
    <link rel="canonical" href="https://www.naiquev.in/{path}" />
  </head>
  <body>
    <h1>
      The page been moved to <a href="https://www.naiquev.in/{path}">https://www.naiquev.in/{path}</a>
    </h1>
  </body>
</html>
"""""


def replace_html(rootdir, path, dry_run=False):
    filepath = os.path.join(rootdir, path)
    content = template.format(path=path)
    if dry_run:
        print("Dry run - No changes will be made")
        print(content)
    else:
        print("Overwriting file: {0}".format(filepath))
        with open(filepath, "w") as f:
            f.write(content)


def main():
    rootdir, dry_run, path = sys.argv[1:]
    is_dry_run = dry_run != "0"
    replace_html(rootdir, path, is_dry_run)


if __name__ == '__main__':
    main()
