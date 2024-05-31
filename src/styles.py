# -*- coding: utf-8 -*-
"""
"""


import tkinter as tk
from tkinter import ttk


class AppStyles:
    default_font = 'DejaVu Serif'
    default_size = 10

    def __init__(self) -> None:
        """
        """
        self.__style = ttk.Style()
        self.entrys()
        self.labels()
        self.entrys()

    def buttons(self) -> None:
        """
        Style to buttons.
        """
        self.__style.configure(
                'ButtonController.TButton',
                font=(AppStyles.default_font, AppStyles.default_size + 4),
                anchor=tk.CENTER,
                justify='center'
            )

        self.__style.configure(
                'Button.TButton',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER
            )
        self.__style.configure(
                'ButtonJoinMerge.TButton',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER
            )
        self.__style.configure(
                'IndexButtonPage.TButton',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER
            )

    def labels(self) -> None:
        """
        Styles to labels.
        """
        self.__style.configure(
                'LabelListPDF.TLabel',
                font=(AppStyles.default_font, AppStyles.default_size)
            )
        self.__style.configure(
                'LabelListbox.TLabel',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER,
                justify="center"
            )

    def entrys(self) -> None:
        """
        Style to entry.
        """
        self.__style.configure(
                'PDFOutput.TEntry',
                font=(AppStyles.default_font, AppStyles.default_size),
                padding=(5, 0, 5, 0),
                anchor=tk.CENTER,
            )
