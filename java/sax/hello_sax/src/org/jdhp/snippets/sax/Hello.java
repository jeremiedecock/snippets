package org.jdhp.snippets.sax;

import java.io.File;
import java.io.IOException;

import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;

/**
 * 
 * @author Jeremie Decock
 */
public class Hello {

    public final static String PROGRAM_NAME = "hello_sax";

    /**
     * 
     * @param args
     */
    public static void main(String args[]) {
        
        // Check arguments
        if(args.length != 1) {
            usage();
            System.exit(1);
        }

        // Get file URL
        String filename = args[0];
        String fileUrl = convertToFileURL(filename);
        InputSource inpurSource = new InputSource(fileUrl);
        System.out.println("Parsing " + fileUrl);
        
        // Make the handler
        SaxHandlers handlers = new SaxHandlers();

        // Get informations about the current parser implementation
        //String parserClassName = System.getProperty("org.xml.sax.driver");
        //System.out.println("Parser implementation: " + parserClassName);
        
        // Make the parser and parse
        try {
            // Make the parser
            XMLReader xmlReader = XMLReaderFactory.createXMLReader();
            
            // Get informations about the current parser implementation
            System.out.println("Using parser " + xmlReader.getClass().getCanonicalName());
            
            // Parse
            xmlReader.setContentHandler(handlers);
            xmlReader.setErrorHandler(handlers);
            xmlReader.parse(inpurSource);  //xmlReader.parse(fileUrl);
        } catch(IOException ex) {
            //
        	ex.printStackTrace();
        } catch(SAXException ex) {
            //
        	ex.printStackTrace();
        }
    }
    
    /**
     * @param filename
     * @return
     */
    public static String convertToFileURL(String filename) {
        String path = new File(filename).getAbsolutePath();

        if(File.separatorChar != '/') {
            path = path.replace(File.separatorChar, '/');
        }

        if(!path.startsWith("/")) {
            path = "/" + path;
        }

        return "file:" + path;
    }

    /**
     *
     */
    public static void usage() {
        System.out.println("Usage: " + PROGRAM_NAME + " file.xml");
    }
}
