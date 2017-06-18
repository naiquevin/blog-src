#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Vineet Naik'
SITENAME = u"/home/vineet"
SITETITLE = u"Vineet's mind space on the internet"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

THEME = 'naiq'

MENUITEMS = (('feed', '/feeds/all.atom.xml'),
             ('music', '/pages/music.html'),
             ('talks', '/pages/talks.html'),
             ('code', '/pages/code.html'),
             ('about', '/pages/about-me.html'),)

DEBUG = True

# MD_EXTENSIONS = ['codehilite(css_class=codehilite)','extra']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'codehilite'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5'
}

STATIC_PATHS = ['talks']

PAGE_EXCLUDES = ['talks']
ARTICLE_EXCLUDES = ['pages', 'talks']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
