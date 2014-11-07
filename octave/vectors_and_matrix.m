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


% Create vector variables
v1 = 1:20
v2 = 1:2:39
v3 = [0 0 0 0 0 0]
v4 = v3
v4(3) = 1

% Create matrix variables
m1 = [0 1 2 3; 4 5 6 7; 8 9 10 11];
m2 = ones(5,3);
m3 = zeros(5,3);
m4 = eye(4);
m5 = m1';    % Transpose
m6 = m3;
m6(2,1) = 1;
m7 = ones(4,4) * 3

% Print the variables
disp ("The value of v1 is "), disp(v1);
disp ("The value of v2 is "), disp(v2);
disp ("The value of v3 is "), disp(v3);
disp ("The value of v4 is "), disp(v4);
disp ("The value of m1 is "), disp(m1);
disp ("The value of m2 is "), disp(m2);
disp ("The value of m3 is "), disp(m3);
disp ("The value of m4 is "), disp(m4);
disp ("The value of m5 is "), disp(m5);
disp ("The value of m6 is "), disp(m6);
disp ("The value of m7 is "), disp(m7);

