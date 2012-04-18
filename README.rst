.. contents::

Introduction
============

This package provides a class to use wkhtmltopdf in python without any trouble (?)

USAGE
=====
        >>> ... register utility ...

        >>> from abstract.wkhtmltopdf import PDFRenderer
        >>> renderer = PDFRenderer()
        >>> document = self.form_instance.getContent()
        >>> self.request.response.setHeader('Content-Type', 'application/pdf')
        >>> self.request.response.setHeader(
        ...     'Content-Disposition',
        ...     'attachment; filename="%s.pdf"' % document.__name__)
        >>> return renderer(self.render())


Zope/Plone integration
======================
 ...

Pyramid integration
===================
 ...
