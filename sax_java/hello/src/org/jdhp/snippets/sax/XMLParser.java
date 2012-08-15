package org.jdhp.snippets.sax;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.InputSource;
import org.xml.sax.Locator;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;

/**
 * @author Jeremie Decock
 * 
 * XMLParser is a copy of org.xml.sax.helpers.DefaultHandler helper.
 * 
 * XMLParser has been made to be used as a starting point for new handlers.
 * Users can copy it and drop useless methods.
 * 
 * DefaultHandler implements the four SAX handlers:
 * - org.xml.sax.EntityResolver
 * - org.xml.sax.DTDHandler
 * - org.xml.sax.ContentHandler
 * - org.xml.sax.ErrorHandler
 * 
 * The main methods are:
 * - void startDocument()
 * - void endDocument()
 * - void startElement(String namespaceURI, String localName, String qualifiedName, Attributes attributes)
 * - void endElement(String namespaceURI, String localName, String qualifiedName)
 * - void characters(char ch[], int start, int length)
 * - void warning(SAXParseException e)
 * - void error(SAXParseException e)
 * - void fatalError(SAXParseException e)
 */
public class XMLParser extends DefaultHandler
{

	/**
	 * 
	 * @param filename
	 */
    public XMLParser(String filename) {
        String fileUrl = convertToFileURL(filename);
        System.out.println("Parsing " + fileUrl);

        try {
            SAXParserFactory spf = SAXParserFactory.newInstance();
            spf.setNamespaceAware(true);
            SAXParser saxParser = spf.newSAXParser();

            XMLReader xmlReader = saxParser.getXMLReader();
            xmlReader.setContentHandler(this);
            xmlReader.parse(fileUrl);
        } catch(ParserConfigurationException ex) {
            //
        } catch(IOException ex) {
            //
        } catch(SAXException ex) {
            //
        }
    }

    
    /**
     * @param filename
     * @return
     */
    private static String convertToFileURL(String filename) {
        String path = new File(filename).getAbsolutePath();

        if(File.separatorChar != '/') {
            path = path.replace(File.separatorChar, '/');
        }

        if(!path.startsWith("/")) {
            path = "/" + path;
        }

        return "file:" + path;
    }


    // EntityResolver interface ////////////////////////////////////////


    /**
     * Resolve an external entity.
     *
     * <p>Always return null, so that the parser will use the system
     * identifier provided in the XML document.  This method implements
     * the SAX default behaviour: application writers can override it
     * in a subclass to do special translations such as catalog lookups
     * or URI redirection.</p>
     *
     * @param publicId The public identifier, or null if none is
     *                 available.
     * @param systemId The system identifier provided in the XML
     *                 document.
     * @return The new input source, or null to require the
     *         default behaviour.
     * @exception java.io.IOException If there is an error setting
     *            up the new input source.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.EntityResolver#resolveEntity
     */
    public InputSource resolveEntity(String publicId, String systemId)
        throws IOException, SAXException
    {
        return null;
    }


    // DTDHandler interface ////////////////////////////////////////////


    /**
     * Receive notification of a notation declaration.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass if they wish to keep track of the notations
     * declared in a document.</p>
     *
     * @param name The notation name.
     * @param publicId The notation public identifier, or null if not
     *                 available.
     * @param systemId The notation system identifier.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.DTDHandler#notationDecl
     */
    public void notationDecl(String name, String publicId, String systemId)
        throws SAXException
    {
        // no op
    }


    /**
     * Receive notification of an unparsed entity declaration.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to keep track of the unparsed entities
     * declared in a document.</p>
     *
     * @param name The entity name.
     * @param publicId The entity public identifier, or null if not
     *                 available.
     * @param systemId The entity system identifier.
     * @param notationName The name of the associated notation.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.DTDHandler#unparsedEntityDecl
     */
    public void unparsedEntityDecl(String name, String publicId,
                                    String systemId, String notationName)
        throws SAXException
    {
        // no op
    }


    // ContentHandler interface ////////////////////////////////////////


    /**
     * Receive a Locator object for document events.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass if they wish to store the locator for use
     * with other document events.</p>
     *
     * @param locator A locator for all SAX document events.
     * @see org.xml.sax.ContentHandler#setDocumentLocator
     * @see org.xml.sax.Locator
     */
    public void setDocumentLocator(Locator locator)
    {
        // no op
    }


    /**
     * Receive notification of the beginning of the document.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions at the beginning
     * of a document (such as allocating the root node of a tree or
     * creating an output file).</p>
     *
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#startDocument
     */
    public void startDocument()
        throws SAXException
    {
    	System.out.println("start document");
    }


    /**
     * Receive notification of the end of the document.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions at the end
     * of a document (such as finalising a tree or closing an output
     * file).</p>
     *
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#endDocument
     */
    public void endDocument()
        throws SAXException
    {
    	System.out.println("end document");
    }


    /**
     * Receive notification of the start of a Namespace mapping.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions at the start of
     * each Namespace prefix scope (such as storing the prefix mapping).</p>
     *
     * @param prefix The Namespace prefix being declared.
     * @param namespaceURI The Namespace URI mapped to the prefix.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#startPrefixMapping
     */
    public void startPrefixMapping(String prefix, String namespaceURI)
        throws SAXException
    {
        // no op
    }


    /**
     * Receive notification of the end of a Namespace mapping.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions at the end of
     * each prefix mapping.</p>
     *
     * @param prefix The Namespace prefix being declared.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#endPrefixMapping
     */
    public void endPrefixMapping(String prefix)
        throws SAXException
    {
        // no op
    }


    /**
     * Receive notification of the start of an element.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions at the start of
     * each element (such as allocating a new tree node or writing
     * output to a file).</p>
     *
     * @param namespaceURI The Namespace URI, or the empty string if the
     *        element has no Namespace URI or if Namespace
     *        processing is not being performed.
     * @param localName The local name (without prefix), or the
     *        empty string if Namespace processing is not being
     *        performed.
     * @param qualifiedName The qualified name (with prefix), or the
     *        empty string if qualified names are not available.
     * @param attributes The attributes attached to the element.  If
     *        there are no attributes, it shall be an empty
     *        Attributes object.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#startElement
     */
    public void startElement(String namespaceURI, String localName, String qualifiedName, Attributes attributes)
        throws SAXException
    {
        if(namespaceURI.equals("")) {
        	System.out.println("start element: " + qualifiedName);
        	
        	/* 
        	 * In this snippet, attributes name are unknown so a "for loop" is used to iterate on all attributes.
        	 * In a real program, attributes name are known so "attributes.getValue("...")" can be used directly.
        	 */
        	for(int i=0 ; i<attributes.getLength() ; i++) {
        		String attributeName = attributes.getLocalName(i);
        		
        		/*
        		 *  "attributes.getValue(int index);" could be used too.
        		 */
        		System.out.println("attribute \"" + attributeName + "\" = " + attributes.getValue(attributeName));
        	}
        } else {
        	System.out.println("start element: {" + namespaceURI + "}" + localName);
        	
        	/* 
        	 * In this snippet, attributes name are unknown so a "for loop" is used to iterate on all attributes.
        	 * In a real program, attributes name are known so "attributes.getValue("...")" can be used directly.
        	 */
        	for(int i=0 ; i<attributes.getLength() ; i++) {
        		String attributeName = attributes.getLocalName(i);

        		/*
        		 *  "attributes.getValue(int index);" could be used too.
        		 */
        		System.out.println("attribute \"" + attributeName + "\" = " + attributes.getValue(attributeName));
        	}
        }
    }


    /**
     * Receive notification of the end of an element.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions at the end of
     * each element (such as finalising a tree node or writing
     * output to a file).</p>
     *
     * @param namespaceURI The Namespace URI, or the empty string if the
     *        element has no Namespace URI or if Namespace
     *        processing is not being performed.
     * @param localName The local name (without prefix), or the
     *        empty string if Namespace processing is not being
     *        performed.
     * @param qualifiedName The qualified name (with prefix), or the
     *        empty string if qualified names are not available.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#endElement
     */
    public void endElement(String namespaceURI, String localName, String qualifiedName)
        throws SAXException
    {
        if(namespaceURI.equals("")) {
        	System.out.println("end element: " + qualifiedName);
        } else {
        	System.out.println("end element: {" + namespaceURI + "}" + localName);
        }
    }


    /**
     * Receive notification of character data inside an element.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method to take specific actions for each chunk of character data
     * (such as adding the data to a node or buffer, or printing it to
     * a file).</p>
     *
     * @param ch The characters.
     * @param start The start position in the character array.
     * @param length The number of characters to use from the
     *               character array.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#characters
     */
    public void characters(char ch[], int start, int length)
        throws SAXException
    {
    	StringBuffer str = new StringBuffer();
    	
        for(int i=start ; i<start+length ; i++) {
        	switch(ch[i]) {
        	case '\\':
        		str.append("\\\\");
        		break;
        	case '"':
        		str.append("\\\"");
        		break;
        	case '\n':
        		str.append("\\n");
        		break;
        	case '\r':
        		str.append("\\r");
        		break;
        	case '\t':
        		str.append("\\t");
        		break;
        	default:
        		str.append(ch[i]);
        		break;
        	}
        }
       
        System.out.println("characters: " + str);
    }


    /**
     * Receive notification of ignorable whitespace in element content.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method to take specific actions for each chunk of ignorable
     * whitespace (such as adding data to a node or buffer, or printing
     * it to a file).</p>
     *
     * @param ch The whitespace characters.
     * @param start The start position in the character array.
     * @param length The number of characters to use from the
     *               character array.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#ignorableWhitespace
     */
    public void ignorableWhitespace(char ch[], int start, int length)
        throws SAXException
    {
        // no op
    }


    /**
     * Receive notification of a processing instruction.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions for each
     * processing instruction, such as setting status variables or
     * invoking other methods.</p>
     *
     * @param target The processing instruction target.
     * @param data The processing instruction data, or null if
     *             none is supplied.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#processingInstruction
     */
    public void processingInstruction(String target, String data)
        throws SAXException
    {
        // no op
    }


    /**
     * Receive notification of a skipped entity.
     *
     * <p>By default, do nothing.  Application writers may override this
     * method in a subclass to take specific actions for each
     * processing instruction, such as setting status variables or
     * invoking other methods.</p>
     *
     * @param name The name of the skipped entity.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ContentHandler#processingInstruction
     */
    public void skippedEntity(String name)
        throws SAXException
    {
        // no op
    }


    // ErrorHandler interface //////////////////////////////////////////


    /**
     * Receive notification of a parser warning.
     *
     * <p>The default implementation does nothing.  Application writers
     * may override this method in a subclass to take specific actions
     * for each warning, such as inserting the message in a log file or
     * printing it to the console.</p>
     *
     * @param e The warning information encoded as an exception.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ErrorHandler#warning
     * @see org.xml.sax.SAXParseException
     */
    public void warning(SAXParseException e)
        throws SAXException
    {
    	System.out.println("warning: " + e.getMessage());
    }


    /**
     * Receive notification of a recoverable parser error.
     *
     * <p>The default implementation does nothing.  Application writers
     * may override this method in a subclass to take specific actions
     * for each error, such as inserting the message in a log file or
     * printing it to the console.</p>
     *
     * @param e The error information encoded as an exception.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ErrorHandler#warning
     * @see org.xml.sax.SAXParseException
     */
    public void error(SAXParseException e)
        throws SAXException
    {
    	System.out.println("error: " + e.getMessage());
    }


    /**
     * Report a fatal XML parsing error.
     *
     * <p>The default implementation throws a SAXParseException.
     * Application writers may override this method in a subclass if
     * they need to take specific actions for each fatal error (such as
     * collecting all of the errors into a single report): in any case,
     * the application must stop all regular processing when this
     * method is invoked, since the document is no longer reliable, and
     * the parser may no longer report parsing events.</p>
     *
     * @param e The error information encoded as an exception.
     * @exception org.xml.sax.SAXException Any SAX exception, possibly
     *            wrapping another exception.
     * @see org.xml.sax.ErrorHandler#fatalError
     * @see org.xml.sax.SAXParseException
     */
    public void fatalError(SAXParseException e)
        throws SAXException
    {
    	System.out.println("fatalError: " + e.getMessage());
        throw e;
    }

}

