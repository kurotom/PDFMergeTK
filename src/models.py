# -*- coding: utf-8 -*-
"""
"""

import fitz

import os

from typing import Union, List


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


class Data:
    # total_pages
    total_pages = 0
    # [ names_pdf ]
    names = []
    # [ PDFile_objs ]
    selected = []
    # [ fitz.fitz.Pixmap ]
    imagesTK = []
    # [ str ]
    images_loaded = []

    def get_images() -> List[fitz.fitz.Pixmap]:
        """
        """
        return Data.imagesTK

    def set_names(
        pdf_names: str
    ) -> None:
        """
        """
        if pdf_names not in Data.names:
            pdf_names = os.path.basename(pdf_names)
            Data.names.append(pdf_names)

    def add(
        pdfileObj: PDFile,
        avoid_duplicates: bool = True
    ) -> None:
        """
        """
        if avoid_duplicates:
            if Data.get_index(pdfileObj.name) == -1:
                Data.total_pages += pdfileObj.n_pages  # set total pages
                Data.selected.append(pdfileObj)  # add PDFile instance.
                Data.set_names(pdf_names=pdfileObj.name)
        else:
            Data.total_pages += pdfileObj.n_pages
            Data.selected.append(pdfileObj)
            Data.set_names(pdf_names=pdfileObj.name)

    def add_image(
        current_name: str,
        image: fitz.fitz.Pixmap
    ) -> None:
        """
        """
        # if current_name not in Data.images_loaded:
        Data.imagesTK.append(image)

    def set_loaded_images_pdfile(
        pdfileObj: PDFile
    ) -> None:
        """
        """
        Data.images_loaded.append(os.path.basename(pdfileObj.name))

    def collect_images() -> None:
        """
        """
        # Data.imagesTK.clear()
        for item in Data.selected:
            print('Data collect_images ', item)
            if item.name not in Data.images_loaded:
                Data.images_loaded.append(item.name)
                Data.imagesTK += item.images

    def delete(
        pdf_name: str
    ) -> int:
        """
        """
        idx = Data.get_index(pdf_name)
        if idx < 0:
            return idx
        else:
            for item in Data.selected:
                if item.name == pdf_name:
                    Data.selected.pop(idx)
                    Data.names.pop(Data.names.index(pdf_name))
                    Data.images_loaded.pop(
                                    Data.images_loaded.index(pdf_name)
                                )

                    Data.total_pages = sum(
                                        [
                                            i.n_pages
                                            for i in Data.selected
                                        ]
                                    )
                    break

            Data.collect_images()
            return idx

    def get_index(
        pdf_name: str
    ) -> int:
        """
        """
        idx = -1
        for i in range(len(Data.selected)):
            if pdf_name == Data.selected[i].name:
                idx = i
        return idx

    def find(
        name: str
    ) -> Union[PDFile, None]:
        """
        """
        indx = Data.get_index(pdf_name=name)
        if indx == -1:
            return None
        else:
            return Data.selected[Data.get_index(pdf_name=name)]

    def sort(
        listKey: list
    ) -> None:
        """
        """
        sorted_PDF_files = {
                name: index
                for index, name in enumerate(listKey)
            }

        Data.selected = sorted(
                                Data.selected,
                                key=lambda x: sorted_PDF_files[x.name]
                            )

        Data.names = [i.name for i in Data.selected]

        Data.collect_images()

    def close() -> None:
        """
        """
        for item in Data.selected:
            item.data.close()
        Data.names.clear()
        Data.selected.clear()
        Data.imagesTK.clear()
        Data.images_loaded.clear()

    @staticmethod
    def status() -> str:
        return '<[ Items: %s, Images: %s, Total Pages: %i ]>' % (
                            len(Data.selected),
                            len(Data.imagesTK),
                            Data.total_pages
                        )
