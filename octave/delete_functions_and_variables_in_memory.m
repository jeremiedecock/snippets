#!/usr/bin/octave -q

% Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
%
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
%
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
% THE SOFTWARE.

% Usage: octave -q <THIS_FILE_NAME>

function [somme, produit] = testFunction(arg1, arg2)
    somme = arg1 + arg2;
    produit = arg1 * arg2;
endfunction

[m1,m2] = testFunction(2,3)

% Print functions and variables in memory
who;
disp ("The value of m1 is "), disp(m1);
disp ("The value of m2 is "), disp(m2);

% Delete functions and variables in memory
clear all;

% Print functions and variables in memory
who;
disp ("The value of m1 is "), disp(m1);
disp ("The value of m2 is "), disp(m2);
