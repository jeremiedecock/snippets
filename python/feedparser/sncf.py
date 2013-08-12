#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser

rss_url = "http://www.transilien.com/flux/rss/traficLigne?codeLigne=D"

feed_dict = feedparser.parse(rss_url)

for key, value in feed_dict.items():
    print key, ':', value

print

print [(entry['published'], entry['title']) for entry in feed_dict.entries]
