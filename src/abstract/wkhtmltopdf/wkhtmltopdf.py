# -*- encoding: utf-8 -*-
import sys
import subprocess
import logging
from zope.component import getUtility
from interfaces import IWkhtmltopdfConfig


class ConfigurationError(Exception):
    """Whkthmltopdf configuration error
    """


class PDFRenderer(object):

    def __init__(self):
        config = getUtility(IWkhtmltopdfConfig)
        self.logger = logging.getLogger("whkthmltopdf")

        self.executable = config.paths.get(sys.platform)
        if not self.executable:
            error = 'Wkhtmltopdf executable not found for this platform'
            raise ConfigurationError(error)

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
            error = "wkhtmltopdf failed (%d): %s" % \
                                    (process.returncode, stderr)
            raise RuntimeError(error)
        return stdout
