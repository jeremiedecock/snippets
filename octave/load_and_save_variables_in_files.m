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


% Create the "m" variable (a matrix here)
m = [0 1 2 3; 4 5 6 7; 8 9 10 11];

% Print the "m" variable
disp ("The value of m is "), disp(m);

% Save the "m" variable in the "test2.dat" file
save("test2.dat","m")

clear m;
who;

% Load the "test2.dat" file in the "m" variable
load "test2.dat";

% Print the "m" variable
disp ("The value of m is "), disp(m);

