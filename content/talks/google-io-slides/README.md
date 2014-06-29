Google IO Slides adapted for Pelican
====================================

The original code for Google IO Slides is available
[here](https://code.google.com/p/io-2012-slides)

I have rearranged and modified it to make it easy to host the slides
for multiple presentations while sharing most of the javascript and
css code.

I write the slides using markdown and then use the markdown generator
script (packaged with the Google IO Slides code) to build the html
presentation. Currently this setup doesn't support generating output
html file directly under the dir of pelican instance so it needs to be
generated separately and copied under the `content/talks/<talk-name>`
dir manually.

Steps to copy files:

* Copy files as follows,

  - `cp <src>/presentation_output.html <pelican>/content/talks/<talkname>/index.html`
  - `cp <src>/slide_config.js <pelican>/content/talks/<talkname>/slide_config.js`
  - `cp <src>/scripts/md/slides.md <pelican>/content/talks/<talkname>/slides.md`
  - Copy any other dirs for static assets such as `images` or `theme`
    if you have added or edited CSS/SCSS.

* Edit `<pelican>/content/talks/<talkname>/index.html` as follows,

  - Prefix `href` attr of link tags for CSS stylesheets with
    `/talks/google-io-slides/`.
  - Prefix `src` and `data-main` for the require.js script tag with
    `/talks/google-io-slides/`.
  - Before the require.js script tag, add the line to manually include
    the slide_config.js `<script src="slide_config.js"></script>`.

    Note: This is because `slide_config.js` file is not loaded via
    require.js so that every presentation can have it's own
    `slide_config.js` file.

  - Add google analytics code.

