#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Required package (on Debian8):
# - BeautifulSoup4: python3-bs4

# Online documentation:
# - BeautifulSoup4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# - Urllib:         https://docs.python.org/3/library/internet.html
#                   https://docs.python.org/3/library/urllib.request.html

import argparse
from bs4 import BeautifulSoup
import json
import os
import os.path
import random
import re
import shutil
import time
import urllib.request
from urllib.parse import urljoin

import crawler
from http_headers import HTTP_HEADERS

MEAN_TIME_SLEEP = 15
STD_TIME_SLEEP = 5

class MoocFunNode(crawler.Node):

    def __init__(self, url, depth):
        self.url = url

        #self.html = urllib.request.urlopen(self.url).read()

        request = urllib.request.Request(self.url, data=None, headers=HTTP_HEADERS)
        response = urllib.request.urlopen(request)
        self.html = response.read()

        #with open("mooc.htm", "r") as fd:
        #    self.html = fd.read()

        self.depth = depth


    @property
    def child_nodes(self):
        child_nodes_set = set()

        if self.depth == 0:
            for course_url in self.courses:
                child_nodes_set.add(MoocFunNode(course_url, self.depth + 1))

        return child_nodes_set


    def visit(self):
        """Do something with node value."""
        print("Visiting {}...".format(self.url))

        if self.depth == 0:
            print("I'm visiting the root node...")

            # Export the table of contents
            toc_dict = self.table_of_contents
            with open("test.json", "w") as fd:
                json.dump(toc_dict, fd, sort_keys=True, indent=4)  # pretty print format

        elif self.depth == 1:
            courses_dict = self.courses
            #with open("test2.json", "w") as fd:
            #    json.dump(courses_dict, fd, sort_keys=True, indent=4)  # pretty print format

            chap_name = courses_dict[self.url]["chap_name"]
            title = courses_dict[self.url]["title"]

            if not os.path.exists(chap_name):
                os.mkdir(chap_name)

            soup = BeautifulSoup(self.html)

            video_num = 0
            for sec_div in soup.find_all(id=re.compile('^seq_contents_')):
                print(sec_div['id'])

                embeded_html = sec_div.string
                soup2 = BeautifulSoup(embeded_html)

                for anchor in soup2.find_all('a'):
                    if anchor.string == "Haute définition (720p)":
                        video_num += 1
                        video_url = anchor['href']

                        video_filename = os.path.join(chap_name, "{}_video{}.mp4".format(title, video_num))

                        print(video_filename, video_url)

                        request = urllib.request.Request(video_url, data=None, headers=HTTP_HEADERS)
                        with urllib.request.urlopen(request) as response, open(video_filename, 'wb') as out_file:
                            shutil.copyfileobj(response, out_file)

                        # Wait a litte bit
                        time.sleep(random.gauss(MEAN_TIME_SLEEP, STD_TIME_SLEEP))


#    @property
#    def courses(self):
#        courses_set = set()
#
#        soup = BeautifulSoup(self.html)
#
#        for chap_div in soup.find_all('div', 'chapter'):
#            for course_li in chap_div.find_all('li'):
#                course_relative_url = course_li.a['href']
#                course_absolute_url = urljoin(self.url, course_relative_url)
#                courses_set.add(course_absolute_url)
#
#        return courses_set


    @property
    def courses(self):
        """
        {
            "url_cours_1":
                {"chap_name":"Semaine 1", "title":"cours 1", "subtitle":"..."},
            "url_cours_2":
                {"chap_name":"Semaine 1", "title":"cours 2", "subtitle":"..."},
            "url_cours_3":
                {"chap_name":"Semaine 2", "title":"cours 3", "subtitle":"..."},
            ...
        }
        """

        courses_dict = {}

        #print(self.html)

        soup = BeautifulSoup(self.html)

        for chap_div in soup.find_all('div', 'chapter'):
        #for chap_div in soup.find_all('div', {'class': 'chapter'}):
        #for chap_div in soup.find_all('div'):
            chap_name = str(chap_div.h3.a.string).strip()
            #print(chap_div)

            for course_num, course_elem in enumerate(chap_div.find_all('li')):
                course_title = str(course_elem.a.p.string).strip()

                course_relative_url = course_elem.a['href']
                course_absolute_url = urljoin(self.url, course_relative_url)

                course_desc = {"chap_name": re.sub('[.,;:!?]', '', chap_name.lower().replace(' ', '_')),
                               "title": re.sub('[.,;:!?]', '', course_title.lower().replace(' ', '_'))}
                courses_dict[course_absolute_url] = course_desc

        return courses_dict


    @property
    def table_of_contents(self):
        """
        {
            "semaine 1": [
                {"title":"cours 1", "subtitle":"...", "url":"..."},
                {"title":"cours 2", "subtitle":"...", "url":"..."},
                ...
            ],
            "semaine 2": [
                {"title":"cours 1", "subtitle":"...", "url":"..."},
                {"title":"cours 2", "subtitle":"...", "url":"..."},
                ...
            ],
        }
        """

        toc_dict = {}

        soup = BeautifulSoup(self.html)

        for chap_div in soup.find_all('div', 'chapter'):
            chap_str = str(chap_div.h3.a.string).strip()
            toc_dict[chap_str] = []
            #print(chap_str)

            for course_num, course_li in enumerate(chap_div.find_all('li')):
                course_title = str(course_li.a.p.string).strip()

                course_subtitle = ""
                for subtitle_p in course_li.a.find_all('p', 'subtitle'):
                    course_subtitle = str(subtitle_p.string).strip()

                course_relative_url = course_li.a['href']
                course_absolute_url = urljoin(self.url, course_relative_url)

                #print("- Cours", course_num + 1)
                #print("  - title:", course_title)
                #print("  - subtitle:", course_subtitle)
                #print("  - url:", course_absolute_url)
                toc_dict[chap_str].append({"title": course_title, "subtitle": course_subtitle, "url": course_absolute_url})

        return toc_dict


    @property
    def is_final(self):
        return True


def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='A BeautifulSoup snippet.')
    parser.add_argument("url", nargs=1, metavar="URL",
                        help="The URL of the webpage to parse.")
    args = parser.parse_args()

    url = args.url[0]

    # TRAVERSE THE GRAPH ######################################################

    start_node = MoocFunNode(url, depth=0)
    crawler.walk(start_node)

    # PRINT TRAVERSED NODES ###################################################

    print("Traversed nodes:")
    for node in crawler.Node.traversed_nodes:
        print(" ", node)


if __name__ == '__main__':
    main()

