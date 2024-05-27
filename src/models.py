# -*- coding: utf-8 -*-
"""
"""

import fitz


class PDFile:
    def __init__(
        self,
        name: str,
        data: fitz.fitz.Document,
        images: fitz.fitz.Pixmap,
        n_pages: int
    ) -> None:
        """
        """
        self.name = name
        self.data = data
        self.images = images
        self.n_pages = n_pages

    def __repr__(self) -> str:
        """
        """
        return '<[ Name: %s, Pages: %i ]>' % (self.name, self.n_pages)
