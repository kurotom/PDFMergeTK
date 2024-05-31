# -*- coding: utf-8 -*-
"""
AppStyles : in charge of styles of app.
"""

import tkinter as tk
from tkinter import ttk


class AppStyles:
    """
    In charge of all style of elements of application.
    """
    default_font = 'DejaVu Serif'
    default_size = 10

    def __init__(self) -> None:
        """
        Constructor
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
                font=(AppStyles.default_font, AppStyles.default_size + 5),
                anchor=tk.CENTER,
                justify='center'
            )

        self.__style.configure(
                'Button.TButton',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER,
                justify='center'
            )
        self.__style.configure(
            'ButtonJoinMerge.TButton',
            font=(AppStyles.default_font, AppStyles.default_size + 1, 'bold'),
            anchor=tk.CENTER,
            justify='center'
        )
        self.__style.configure(
                'IndexButtonPage.TButton',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER,
                justify='center'
            )

    def labels(self) -> None:
        """
        Styles to labels.
        """
        self.__style.configure(
                'LabelListPDF.TLabel',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER,
                justify='center'
            )
        self.__style.configure(
                'LabelListbox.TLabel',
                font=(AppStyles.default_font, AppStyles.default_size, 'bold'),
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
