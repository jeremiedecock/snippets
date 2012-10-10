package org.jdhp.snippets.commons;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.GnuParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;

public class HelloCommonsCli {

    public final static String VERSION = "1.0";

    public final static String PROGRAM_NAME = "Hello_commons_cli";

    public final static String COMMAND = "hello_commons_cli";

    public static void main(String args[]) {

        // PARSE OPTIONS USING CLI (APACHE) ///////////////////////////////////
        
        Option opt_help = new Option("help", "display this help and exit");
        Option opt_version = new Option("version", "output version information and exit");
        
        Options options = new Options();
        options.addOption(opt_help);
        options.addOption(opt_version);
        
//      options.addOption("h", "help", false, "display this help and exit");
//      options.addOption("v", "verbose", false, "output version information and exit");
        
        HelpFormatter formatter = new HelpFormatter();
        
        CommandLineParser parser = new GnuParser();
        
        CommandLine cmd;
        try {
            cmd = parser.parse(options, args);
            
            if(cmd.hasOption("help")) {
                System.out.println(
                        PROGRAM_NAME + " snippet.\n\n" +
                        "Usage: " + COMMAND + " [OPTION]\n\n" +
                        "Options:\n" +
                        "    -v, --version\n" +
                        "        output version information and exit\n\n" +
                        "    -h, --help\n" +
                        "        display this help and exit\n\n" +
                        "Report bugs to <jd.jdhp@gmail.com>."
                );
                //System.exit(0);
            }
            
            if(cmd.hasOption("version")) {
                System.out.println(
                    PROGRAM_NAME + " " + VERSION + "\n\n" +
                    "Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)\n" +
                    "This is free software; see the source for copying conditions.\n" +
                    "There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
                );
                //System.exit(0);
            }
        } catch (ParseException e1) {
            System.err.println("Parsing (options) failed. Reason: " + e1.getMessage());
            formatter.printHelp(COMMAND, options);
            System.exit(1);
        }
    }
}
