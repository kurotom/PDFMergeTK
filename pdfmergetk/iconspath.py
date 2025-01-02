# -*- coding: utf-8 -*-
"""
Icons for gui
"""

from pdfmergetk.pathclass import PathClass

base = PathClass.dirname(PathClass.realpath(__file__))


iconUP = PathClass.realpath(
        PathClass.join(base, *"/icons/up.png".split("/"))
    )

iconDOWN = PathClass.realpath(
        PathClass.join(base, *"/icons/down.png".split("/"))
    )

iconNEXT = PathClass.realpath(
        PathClass.join(base, *"/icons/right.png".split("/"))
    )

iconPREV = PathClass.realpath(
        PathClass.join(base, *"/icons/left.png".split("/"))
    )

iconTRASH = PathClass.realpath(
        PathClass.join(base, *"/icons/trash.png".split("/"))
    )
