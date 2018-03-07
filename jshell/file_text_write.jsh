//usr/bin/env jshell --execution local "$0" "$@"; exit $?

// See:
// - https://stackoverflow.com/questions/15803350/filewrite-bufferedwriter-and-printwriter-combined
// - https://stackoverflow.com/questions/5949926/what-is-the-difference-between-append-and-write-methods-of-java-io-writer
// - https://stackoverflow.com/questions/6998905/java-bufferedwriter-object-with-utf-8
// - http://tutorials.jenkov.com/java-nio/nio-vs-io.html
// - https://docs.oracle.com/javase/9/docs/api/java/io/FileWriter.html
// - https://docs.oracle.com/javase/9/docs/api/java/io/BufferedWriter.html
// - https://docs.oracle.com/javase/9/docs/api/java/io/PrintWriter.html
// - https://docs.oracle.com/javase/9/docs/api/java/nio/file/Files.html
// - https://docs.oracle.com/javase/9/docs/api/java/nio/file/Paths.html 
// - https://docs.oracle.com/javase/9/docs/api/java/nio/charset/Charset.html
// - https://docs.oracle.com/javase/9/docs/api/java/nio/file/StandardOpenOption.html

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

String PATH = "test.txt";

// Methode 1: FileWriter
// Available methods: append() close() equals() flush() getClass() getEncoding() hashCode() notify() notifyAll() toString() wait() write()
FileWriter out = new FileWriter(PATH);
out.append("Hello!\n");
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();
System.out.println(out.getEncoding());

// Methode 2: BufferedWriter
// Available methods: append() close() equals() flush() getClass() hashCode() newLine() notify() notifyAll() toString() wait() write()
BufferedWriter out = new BufferedWriter(new FileWriter(PATH));  // The buffer size can also be defined in BufferedWriter constructor
out.append("Hello!\n");
//out.newLine();
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

// Methode 3: PrintWriter
// Available methods: append() checkError() close() equals() flush() format() getClass() hashCode() notify() notifyAll() print() printf() println() toString() wait() write()
PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(PATH)));
//or PrintWriter out = new PrintWriter(new FileWriter("test.txt"));
out.print("Hello ");
out.println("World!")
out.append("Hello!\n");
//out.newLine();
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

// Methode 4: FileOutputStream wrapped in OutputStreamWriter
// The problem with above methods is that they don't let you specify the encoding, it always use the system encoding...
// See https://stackoverflow.com/questions/6998905/java-bufferedwriter-object-with-utf-8 and https://docs.oracle.com/javase/9/docs/api/java/io/FileWriter.html
// Available methods: append() close() equals() flush() getClass() getEncoding() hashCode() notify() notifyAll() toString() wait() write()
OutputStreamWriter out = new OutputStreamWriter(new FileOutputStream(PATH), StandardCharsets.UTF_8);
// or OutputStreamWriter out = new OutputStreamWriter(new FileOutputStream(PATH), "UTF-8");
out.append("Hello!\n");
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

// Methode 5: same as method 4 but with an additional buffer
BufferedWriter out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(PATH), StandardCharsets.UTF_8));
out.append("Hello!\n");
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

// Methode 6: similar to method 4 (Java >= 7)
// Available methods: append() close() equals() flush() getClass() hashCode() newLine() notify() notifyAll() toString() wait() write()
BufferedWriter out = Files.newBufferedWriter(Paths.get(PATH), StandardCharsets.UTF_8);
// or BufferedWriter out = Files.newBufferedWriter(Paths.get(PATH));
// or BufferedWriter out = Files.newBufferedWriter(Paths.get(PATH), StandardCharsets.UTF_8, StandardOpenOption.WRITE);  // To erase PATH
// or BufferedWriter out = Files.newBufferedWriter(Paths.get(PATH), StandardCharsets.UTF_8, StandardOpenOption.APPEND); // To append in PATH
out.append("Hello!\n");
out.append("¡Buenos días!\n");
out.append("Bonjour!\n");
out.append("你好！\n");
out.close();

/exit
