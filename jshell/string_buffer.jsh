//usr/bin/env jshell --execution local "$0" "$@"; exit $?

StringBuffer buffer = new StringBuffer();

buffer.append("Hell");
buffer.append(" World ");
buffer.append('!');
buffer.insert(4, 'o');

System.out.println(buffer);

/exit
