package org.jdhp.snippets.sax;


public class Hello {

    public final static String PROGRAM_NAME = "hello_sax";

    /**
     *
     */
    public static void main(String args[]) {
        if(args.length != 1) {
            usage();
            System.exit(1);
        }

        String filename = args[0];
        XMLParser parser = new XMLParser(filename);
    }

    /**
     *
     */
    public static void usage() {
        System.out.println("Usage: " + PROGRAM_NAME + " file.xml");
    }
}
