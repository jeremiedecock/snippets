#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

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

import tkinter as tk

color_list = ['aliceblue', 'antiquewhite', 'antiquewhite1', 'antiquewhite2',
    'antiquewhite3', 'antiquewhite4', 'aquamarine', 'aquamarine2',
    'aquamarine4', 'azure', 'azure2', 'azure3', 'azure4', 'bisque', 'bisque2',
    'bisque3', 'bisque4', 'blanchedalmond', 'blue', 'blue2', 'blue4',
    'blueviolet', 'brown', 'brown1', 'brown2', 'brown3', 'brown4',
    'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'cadetblue',
    'cadetblue1', 'cadetblue2', 'cadetblue3', 'cadetblue4', 'chartreuse2',
    'chartreuse3', 'chartreuse4', 'chocolate1', 'chocolate2', 'chocolate3',
    'coral', 'coral1', 'coral2', 'coral3', 'coral4', 'cornflowerblue',
    'cornsilk2', 'cornsilk3', 'cornsilk4', 'cyan', 'cyan2', 'cyan3', 'cyan4',
    'darkgoldenrod', 'darkgoldenrod1', 'darkgoldenrod2', 'darkgoldenrod3',
    'darkgoldenrod4', 'darkgreen', 'darkkhaki', 'darkolivegreen',
    'darkolivegreen1', 'darkolivegreen2', 'darkolivegreen3', 'darkolivegreen4',
    'darkorange', 'darkorange1', 'darkorange2', 'darkorange3', 'darkorange4',
    'darkorchid', 'darkorchid1', 'darkorchid2', 'darkorchid3', 'darkorchid4',
    'darksalmon', 'darkseagreen', 'darkseagreen1', 'darkseagreen2',
    'darkseagreen3', 'darkseagreen4', 'darkslateblue', 'darkslategray',
    'darkslategray1', 'darkslategray2', 'darkslategray3', 'darkslategray4',
    'darkturquoise', 'darkviolet', 'deeppink', 'deeppink2', 'deeppink3',
    'deeppink4', 'deepskyblue', 'deepskyblue2', 'deepskyblue3', 'deepskyblue4',
    'dimgray', 'dodgerblue', 'dodgerblue2', 'dodgerblue3', 'dodgerblue4',
    'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'floralwhite',
    'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'gold2', 'gold3',
    'gold4', 'goldenrod', 'goldenrod1', 'goldenrod2', 'goldenrod3',
    'goldenrod4', 'gray', 'gray1', 'gray10', 'gray11', 'gray12', 'gray13',
    'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19', 'gray2',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26',
    'gray27', 'gray28', 'gray29', 'gray3', 'gray30', 'gray31', 'gray32',
    'gray33', 'gray34', 'gray35', 'gray36', 'gray37', 'gray38', 'gray39',
    'gray4', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46',
    'gray47', 'gray48', 'gray49', 'gray5', 'gray50', 'gray51', 'gray52',
    'gray53', 'gray54', 'gray55', 'gray56', 'gray57', 'gray58', 'gray59',
    'gray6', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray7', 'gray70', 'gray71',
    'gray72', 'gray73', 'gray74', 'gray75', 'gray76', 'gray77', 'gray78',
    'gray79', 'gray8', 'gray80', 'gray81', 'gray82', 'gray83', 'gray84',
    'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray9', 'gray90',
    'gray91', 'gray92', 'gray93', 'gray94', 'gray95', 'gray97', 'gray98',
    'gray99', 'green', 'green2', 'green3', 'green4', 'greenyellow',
    'honeydew2', 'honeydew3', 'honeydew4', 'hotpink', 'hotpink1', 'hotpink2',
    'hotpink3', 'hotpink4', 'indianred', 'indianred1', 'indianred2',
    'indianred3', 'indianred4', 'ivory2', 'ivory3', 'ivory4', 'khaki',
    'khaki1', 'khaki2', 'khaki3', 'khaki4', 'lavender', 'lavenderblush',
    'lavenderblush2', 'lavenderblush3', 'lavenderblush4', 'lawngreen',
    'lemonchiffon', 'lemonchiffon2', 'lemonchiffon3', 'lemonchiffon4',
    'lightblue', 'lightblue1', 'lightblue2', 'lightblue3', 'lightblue4',
    'lightcoral', 'lightcyan', 'lightcyan2', 'lightcyan3', 'lightcyan4',
    'lightgoldenrod', 'lightgoldenrod1', 'lightgoldenrod2', 'lightgoldenrod3',
    'lightgoldenrod4', 'lightgoldenrodyellow', 'lightgrey', 'lightpink',
    'lightpink1', 'lightpink2', 'lightpink3', 'lightpink4', 'lightsalmon',
    'lightsalmon2', 'lightsalmon3', 'lightsalmon4', 'lightseagreen',
    'lightskyblue', 'lightskyblue1', 'lightskyblue2', 'lightskyblue3',
    'lightskyblue4', 'lightslateblue', 'lightslategray', 'lightsteelblue',
    'lightsteelblue1', 'lightsteelblue2', 'lightsteelblue3', 'lightsteelblue4',
    'lightyellow', 'lightyellow2', 'lightyellow3', 'lightyellow4', 'limegreen',
    'linen', 'magenta2', 'magenta3', 'magenta4', 'maroon', 'maroon1',
    'maroon2', 'maroon3', 'maroon4', 'mediumaquamarine', 'mediumblue',
    'mediumorchid', 'mediumorchid1', 'mediumorchid2', 'mediumorchid3',
    'mediumorchid4', 'mediumpurple', 'mediumpurple1', 'mediumpurple2',
    'mediumpurple3', 'mediumpurple4', 'mediumseagreen', 'mediumslateblue',
    'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue',
    'mintcream', 'mistyrose', 'mistyrose2', 'mistyrose3', 'mistyrose4',
    'navajowhite', 'navajowhite2', 'navajowhite3', 'navajowhite4', 'navy',
    'oldlace', 'olivedrab', 'olivedrab1', 'olivedrab2', 'olivedrab4', 'orange',
    'orange2', 'orange3', 'orange4', 'orangered', 'orangered2', 'orangered3',
    'orangered4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'palegoldenrod',
    'palegreen', 'palegreen1', 'palegreen2', 'palegreen3', 'palegreen4',
    'paleturquoise', 'paleturquoise1', 'paleturquoise2', 'paleturquoise3',
    'paleturquoise4', 'palevioletred', 'palevioletred1', 'palevioletred2',
    'palevioletred3', 'palevioletred4', 'papayawhip', 'peachpuff',
    'peachpuff2', 'peachpuff3', 'peachpuff4', 'pink', 'pink1', 'pink2',
    'pink3', 'pink4', 'plum1', 'plum2', 'plum3', 'plum4', 'powderblue',
    'purple', 'purple1', 'purple2', 'purple3', 'purple4', 'red', 'red2',
    'red3', 'red4', 'rosybrown', 'rosybrown1', 'rosybrown2', 'rosybrown3',
    'rosybrown4', 'royalblue', 'royalblue1', 'royalblue2', 'royalblue3',
    'royalblue4', 'saddlebrown', 'salmon', 'salmon1', 'salmon2', 'salmon3',
    'salmon4', 'sandybrown', 'seagreen', 'seagreen1', 'seagreen2', 'seagreen3',
    'seashell2', 'seashell3', 'seashell4', 'sienna1', 'sienna2', 'sienna3',
    'sienna4', 'skyblue', 'skyblue1', 'skyblue2', 'skyblue3', 'skyblue4',
    'slateblue', 'slateblue1', 'slateblue2', 'slateblue3', 'slateblue4',
    'slategray', 'slategray1', 'slategray2', 'slategray3', 'slategray4',
    'snow', 'snow2', 'snow3', 'snow4', 'springgreen', 'springgreen2',
    'springgreen3', 'springgreen4', 'steelblue', 'steelblue1', 'steelblue2',
    'steelblue3', 'steelblue4', 'tan1', 'tan2', 'tan4', 'thistle', 'thistle1',
    'thistle2', 'thistle3', 'thistle4', 'tomato', 'tomato2', 'tomato3',
    'tomato4', 'turquoise', 'turquoise1', 'turquoise2', 'turquoise3',
    'turquoise4', 'violetred', 'violetred1', 'violetred2', 'violetred3',
    'violetred4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'whitesmoke',
    'yellow', 'yellow2', 'yellow3', 'yellow4', 'yellowgreen']

label_width = max([len(s) for s in color_list])
max_columns = 10

root = tk.Tk()
root.title("Named colour chart")

row_index = 0
column_index = 0

for color in color_list:
    label = tk.Label(root, text=color, background=color, font="mono 8", width=label_width)
    label.grid(row=row_index, column=column_index, sticky="ew")

    row_index += 1
    if row_index > (len(color_list) / max_columns):
        row_index = 0
        column_index += 1

root.mainloop()
