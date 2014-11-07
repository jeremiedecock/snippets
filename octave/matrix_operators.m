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

% Create matrix variables
m1 = [0 1 2 3; 4 5 6 7; 8 9 10 11];
m2 = [1 2 3; 4 5 6; 7 8 9];
m3 = [4 7 3; 5 1 6; 9 3 2];
v1 = [0 0 0 0 0 0];
v2 = [0 0 0 0 0 0];

m1'           % transpose
m1(1,1) = 3   % changes the value of the top-left element (indices start at 1 not at 0!)
m1 *= 2       % or m1=m1*2  -> multiply m1 by the scalar 2

m2*m3         % scalar product
m2.*m3        % element wise product

m2^2          % scalar product
m2.^2         % element wise product

size(m1)
size(m1,1)    % num rows
size(m1,2)    % num columns

m1(2,:)       % get the second row of m1
m1(:,3)       % get the third column of m1

m4 = zeros(4,3)
m4(1:3,1:2) = 1  % put 1 in some elements of the matrix

% Sort a matrix
% S: a copy of the sorted matrix
% I: former indices of elements
[S, I] = sort([1 2; 2 3; 3 1])

% Reshape
m5 = rand(5,5)
m5 = reshape(m5, 25, 1)   % create a matrix 25x1
m5 = reshape(m5, 5, 5)    % create a matrix 5x5

% Max value and argmax (by columns)
[maxvalues, indices] = max(m1)

% Find non zero elements
m6 = floor(rand(10,1)*2)
find(m6)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

v1(1:3) += 1        % or v1(1:3) = v1(1:3)+1  -> return v1=[1 1 1 0 0 0]
v2(end-2:end) += 1  % or v2(end-2:end) = v2(end-2:end)+1  -> return v2=[0 0 0 1 1 1]

v1 = [0 1 2 3]
v2 = [4;5;6;7]
v1*v2               % scalar product
v1.*v2'             % element wise product

length(v1)
