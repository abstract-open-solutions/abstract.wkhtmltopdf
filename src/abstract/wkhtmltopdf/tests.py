# -*- encoding: utf-8 -*-
# pylint: disable=W0212
import sys
import unittest2 as unittest
from mock import Mock
from zope.interface import implements

from zope.component import getGlobalSiteManager
from zope.component import getUtility

from interfaces import IWkhtmltopdfConfig
from wkhtmltopdf import PDFRenderer
from wkhtmltopdf import ConfigurationError


_PATHS = {'linux2': '/absolute/path/to/linux/wkhtmltopdf',
          'darwin': '/absolute/path/to/osx/wkhtmltopdf'}


class WkhtmltopdfConfig:
    """Dummy WkhtmltopdfConfig utility
    """
    implements(IWkhtmltopdfConfig)
    paths = _PATHS


class WkhtmltopdfTestCase(unittest.TestCase):

    def setUp(self):
        self.component_registry = getGlobalSiteManager()

    def _registerUtility(self):
        self.component_registry.registerUtility(factory=WkhtmltopdfConfig)

    def _unregisterUtility(self):
        utility = getUtility(IWkhtmltopdfConfig)
        self.component_registry.unregisterUtility(utility)

    def test_config(self):
        """Testing PDFRenderer configuration
        """

        self._registerUtility()
        renderer = PDFRenderer()
        self.assertEqual(renderer.executable, _PATHS[sys.platform])

        # When we call PDFRenderer in a not configured platform
        # it raises a ConfigurationError
        _original = PDFRenderer._platform
        PDFRenderer._platform = 'no-existent-platform'
        self.assertRaises(ConfigurationError, PDFRenderer)
        PDFRenderer._platform = _original

        self._unregisterUtility()

    def test_args(self):
        self._registerUtility()
        renderer = PDFRenderer()

        args = (
            _PATHS[sys.platform],
            '-q',
            '--encoding',
            'utf-8',
            '--print-media-type',
            '-',
            '-',
        )

        self.assertEqual(renderer._args, args)
        self._unregisterUtility()

    def test_runtimerror_on_call(self):
        """When wkhtmltopdf fails PDFRenderer raises a RuntimeError
        """
        self._registerUtility()
        renderer = PDFRenderer()
        orig = renderer._generate_pdf
        renderer._generate_pdf = Mock()
        renderer._generate_pdf.return_value = 'stdout', 'stderr'

        renderer._process = Mock()
        renderer._process.returncode = 1

        self.assertRaises(RuntimeError, renderer, '<html>')

        renderer._generate_pdf = orig
        self._unregisterUtility()


if __name__ == '__main__':
    unittest.main()
