#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Vineet Naik'
SITENAME = u'/home/vineet'
SITETITLE = u'Vineet\'s mind space on the internet'
SITEURL = ''

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

THEME = 'naiq'

MENUITEMS = (('feed', '/feeds/all.atom.xml'),
             ('music', '/pages/music.html'),
             ('talks', '/pages/talks.html'),
             ('code', 'http://github.com/naiquevin'),
             ('about', '/pages/about-me.html'),)


DEBUG = True

MD_EXTENSIONS = ['codehilite(css_class=codehilite)','extra']

STATIC_PATHS = ['talks']

PAGE_EXCLUDES = ['talks']
ARTICLE_EXCLUDES = ['pages', 'talks']
            
