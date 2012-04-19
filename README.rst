.. contents::

Introduction
============

This package provides a class to use wkhtmltopdf in python without any trouble (?)

USAGE
=====

    >>> from zope.interface import implements
    >>> from interfaces import IWkhtmltopdfConfig

    >>> class WkhtmltopdfConfig:
    ...     """Wkhtmltopdf Config utility
    ...     """
    ...     implements(IWkhtmltopdfConfig)
    ...      paths = {'linux2': '/absolute/path/to/linux/wkhtmltopdf',
    ...               'darwin': '/absolute/path/to/osx/wkhtmltopdf'}


    <utility
        provides="abstract.wkhtmltopdf.interfaces.IWkhtmltopdfConfig"
        factory=".WkhtmltopdfConfig"
      />


Zope/Plone integration
======================

    >>> from abstract.wkhtmltopdf import PDFRenderer
    >>> renderer = PDFRenderer()
    >>> document = self.form_instance.getContent()
    >>> self.request.response.setHeader('Content-Type', 'application/pdf')
    >>> self.request.response.setHeader(
    ...     'Content-Disposition',
    ...     'attachment; filename="%s.pdf"' % document.__name__)
    >>> return renderer(self.render())


Pyramid integration
===================


    >>> from pyramid.response import Response
    >>> from pyramid.renderers import get_renderer
    >>> from abstract.wkhtmltopdf import PDFRenderer

    >>> def print_page(context, request):
    ...
    ...     params = dict(
    ...         some_key='some value')
    ...
    ...     template = get_renderer('print.pt').implementation()
    ...     data = template.render(**params)
    ...
    ...     renderer = PDFRenderer()
    ...     response = Response(renderer(data))
    ...     response.content_type = 'application/pdf'
    ...     response.headers.add('Content-Disposition',
    ...         'attachment;filename=%s' % filename)
    ...
    ...     return response

