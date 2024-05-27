# -*- coding: utf-8 -*-
"""
"""

import fitz

from typing import List


class PDFile:
    def __init__(
        self,
        name: str,
        data: fitz.fitz.Document,
        images: List[fitz.fitz.Pixmap] = []
    ) -> None:
        """
        """
        self.name = name
        self.data = data
        self.images = images
        self.n_pages = len(self.data)

    def __repr__(self) -> str:
        """
        """
        return '<[ Name: %s, Pages: %i ]>' % (self.name, self.n_pages)
