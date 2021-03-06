.. contents::

Introduction
============

This package provides a class to use wkhtmltopdf in python without any trouble (?)



Configuration
=============

    >>> from zope.interface import implements
    >>> from interfaces import IWkhtmltopdfConfig

    >>> class WkhtmltopdfConfig:
    ...     """Wkhtmltopdf Config utility
    ...     """
    ...     implements(IWkhtmltopdfConfig)
    ...      paths = {'linux2': '/absolute/path/to/linux/wkhtmltopdf',
    ...               'darwin': '/absolute/path/to/osx/wkhtmltopdf'}


zcml example registration::

    <utility
        provides="abstract.wkhtmltopdf.interfaces.IWkhtmltopdfConfig"
        factory=".WkhtmltopdfConfig"
      />

You can also use an environment variable to get this conf, by passing it at runtime::

    WKHTML2PDF_PATH=/usr/bin/wkhtmltopdf bin/instance fg

or by buildout setup::

    [...]

    [instance]
    environment-vars =
        WKHTML2PDF_PATH /usr/bin/wkhtmltopdf

    [...]


Default: if none of the above setting is found and one of the default paths is found

    `/usr/bin/wkhtmltopdf`
    `/usr/local/bin/wkhtmltopdf`

it will be used as a default (and this info will be logged).


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


Install kwhtmltopdf with zc.buildout
====================================

Dependencies
-------------

linux:

    * xfonts-scalable
    * libfontconfig1


buildout example configuration ::

    [buildout]
    ...
    parts =
        ...
        wkhtmltopdf-linux
        wkhtmltopdf-osx

    ...

    [instance]
    environment-vars +=
        WKHTML2PDF_PATH ${buildout:directory}/parts/${wkhtmltopdf:executable-path}/${wkhtmltopdf:filename}

    ...

    [wkhtmltopdf-linux]
    recipe = hexagonit.recipe.download
    url = http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.10.0_rc2-static-i386.tar.bz2
    download-only = true
    filename = wkhtmltopdf
    executable-path = ${:_buildout_section_name_}


    [wkhtmltopdf-osx]
    recipe = hexagonit.recipe.download
    url = http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-OSX-0.10.0_rc2-static.tar.bz2

