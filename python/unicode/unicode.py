#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

# DEFINE
str1 = "Hello!"
unicode_obj1 = u"¡Buenos días!"
unicode_obj2 = u"你好！"

# PRINT

print
print str1
print unicode_obj1
print unicode_obj2

# CONCAT

print
print str1 + " " + unicode_obj1 + " " + unicode_obj2,
print type(str1 + " " + unicode_obj1 + " " + unicode_obj2)

# PRINT TYPE

print
print str1,  type(str1)
print unicode_obj1, type(unicode_obj1)
print unicode_obj2, type(unicode_obj2)

# LENGTH

print
print "len(", unicode_obj2, ") = ", len(unicode_obj2)
print u"len({0}) = {1}".format(unicode_obj2, len(unicode_obj2))
print u"len(%s) = %s" % (unicode_obj2, len(unicode_obj2))

# UNICODE TO ASCII (你好！ -> )


# ASCII TO UNICODE ( -> 你好！)


# UNICODE TO HEX ASCII (你好！ -> hex)

print
hex_str = unicode_obj2.encode("utf-8").encode("hex")
print "{0} {1} (len: {2})".format(hex_str, type(hex_str), len(hex_str))

hex_list = [unicode_char.encode("utf-8").encode("hex") for unicode_char in unicode_obj2]
print(hex_list)

