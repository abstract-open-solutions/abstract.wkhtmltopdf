import sys
import subprocess
import logging
from zope.component import queryUtility
from interfaces import IWkhtmltopdfConfig
# from App.config import getConfiguration


class PDFRenderer(object):

    def __init__(self):
        config = queryUtility(IWkhtmltopdfConfig)
        self.logger = logging.getLogger("whkthmltopdf")
        if not config:
            self.logger.error('IWkhtmltopdfConfig utility not found')
            raise Exception('Cazzzo!!!')

        self.executable = config().paths.get(sys.platform)
        if not self.executable:
            self.logger.error('Wkhtmltopdf executable not found')
            raise Exception('ri Cazzzo!!!')

    def __call__(self, data):
        if isinstance(data, unicode):
            data = data.encode("utf-8")
        args = (self.executable, "-q", "--encoding", "utf-8",
                "--print-media-type", "-", "-")
        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        log_str = "Calling %s" % " ".join(args)
        logging.debug(log_str)
        stdout, stderr = process.communicate(data)
        if process.returncode != 0:
            log_str = "wkhtmltopdf failed (%d): %s" % \
                                    (process.returncode, stderr)
            logging.error(log_str)
        return stdout
