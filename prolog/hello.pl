% Usage:
% - with gprolog:
%       - interactive mode:
%           $ gprolog
%           > consult(hello).
%       (see: http://en.literateprograms.org/Hello_World_%28Prolog%29)
%       - compile and exec mode:
%           $ gplc hello.pl
%           $ ./hello
%       (see: http://stackoverflow.com/questions/3576166/hello-world-in-prolog)
% - with swi-prolog:
%       $ swipl hello.pl

:- initialization(main).
main :- write('Hello World!'), nl, halt.
