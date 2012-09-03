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

    def startElementNS(self, name, qname, attr):
        """TODO: improve this"""
        print "Start NS element:", name, qname,
        for key, value in attr.items():
            print "[", key, "=", value, "]",
        print

    def endElementNS(self, name, qname):
        """TODO: improve this"""
        print "End NS element:", name, qname

    def characters(self, ch):
        print "Characters:", ch

    # ErrorHandler ##############################

    def fatalError(self, exception):
        print "Fatal error:", exception

    def error(self, exception):
        print "Error:", exception

    def warning(self, exception):
        print "Warning:", exception

