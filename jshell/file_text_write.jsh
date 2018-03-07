//usr/bin/env jshell --execution local "$0" "$@"; exit $?

// See:
// - https://stackoverflow.com/questions/15803350/filewrite-bufferedwriter-and-printwriter-combined
// - https://stackoverflow.com/questions/5949926/what-is-the-difference-between-append-and-write-methods-of-java-io-writer
// - https://docs.oracle.com/javase/9/docs/api/java/io/FileWriter.html
// - https://docs.oracle.com/javase/9/docs/api/java/io/BufferedWriter.html
// - https://docs.oracle.com/javase/9/docs/api/java/io/PrintWriter.html

// Methode 1: FileWriter
// Available methods: append() close() equals() flush() getClass() getEncoding() hashCode() notify() notifyAll() toString() wait() write()
FileWriter out = new FileWriter("test1.txt");
out.append("Hello!\n");
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();
System.out.println(out.getEncoding());

// Methode 2: BufferedWriter
// Available methods: append() close() equals() flush() getClass() hashCode() newLine() notify() notifyAll() toString() wait() write()
BufferedWriter out = new BufferedWriter(new FileWriter("test2.txt"));  // The buffer size can also be defined in BufferedWriter constructor
out.append("Hello!\n");
//out.newLine();
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

// Methode 3: PrintWriter
// Available methods: append() checkError() close() equals() flush() format() getClass() hashCode() notify() notifyAll() print() printf() println() toString() wait() write()
PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("test3.txt")));
//or PrintWriter out = new PrintWriter(new FileWriter("test.txt"));
out.print("Hello ");
out.println("World!")
out.append("Hello!\n");
//out.newLine();
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

/exit
