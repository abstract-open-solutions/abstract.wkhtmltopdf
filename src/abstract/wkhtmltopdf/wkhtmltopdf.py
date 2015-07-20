# -*- encoding: utf-8 -*-
import os
import sys
import subprocess
import logging

from zope.component import queryUtility

from interfaces import IWkhtmltopdfConfig

DEFAULT_EXE_PATHS = (
    '/usr/bin/wkhtmltopdf',
    '/usr/local/bin/wkhtmltopdf',
)


class ConfigurationError(Exception):
    """Whkthmltopdf configuration error
    """


class PDFRenderer(object):
    _process = None
    executable = ''

    def __init__(self):
        config = queryUtility(IWkhtmltopdfConfig)
        self.logger = logging.getLogger("whkthmltopdf")

        if config:
            self.executable = config.paths.get(self._platform)

        if not self.executable:
            self.executable = os.environ.get('WKHTML2PDF_PATH')

        if not self.executable:
            for path in DEFAULT_EXE_PATHS:
                if os.path.exists(path):
                    self.executable = path
                    msg = 'No config utility found, but found %s, using it!' \
                        % path
                    self.logger.info(msg)
                    break

        if not self.executable:
            error = (
                'Wkhtmltopdf executable not found'
                ' for this platform - %s' % self._platform)
            raise ConfigurationError(error)

    @property
    def _platform(self):
        return sys.platform

    @property
    def _args(self):
        return (self.executable, "-q", "--encoding", "utf-8",
                "--print-media-type", "-", "-")

    def _generate_pdf(self, data):
        self._process = subprocess.Popen(
            self._args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        log_str = "Calling %s" % " ".join(self._args)
        logging.debug(log_str)
        stdout, stderr = self._process.communicate(data)
        return stdout, stderr

    def __call__(self, data):
        if isinstance(data, unicode):
            data = data.encode("utf-8")

        stdout, stderr = self._generate_pdf(data)
        if self._process.returncode != 0:
            error = "wkhtmltopdf failed (%d): %s" % \
                                    (self._process.returncode, stderr)
            raise RuntimeError(error)
        return stdout
