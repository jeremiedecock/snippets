//usr/bin/env jshell --execution local "$0" "$@"; exit $?

Path currentPath = Paths.get(System.getProperty("user.dir"));
Path filePath = Paths.get(currentPath.toString(), "foo", "bar.txt");
System.out.println(filePath.toString());

/exit
