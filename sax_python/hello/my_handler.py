from xml.sax.handler import ContentHandler, ErrorHandler

class MyHandler(ContentHandler, ErrorHandler):
    """A content handler"""

    # ContentHandler ############################

    def startDocument(self):
        print "Start document"

    def endDocument(self):
        print "End document"

    def startElement(self, name, attr):
        print "Start element:", name,

        for key, value in attr.items():
            print "[", key, "=", value, "]",
        print 

    def endElement(self, name):
        print "End element:", name

    def characters(self, ch):
        print "Characters element:", ch

    # ErrorHandler ##############################

    def fatalError(self, exception):
        print "Fatal error:", exception

    def error(self, exception):
        print "Error:", exception

    def warning(self, exception):
        print "Warning:", exception

