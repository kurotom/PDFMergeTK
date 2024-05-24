# -*- coding: utf-8 -*-
"""
"""
import tkinter as tk
from tkinter import ttk, Tk

from tkinter import filedialog
# from tkinter import messagebox

import fitz

import os
import sys
import subprocess

from PIL import Image, ImageTk

from typing import Union, Tuple

from src.langs import languagesDict


class ElementsTK:
    items = []
    menuItems = []


class LanguagesClass:
    lang = 'en'
    language = languagesDict[lang]


class PDFiles:
    selected = {}


class MainGUI:
    """
    """

    def __init__(
        self,
        rootGUI: Tk,
        lang: str = 'en'
    ) -> None:
        """
        """
        LanguagesClass.lang = lang

        self.__width_frame_usercontrol = 300
        self.__height_frame_usercontrol = 1

        self.output_filename_pdf_entry = tk.StringVar()

        self.show_save_as = True
        self.adding_files = False
        self.rootGUI = rootGUI

        self.userlistbox = None

        self.frameUserControl = ttk.Frame(self.rootGUI)

        self.displaycanvas = DisplayCanvas(
                                mainTk=self.rootGUI,
                                height_canvas=500,
                                width_canvas=300
                            )

        self.menu()
        self.userInterface()
        self.displaycanvas.show()

        self.frameUserControl.place(
                x=10,
                y=10,
                relheight=1,
                width=self.__width_frame_usercontrol
            )

        self.rootGUI.title("PDF Merger")
        self.rootGUI.geometry("600x510")
        self.rootGUI.resizable(False, False)

    def menu(self) -> None:
        """
        """
        menubar = tk.Menu(self.rootGUI)
        self.rootGUI.config(menu=menubar)

        quit_ = tk.Menu(menubar, tearoff=0)
        quit_.add_command(
                    label=LanguagesClass.language['quit'],
                    command=self.rootGUI.destroy
                )

        langs_ = tk.Menu(menubar, tearoff=0)
        langs_.add_command(
                    label=LanguagesClass.language['en'],
                    command=lambda: self.change_language('en')
                )
        langs_.add_command(
                    label=LanguagesClass.language['es'],
                    command=lambda: self.change_language('es')
                )

        menubar.add_cascade(
                    label=LanguagesClass.language['file'],
                    menu=quit_
                )
        menubar.add_cascade(
                    label=LanguagesClass.language['langMenu'],
                    menu=langs_
                )

        # item , {index: label}
        ElementsTK.menuItems.append([quit_, {0: 'quit'}])
        ElementsTK.menuItems.append([langs_, {0: 'en', 1: 'es'}])
        ElementsTK.menuItems.append([menubar, {1: 'file', 2: 'langMenu'}])

    def change_language(self, lang) -> None:
        """
        """
        if lang == 'en':
            LanguagesClass.lang = 'en'
        if lang == 'es':
            LanguagesClass.lang = 'es'

        LanguagesClass.language = languagesDict[LanguagesClass.lang]

        for menuItem in ElementsTK.menuItems:
            item, indexLabel = menuItem
            for k, label in indexLabel.items():
                try:
                    # print(k, label, item.entrycget(k, 'label'))
                    item.entryconfigure(
                                k,
                                label=LanguagesClass.language[label]
                            )
                except BaseException:
                    pass

        for item_dict in ElementsTK.items:
            for k, itemTK in item_dict.items():
                # print(k, itemTK, itemTK['text'], LanguagesClass.language[k])
                itemTK['text'] = LanguagesClass.language[k]
                if k == 'open' and self.adding_files:
                    itemTK['text'] = LanguagesClass.language['add']

    def userInterface(
        self
    ) -> None:
        """
        """
        self.open_files = ttk.Button(
                                self.frameUserControl,
                                text=LanguagesClass.language['open'],
                                command=self.select_pdf
                            )

        self.open_files.place(
                x=(self.__width_frame_usercontrol / 2) - 62,
                y=0,
                height=30,
                width=100
            )

        ElementsTK.items.append({'open': self.open_files})

    def select_pdf(self) -> None:
        """
        """
        filesPDF = filedialog.askopenfiles(
                    filetypes=[(LanguagesClass.language['files'], "*.pdf")],
                    title=LanguagesClass.language['select']
                )

        if filesPDF == '':
            pass
        else:
            if len(filesPDF) > 0:

                self.save_as()

                self.show_save_as = False

                if isinstance(filesPDF, list) is False:
                    filesPDF = [filesPDF]

                if self.adding_files:
                    self.displaycanvas.reset_images()

                self.displaycanvas.clear_canvas()

                for item in filesPDF:

                    name_, ext_ = os.path.splitext(
                                            os.path.basename(str(filesPDF[0]))
                                        )
                    self.output_filename_pdf_entry.set(name_)

                    if item not in PDFiles.selected:
                        data = self.read_pdf(filename=item)
                        PDFiles.selected[item.name] = data

                self.add_files()
                self.displaycanvas.to_canvas()

                convert_button = ttk.Button(
                                        self.frameUserControl,
                                        text=LanguagesClass.language['join'],
                                        command=self.start_merge_pdf
                                    )
                convert_button.place(
                            x=(self.__width_frame_usercontrol / 2) - 62,
                            y=460,
                            height=30,
                            width=100
                        )

                self.listbox_pdf()

                ElementsTK.items.append({'join': convert_button})

    def add_files(self) -> None:
        """
        """
        self.open_files['text'] = LanguagesClass.language['add']
        self.open_files['command'] = self.select_pdf
        self.adding_files = True

    def save_as(self) -> None:
        """
        """
        if self.show_save_as:
            filename_label = ttk.Label(
                                    self.frameUserControl,
                                    text=LanguagesClass.language['name']
                                )
            filename_entry = ttk.Entry(
                                    self.frameUserControl,
                                    textvariable=self.output_filename_pdf_entry
                                )

            filename_label.place(
                    x=0,
                    y=420,
                    height=30,
                    width=70
                )
            filename_entry.place(
                    x=75,
                    y=420,
                    height=30,
                    width=self.__width_frame_usercontrol - (105)
                )

            ElementsTK.items.append({'name': filename_label})

    def start_merge_pdf(self) -> None:
        """
        """
        filename_output = self.output_filename_pdf_entry.get()
        filename_output = filename_output.replace('.pdf', '')
        filename_output = '%s.pdf' % (filename_output)

        sorted_files_pdf = self.userlistbox.get_listbox()

        first_pdf = sorted_files_pdf[0]
        first_pdf_data = self.read_pdf(filename=first_pdf)

        file_save_path = '%s%s%s' % (
                            os.path.expanduser('~'),
                            os.path.sep,
                            filename_output
                        )

        file_save_path_data = self.read_pdf()

        for file_pdf in sorted_files_pdf[1:]:
            file_pdf_data = self.read_pdf(filename=file_pdf)
            first_pdf_data.insert_pdf(file_pdf_data)

        file_save_path_data.insert_pdf(first_pdf_data)

        file_save_path_data.save(file_save_path)

        self.show_directory_file_merged(file_path=file_save_path)

    def show_directory_file_merged(
        self,
        file_path: str
    ) -> None:
        """
        """
        current_plat = sys.platform.lower()

        if current_plat == 'linux':
            subprocess.run(['xdg-open', file_path])
        elif current_plat == 'darwin':
            subprocess.run(['open', file_path])
        elif current_plat == 'win32':
            os.startfile(file_path)
        else:
            pass

    def listbox_pdf(self) -> None:
        """
        """
        self.userlistbox = UserListBox(
                            frame=self.frameUserControl,
                            width=self.__width_frame_usercontrol,
                            entry_filename=self.output_filename_pdf_entry,
                            displaycanvas=self.displaycanvas
                        )

    def read_pdf(
        self,
        filename: str = None
    ) -> fitz.fitz.Document:
        """
        """
        if filename is None:
            return fitz.open()
        else:
            return fitz.open(filename, filetype='pdf')

    def to_image(self) -> None:
        """
        """
        pass


class UserListBox(MainGUI):
    def __init__(
        self,
        frame: tk.Frame,
        width: int,
        entry_filename: tk.StringVar,
        displaycanvas: tk.Canvas
    ) -> None:
        """
        """
        self.index = 0
        self.width = width

        self.displaycanvas = displaycanvas
        self.total_index = len(PDFiles.selected)
        self.entry_filename = entry_filename

        self.list_pdfs = list(PDFiles.selected.keys())

#
        pdfs_basename = [
                            os.path.basename(i)
                            for i in self.list_pdfs
                        ]

        self.path_pdf_files_dict = dict(zip(pdfs_basename, self.list_pdfs))

        self.frame = frame

        self.label_listbox = ttk.Label(
                                self.frame,
                                text=LanguagesClass.language['list'],
                                justify="center",
                                anchor=tk.CENTER
                            )

        self.choices = tk.StringVar()
        self.listbox_files = tk.Listbox(
                    self.frame,
                    listvariable=self.choices
                )
        # print('--> ', self.path_pdf_files_dict)

        self.choices.set(pdfs_basename)

        horizontalScroll = ttk.Scrollbar(
                                self.frame,
                                orient=tk.HORIZONTAL,
                                command=self.listbox_files.xview
                            )
        verticalScroll = ttk.Scrollbar(
                                self.frame,
                                orient=tk.VERTICAL,
                                command=self.listbox_files.yview
                            )

        self.listbox_files.configure(
                xscrollcommand=horizontalScroll.set,
                yscrollcommand=verticalScroll.set
            )

#
        up_button = ttk.Button(
                    self.frame,
                    text=u'\u21E7',
                    command=self.up_file_list
                )
        down_button = ttk.Button(
                    self.frame,
                    text=u'\u21E9',
                    command=self.down_file_list
                )

        self.label_listbox.place(
                x=0,
                y=40,
                height=30,
                width=self.width - (30)
            )

# ListBox Place
        self.listbox_files.place(
                x=0,
                y=70,
                height=300,
                width=self.width - (45)
            )
        horizontalScroll.place(
                x=0,
                y=365,
                height=15,
                width=self.width - (45)
            )
        verticalScroll.place(
                x=self.width - (45),
                y=70,
                height=295,
                width=15
            )
#

        up_button.place(
                x=(self.width / 2) - 75,
                y=380,
                width=50,
                height=30
            )
        down_button.place(
                x=(self.width / 2) - 25,
                y=380,
                width=50,
                height=30
            )

        ElementsTK.items.append({'list': self.label_listbox})

    def up_file_list(self) -> None:
        """
        """
        item_index = self.get_item_and_index()
        if item_index is not None:
            item_selected, position = item_index
            new_position = position - 1
            if new_position >= 0:
                self.relocate_item(
                        position=position,
                        new_position=new_position,
                        item_selected=item_selected
                    )
        self.re_render_canvas()

        self.update_entry_filename_save()

    def down_file_list(self) -> None:
        """
        """
        item_index = self.get_item_and_index()
        if item_index is not None:
            item_selected, position = item_index
            new_position = position + 1
            if new_position < self.total_index:
                self.relocate_item(
                        position=position,
                        new_position=new_position,
                        item_selected=item_selected
                    )
        self.re_render_canvas()

        self.update_entry_filename_save()

    def update_entry_filename_save(self) -> None:
        """
        """
        name_ = self.listbox_files.get(0, 'end')[0].replace('.pdf', '')
        self.entry_filename.set(name_)

    def relocate_item(
        self,
        position: int,
        new_position: int,
        item_selected: str
    ) -> None:
        """
        """
        self.listbox_files.delete(position)
        self.listbox_files.insert(new_position, item_selected)
        self.listbox_files.selection_set(new_position)

    def get_item_and_index(self) -> Union[Tuple[str, int], None]:
        """
        """
        try:
            item_selected = self.listbox_files.get(
                                    self.listbox_files.curselection()
                                )
            position = self.listbox_files.get(0, 'end').index(item_selected)
            return item_selected, position
        except tk.TclError as e:
            return None

    def get_listbox(self) -> list:
        """
        """
        names = self.listbox_files.get(0, 'end')
        paths = [self.path_pdf_files_dict[i] for i in names]
        return paths

    def re_render_canvas(self) -> None:
        """
        """
        sorted_PDF_files = {
            i: PDFiles.selected[i]
            for i in self.get_listbox()
        }

        PDFiles.selected = sorted_PDF_files

        self.displaycanvas.clear_canvas()
        self.displaycanvas.to_canvas()


class DisplayCanvas(MainGUI):
    """
    """
    def __init__(
        self,
        mainTk: Tk,
        height_canvas: int,
        width_canvas: int
    ) -> None:
        """
        """
        self.mainTk = mainTk

        self.frame = ttk.Frame(self.mainTk)

        self.height_canvas = height_canvas
        self.width_canvas = width_canvas

        self.image_height = self.height_canvas - 60
        self.image_width = self.width_canvas - 20

        self.images_pdf = []

        self.current_page = 0
        self.total_pages = 0
        self.current_image = None

        self.frame.place(
            x=290,
            y=10,
            height=self.height_canvas,
            width=self.width_canvas
        )

    def show(self) -> None:
        """
        """
        self.canvas = tk.Canvas(self.frame, bg='#f7f9f9')

        self.canvas.place(
                        x=0,
                        y=0,
                        width=self.width_canvas,
                        height=self.height_canvas - 40
                    )

    def show_buttons(self) -> None:
        """
        """
        self.frame_buttons = ttk.Frame(self.frame)

        self.button_prev = ttk.Button(
                                    self.frame_buttons,
                                    text=u'\u21E6',
                                    command=self.prev_page
                                )

        self.button_current_page = ttk.Button(
                                            self.frame_buttons,
                                            text="",
                                            command=None
                                        )

        self.button_current_page.state(['disabled'])

        self.button_next = ttk.Button(
                                    self.frame_buttons,
                                    text=u'\u21E8',
                                    command=self.next_page
                                )

        middle_frame = (self.width_canvas / 2)

        self.frame_buttons.place(
                                x=0,
                                y=self.height_canvas - 40,
                                relwidth=1,
                                height=40
                            )
        self.button_prev.place(
                            x=middle_frame - 75,
                            y=0,
                            width=50,
                            height=30
                        )
        self.button_current_page.place(
                                    x=middle_frame - (50 / 2),
                                    y=0,
                                    width=50,
                                    height=30
                                )
        self.button_next.place(
                            x=middle_frame + (50 / 2),
                            y=0,
                            width=50,
                            height=30
                        )

    def to_canvas(self) -> None:
        """
        """
        # print('--> ', len(PDFiles.selected))
        self.images_pdf.clear()

        self.show_buttons()

        for filename, pdf in PDFiles.selected.items():
            # print(filename, len(pdf))

            for page in pdf:
                page_pix = page.get_pixmap()
                currentImage = Image.frombytes(
                                        mode='RGB',
                                        size=[page_pix.width, page_pix.height],
                                        data=page_pix.samples
                                    )

                resized_img = currentImage.resize(
                                (self.image_width, self.image_height),
                                Image.LANCZOS
                            )

                imageTK = ImageTk.PhotoImage(resized_img)
                self.images_pdf.append(imageTK)

        self.total_pages = len(self.images_pdf)
        self.show_image(imageTK=self.images_pdf[self.current_page])
        self.set_index_page_button()

    def show_image(
        self,
        imageTK: ImageTk.PhotoImage
    ) -> None:
        """
        """
        self.clear_canvas()
        self.canvas.image = imageTK
        self.canvas.create_image(10, 10, image=imageTK, anchor=tk.NW)

    def clear_canvas(self) -> None:
        """
        """
        self.canvas.delete('all')

    def reset_images(self) -> None:
        """
        """
        self.images_pdf.clear()
        self.total_pages = 0
        self.current_image = None

    def next_page(
        self,
        event=None
    ) -> None:
        """
        """
        self.current_page += 1
        if self.current_page < self.total_pages:
            self.show_image(imageTK=self.images_pdf[self.current_page])
        else:
            self.current_page = self.total_pages - 1

        self.set_index_page_button()

    def prev_page(
        self,
        event=None
    ) -> None:
        """
        """
        self.current_page -= 1
        if self.current_page >= 0:
            self.show_image(imageTK=self.images_pdf[self.current_page])
        else:
            self.current_page = 0

        self.set_index_page_button()

    def set_index_page_button(self) -> None:
        """
        """
        string = f'{self.current_page + 1}-{self.total_pages}'
        self.button_current_page['text'] = string


def main() -> None:
    root = Tk()
    gui = MainGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
