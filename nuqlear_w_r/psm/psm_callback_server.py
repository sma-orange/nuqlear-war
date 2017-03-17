"""Class to handle PSM Callbacks.
Just does some basic logging of Callback XML.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import xml.etree.ElementTree as eT

PSM_CALLBACK_URL = ''
PSM_CALLBACK_PORT = 80

logger = logging.getLogger(__name__)


class CallbackHandler(HTTPServer, BaseHTTPRequestHandler):
    """Class to handle PSM Callbacks.
    Just does some basic logging of Callback XML
    """
    def do_get(self, s):
        """refer to do_post"""
        self.do_post(s)

    def do_post(self, s):
        """parse the request"""
        logger.info('URL request: {}'.format(s.request))
        self.parse_xml(s)

    @staticmethod
    def parse_xml(s):
        """parse and log the xml request"""
        logger.info('Parsing Request')

        tree = eT.parse(s)
        doc = tree.getRoot()

        req_type = doc.find('request-name').text
        logger.info('REQUEST:', req_type)
        if req_type == 'UnitaryRequestDeliveryNotificationRequest':
            # this is the one to handle
            uid = doc.find('unitary-request-id').text
            msisdn = doc.find('msisdn').text
            status = doc.find('delivery-status').text.upper()
            mt = doc.find('total-mt').text
            if status == 'SUCCEEDED':
                logger.info('OK', status, uid, msisdn)
                logger.info('SEND OK Response...')
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write("<response>")
                s.wfile.write("<response-name>UnitaryRequestQualificationNotificationResponse</response-name>")
                s.wfile.write("<params>")
                s.wfile.write("<request-status>OK</request-status>")
                s.wfile.write("</params>")
                s.wfile.write("</response>")
                logger.info('Response Sent')
            elif status == 'FAILED':
                logger.info('KO', status, uid, msisdn, mt)
                details = doc.find('error-details')
                error_code = doc.find('error-code')
                error_type = doc.find('error-code-type')
                logger.info('DETAIL: ', error_type, error_code, details)
                logger.info('SEND KO Response')
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write("<response>")
                s.wfile.write("<response-name>UnitaryRequestQualificationNotificationResponse</response-name>")
                s.wfile.write("<params>")
                s.wfile.write("<request-status>KO</request-status>")
                s.wfile.write("</params>")
                s.wfile.write("</response>")
                logger.info('Response Sent')
            else:
                logger.info('Unsupported Error')
                logger.error(s)
        else:
            logger.info("Only Unitary Is Currently Supported")
            logger.error(s)


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((PSM_CALLBACK_URL, PSM_CALLBACK_PORT), CallbackHandler)
    logger.info('PSM Callback Server Start... ', PSM_CALLBACK_URL, PSM_CALLBACK_PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info('PSM Callback Server Stop.', PSM_CALLBACK_URL, PSM_CALLBACK_PORT)
