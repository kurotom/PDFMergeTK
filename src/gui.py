# -*- coding: utf-8 -*-
"""
PyPDFMerge GUI.

'ElementsTK' : holds the Tkinter elements to change language of texts.
'LanguagesClass' : class in charge of managing the language.
'LoadImagePDFThread' : class (thread) in charge of loading images of the PDF
                       page.
'MainGUI' : main class of app gui.
'UserListBox' : class in charge displaying the names of all PDF files selected
                by the user.
'DisplayCanvas' : class in charge of displaying the images of the PDF pages.
"""

import tkinter as tk
from tkinter import ttk, Tk

from tkinter import filedialog

import os
import subprocess

from threading import Thread, Event
from queue import Queue

from src.styles import AppStyles
from src.langs import languagesDict
from src.reader import ReaderPDFImage
from src.models import PDFile
from src.dataclass import Data
from src.configmanager import ConfigManager


from typing import Union, Tuple


# from time import sleep


class ElementsTK:
    """
    Holds Tkinter elements, buttons, labels, menu.
    """
    items = []
    menuItems = []


class LanguagesClass:
    """
    In charge of managing language of app.
    """
    lang = 'en'
    language = languagesDict[lang]

    def update(
        lang: str
    ) -> None:
        """
        Update language of app.
        """
        LanguagesClass.lang = lang
        LanguagesClass.language = languagesDict[lang]

    def change_language(
        lang,
        adding_files: bool = False
    ) -> None:
        """
        Manages language changes of Tkinter element texts.
        """
        LanguagesClass.update(lang)

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
                if k == 'open' and adding_files:
                    itemTK['text'] = LanguagesClass.language['add']


class LoadImagePDFThread(Thread):
    """
    Thread in charge of loading images of PDF pages.
    """
    def __init__(
        self,
        height: int,
        width: int,
        canvasDisplay: tk.Canvas,
        event: Event,
        works_queue: Queue,
        is_working: bool
    ) -> None:
        """
        Constructor
        """
        Thread.__init__(self)
        self.image_height = height
        self.image_width = width
        self.canvasDisplay = canvasDisplay
        self.event = event

        self.works_queue = works_queue
        self.is_working = is_working

    def run(self) -> None:
        """
        Run thread.
        """
        # print('> LoadImagePDF thread - Started')
        self.worker()
        # self.dumb_test()
        self.is_working = False

    # def dumb_test(self) -> None:
    #     """
    #     """
    #     print('>> ', self.works_queue.size())
    #     name = self.works_queue.get()
    #     sleep(3)
    #     print(f'---  {name}  ---')
    #
    #     if self.works_queue.size() > 0:
    #         self.dumb_test()

    def worker(self) -> None:
        """
        Main work of loading images.
        """
        is_show_canvas = False

        pdfile_obj = Data.find(name=self.works_queue.get())

        if pdfile_obj is not None:
            if self.event.is_set():
                return
            if pdfile_obj.name not in Data.images_loaded:
                print('==> ', pdfile_obj.name)
                Data.set_loaded_images_pdfile(pdfileObj=pdfile_obj)
                generator_images = ReaderPDFImage.to_image(
                                            pdf_document=pdfile_obj.data,
                                            height=self.image_height,
                                            width=self.image_width
                                        )

                for image in generator_images:

                    if self.event.is_set():
                        break

                    pdfile_obj.images.append(image)
                    Data.add_image(
                                current_name=pdfile_obj.name,
                                image=image
                            )
                    if is_show_canvas is False:
                        is_show_canvas = True
                        self.canvasDisplay.to_canvas()

            if self.works_queue.size() > 0:
                self.worker()
            else:
                return


class TasksQueue(Queue):
    """
    Queue of tasks to load images.
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        super().__init__()
        # self.queue = Queue()
        self.__tasks = set()

    def put(
        self,
        pdf_name: str
    ) -> bool:
        """
        Adds PDF name on queue, avoid duplicates.
        """
        if pdf_name not in self.__tasks:
            # self.queue.put(pdf_name)
            super().put(pdf_name)
            return True
        else:
            return False

    def get(self) -> str:
        """
        Returns element from queue.
        """
        # return self.queue.get()
        return super().get()

    def size(self) -> int:
        """
        Returns size of queue.
        """
        return super().qsize()


class MainGUI:
    """
    Main GUI of app.
    """

    def __init__(
        self,
        rootGUI: Tk,
        lang: str = 'en'
    ) -> None:
        """
        Constructor
        """
#
# Load Configuration
        self.configmanager = ConfigManager()
        self.language_init = lang
        LanguagesClass.lang = None
        self.load_config()
#

#
# related to the Thread.
#
        self.is_working = False
        # self.queue_works = Queue()
        self.queue_works = TasksQueue()
        self.event_thread = Event()
        self.thread_load_image = None
#
# related to Styles
        self.app_style = AppStyles()
#
#

        self.height_canvas = 500
        self.width_canvas = 300
        self.image_height = self.height_canvas - 60
        self.image_width = self.width_canvas - 20

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
                                width_canvas=300,
                                style=self.app_style
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

        self.rootGUI.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self) -> None:
        """
        Load configuration of app.
        """
        langconfig = self.configmanager.load_config()
        if langconfig is not None:
            LanguagesClass.lang = langconfig['lang']
        else:
            LanguagesClass.lang = self.language_init
        LanguagesClass.update(LanguagesClass.lang)

    def save_config(self) -> None:
        """
        Save configuration of app.
        """
        dict_lang = {
            'lang': LanguagesClass.lang
        }
        self.configmanager.save_config(config=dict_lang)

    def menu(self) -> None:
        """
        Builds and displays the application menu.
        """
        menubar = tk.Menu(
                        self.rootGUI,
                        font=(AppStyles.default_font, AppStyles.default_size)
                    )

        self.rootGUI.config(menu=menubar)

        quit_ = tk.Menu(menubar, tearoff=0)
        quit_.add_command(
                    label=LanguagesClass.language['quit'],
                    command=self.rootGUI.destroy,
                    font=(AppStyles.default_font, AppStyles.default_size)
                )

        langs_ = tk.Menu(menubar, tearoff=0)
        langs_.add_command(
                    label=LanguagesClass.language['en'],
                    command=lambda: LanguagesClass.change_language(
                                            lang='en',
                                            adding_files=self.adding_files
                                        ),
                    font=(AppStyles.default_font, AppStyles.default_size)
                )
        langs_.add_command(
                    label=LanguagesClass.language['es'],
                    command=lambda: LanguagesClass.change_language(
                                            lang='es',
                                            adding_files=self.adding_files
                                        ),
                    font=(AppStyles.default_font, AppStyles.default_size)
                )

        menubar.add_cascade(
                    label=LanguagesClass.language['file'],
                    menu=quit_
                )
        menubar.add_cascade(
                    label=LanguagesClass.language['langMenu'],
                    menu=langs_
                )

        # [item , {index: label}]
        ElementsTK.menuItems.append([quit_, {0: 'quit'}])
        ElementsTK.menuItems.append([langs_, {0: 'en', 1: 'es'}])
        ElementsTK.menuItems.append([menubar, {1: 'file', 2: 'langMenu'}])

    def userInterface(
        self
    ) -> None:
        """
        Manages open PDF files button.
        """
        self.app_style.buttons()
        self.open_files = ttk.Button(
                                self.frameUserControl,
                                text=LanguagesClass.language['open'],
                                command=self.select_pdf_widget,
                                style='Button.TButton'
                            )

        self.open_files.place(
                x=75,
                y=0,
                height=30,
                width=120
            )

        ElementsTK.items.append({'open': self.open_files})

    def select_pdf_widget(self) -> None:
        """
        Triggers the Tkinter Dialogs to open PDF files.
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

                self.displaycanvas.clear_canvas()


#
# NOTE: instead using `Data.selected` use `Queue()` to stores names of pdf
# files selected using select file dialog tkinter.
#
#
                for item in filesPDF:
                    # print(item)
                    name_pdf = os.path.basename(item.name)
                    pdfile = PDFile(
                                name=name_pdf,
                                data=ReaderPDFImage.read_pdf(item.name)
                            )
                    Data.add(pdfileObj=pdfile)

                    self.queue_works.put(pdf_name=name_pdf)

                self.output_filename_pdf_entry.set(
                        Data.names[0].replace('.pdf', '')
                    )
#
#
# Load Images PDF - Async
                self.event_thread.clear()
                self.thread_load_image = LoadImagePDFThread(
                                            height=self.image_height,
                                            width=self.image_width,
                                            canvasDisplay=self.displaycanvas,
                                            event=self.event_thread,
                                            works_queue=self.queue_works,
                                            is_working=self.is_working
                                        )
                self.thread_load_image.daemon = True
                self.thread_load_image.start()
#
#
#
                self.add_files_pdf_button()

                convert_button = ttk.Button(
                                        self.frameUserControl,
                                        text=LanguagesClass.language['join'],
                                        command=self.start_merge_pdf,
                                        style='ButtonJoinMerge.TButton'
                                    )
                convert_button.place(
                            x=75,
                            y=460,
                            height=30,
                            width=120
                        )

                self.listbox_pdf()

                ElementsTK.items.append({'join': convert_button})

    def add_files_pdf_button(self) -> None:
        """
        Changes text from 'open files' to 'add files' of button.
        """
        self.open_files['text'] = LanguagesClass.language['add']
        self.open_files['command'] = self.select_pdf_widget
        self.adding_files = True

    def save_as(self) -> None:
        """
        Entry to set name of final PDF file.
        """
        if self.show_save_as:

            self.filename_label = ttk.Label(
                                    self.frameUserControl,
                                    text=LanguagesClass.language['name'],
                                    style='LabelListPDF.TLabel'
                                )

            self.filename_entry = ttk.Entry(
                        self.frameUserControl,
                        textvariable=self.output_filename_pdf_entry,
                        font=(AppStyles.default_font, AppStyles.default_size),
                        style='PDFOutput.TEntry'
                    )

            self.filename_label.place(
                    x=0,
                    y=420,
                    height=30,
                    width=70
                )
            self.filename_entry.place(
                    x=80,
                    y=420,
                    height=30,
                    width=self.__width_frame_usercontrol - (105)
                )

            ElementsTK.items.append({'name': self.filename_label})

    def start_merge_pdf(self) -> None:
        """
        Handles merge PDF files and displays the directory where PDF file is
        stored.
        """
        filename_output = self.output_filename_pdf_entry.get()
        filename_output = filename_output.replace('.pdf', '')
        filename_output = '%s.pdf' % (filename_output)
        file_save_path = '%s%s%s' % (
                            os.path.expanduser('~'),
                            os.path.sep,
                            filename_output
                        )

        sorted_files_pdf = self.userlistbox.get_listbox()

        first_pdf = sorted_files_pdf[0]
        pdf_object = Data.find(name=first_pdf)
        first_pdf_data = pdf_object.data

        file_save_path_data = ReaderPDFImage.read_pdf()

        for pdfile_name in sorted_files_pdf[1:]:
            pdfObj = Data.find(name=pdfile_name)
            first_pdf_data.insert_pdf(pdfObj.data)

        file_save_path_data.insert_pdf(first_pdf_data)

        file_save_path_data.save(file_save_path)

        self.show_directory_file_merged(file_path=file_save_path)

    def show_directory_file_merged(
        self,
        file_path: str
    ) -> None:
        """
        Displays the directory where the PDF file is written.
        """
        file_path = os.path.dirname(file_path)
        if self.configmanager.current_platform == 'linux':
            subprocess.run(['xdg-open', file_path])
        elif self.configmanager.current_platform == 'darwin':
            subprocess.run(['open', file_path])
        elif self.configmanager.current_platform == 'win32':
            os.startfile(file_path)
        else:
            # Platform Error.
            pass

    def listbox_pdf(self) -> None:
        """
        Instance of UserListBox.
        """
        self.userlistbox = UserListBox(
                            frame=self.frameUserControl,
                            width=self.__width_frame_usercontrol,
                            entry_filename=self.output_filename_pdf_entry,
                            displaycanvas=self.displaycanvas,
                            style=self.app_style
                        )

    def on_closing(self):
        """
        Termination operations before closing app.
        """
        # print('> on_closing - MainGUI')
        self.save_config()
        if self.thread_load_image is not None:
            self.event_thread.set()
            self.event_thread.clear()
            self.thread_load_image = None
            Data.close()

        self.rootGUI.destroy()


class UserListBox(MainGUI):
    """
    Class in charge to builds listbox with names of PDF files selected by user.
    """

    def __init__(
        self,
        frame: tk.Frame,
        width: int,
        entry_filename: tk.StringVar,
        displaycanvas: tk.Canvas,
        style: ttk.Style
    ) -> None:
        """
        Constructor
        """
        self.index = 0
        self.width = width

        self.displaycanvas = displaycanvas
        self.total_index = len(Data.names)
        self.entry_filename = entry_filename
# Styles
        self.style = style
        self.style.labels()
#
        self.list_pdfs = [
            ' %s' % (i)
            for i in Data.names
        ]

        self.frame = frame

        self.label_listbox = ttk.Label(
                                self.frame,
                                text=LanguagesClass.language['list'],
                                style='LabelListbox.TLabel'
                            )

        self.choices = tk.StringVar()
        self.listbox_files = tk.Listbox(
                    self.frame,
                    listvariable=self.choices,
                    font=(AppStyles.default_font, AppStyles.default_size)
                )
        # print('--> ', self.path_pdf_files_dict)

        self.choices.set(self.list_pdfs)

        self.horizontalScroll = ttk.Scrollbar(
                                self.frame,
                                orient=tk.HORIZONTAL,
                                command=self.listbox_files.xview
                            )
        self.verticalScroll = ttk.Scrollbar(
                                self.frame,
                                orient=tk.VERTICAL,
                                command=self.listbox_files.yview
                            )

        self.listbox_files.configure(
                xscrollcommand=self.horizontalScroll.set,
                yscrollcommand=self.verticalScroll.set
            )

#
        self.up_button = ttk.Button(
                    self.frame,
                    text=u'\u21E7',
                    command=self.up_file_list,
                    style='ButtonController.TButton'
                )
        self.down_button = ttk.Button(
                    self.frame,
                    text=u'\u21E9',
                    command=self.down_file_list,
                    style='ButtonController.TButton'
                )
        self.delete_button = ttk.Button(
                    self.frame,
                    text=u'\U0001F5D1',
                    command=self.delete_pdf_item,
                    style='ButtonController.TButton'
                )

# ListBox Place
        self.label_listbox.place(
                x=75,
                y=40,
                height=30,
                # width=self.width - (30)
                width=120
            )
        self.listbox_files.place(
                x=0,
                y=70,
                height=300,
                width=self.width - (45)
            )
        self.horizontalScroll.place(
                x=0,
                y=365,
                height=15,
                width=self.width - (45)
            )
        self.verticalScroll.place(
                x=self.width - (45),
                y=70,
                height=295,
                width=15
            )
#
# Buttons ListBox
        self.up_button.place(
                x=0,
                y=384,
                width=60,
                height=30
            )
        self.down_button.place(
                x=62,
                y=384,
                width=60,
                height=30
            )
        self.delete_button.place(
                # x=(self.width / 2) - 75,
                x=(self.width - 2) - 90,
                y=384,
                width=60,
                height=30
            )
#
        ElementsTK.items.append({'list': self.label_listbox})

    def up_file_list(self) -> None:
        """
        Manages behavior of button "up" to change position of name.
        """
        item_index = self.get_item_and_index_selected()
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

    def down_file_list(self) -> None:
        """
        Manages behavior of button "down" to change position of name.
        """
        item_index = self.get_item_and_index_selected()
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

    def delete_pdf_item(self) -> None:
        """
        Manages the operations of deleting rows from the list.
        """
        item_str, index = self.get_item_and_index_selected()
        # print('delete listbox - ', index, item_str)

        self.listbox_files.delete(index)

        index_deleted = Data.delete(pdf_name=item_str)

        self.re_render_canvas()

    def update_entry_filename_save(self) -> None:
        """
        Update text on Entry element.
        """
        if len(Data.selected) == 0:
            self.entry_filename.set('')
        else:
            name_ = self.listbox_files.get(0, 'end')[0].replace('.pdf', '')
            self.entry_filename.set(name_.strip())

    def relocate_item(
        self,
        position: int,
        new_position: int,
        item_selected: str
    ) -> None:
        """
        Changes location of elements on list of ListBox element.
        """
        self.listbox_files.delete(position)
        self.listbox_files.insert(new_position, item_selected)
        self.listbox_files.selection_set(new_position)

    def get_item_and_index_selected(self) -> Union[Tuple[str, int], None]:
        """
        Gets and returns the selected list item and its position as a tuple.
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
        Gets and returns all names of elements on list.
        """
        names = self.listbox_files.get(0, 'end')
        return [i.strip() for i in names]

    def re_render_canvas(self) -> None:
        """
        Re-render the canvas element (tk.Canvas), update button index page.
        """
        self.update_entry_filename_save()

        Data.sort(listKey=self.get_listbox())

        self.displaycanvas.clear_canvas()
        self.displaycanvas.set_index_page_button()
        self.displaycanvas.to_canvas()


class DisplayCanvas(MainGUI):
    """
    Class in charge to displays elements on Canvas.
    """

    def __init__(
        self,
        mainTk: Tk,
        height_canvas: int,
        width_canvas: int,
        style: ttk.Style
    ) -> None:
        """
        Constructor
        """
        self.mainTk = mainTk
        self.style = style

        self.frame = ttk.Frame(self.mainTk)

        self.height_canvas = height_canvas
        self.width_canvas = width_canvas

        self.image_height = self.height_canvas - 60
        self.image_width = self.width_canvas - 20

        self.current_pdf = None
        self.current_page = 0

        self.is_show_buttons = False

        self.frame.place(
            x=290,
            y=10,
            height=self.height_canvas,
            width=self.width_canvas
        )

    def show(self) -> None:
        """
        Builds canvas element.
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
        Displays the next and previous buttons for managing images on the
        canvas.
        """
        if self.is_show_buttons is False:

            self.is_show_buttons = True

            self.frame_buttons = ttk.Frame(self.frame)

            self.button_prev = ttk.Button(
                                        self.frame_buttons,
                                        text=u'\u21E6',
                                        command=self.prev_page,
                                        style='ButtonController.TButton'
                                    )

            self.button_current_page = ttk.Button(
                                                self.frame_buttons,
                                                text="",
                                                command=None,
                                                style='IndexButtonPage.TButton'
                                            )

            self.button_current_page.state(['disabled'])

            self.button_next = ttk.Button(
                                        self.frame_buttons,
                                        text=u'\u21E8',
                                        command=self.next_page,
                                        style='ButtonController.TButton'
                                    )

            self.button_delete = ttk.Button(
                                        self.frame_buttons,
                                        text=u'\U0001F5D1',
                                        command=None
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
        Handles the behavior of the Canvas element, displaying the image
        corresponding to the page number.
        """
        self.show_buttons()

        self.clear_canvas()

        self.set_index_page_button()

        # print('>> ', Data.total_pages)

        if Data.total_pages > 0:
            try:
                currentImage = Data.imagesTK[self.current_page]
            except IndexError:
                # print('Error Index, Data.imagesTK')
                # print('-> ', len(Data.imagesTK))
                self.current_page = Data.total_pages - 1
                currentImage = Data.imagesTK[self.current_page]

            # print(Data.status())

            self.canvas.image = currentImage
            self.canvas.create_image(10, 10, image=currentImage, anchor=tk.NW)

            if self.current_page < Data.total_pages:
                self.button_next.state(['!disabled'])

            if self.current_page >= 0:
                self.button_prev.state(['!disabled'])

        else:
            self.button_next.state(['disabled'])
            self.button_prev.state(['disabled'])
            self.set_index_page_button(index=0)

    def clear_canvas(self) -> None:
        """
        Cleans the canvas element.
        """
        self.canvas.delete('all')

    def next_page(
        self,
        event=None
    ) -> None:
        """
        Handles behavior to show image of page.
        """
        self.button_next.state(['!disabled'])
        self.button_prev.state(['!disabled'])

        self.current_page += 1

        if self.current_page < Data.total_pages:
            self.to_canvas()
        else:
            self.current_page = self.current_page - 1
            self.button_next.state(['disabled'])

    def prev_page(
        self,
        event=None
    ) -> None:
        """
        Handles behavior to show image of page.
        """
        self.button_prev.state(['!disabled'])
        self.button_next.state(['!disabled'])

        self.current_page -= 1

        if self.current_page >= 0:
            self.to_canvas()
        else:
            self.current_page = 0
            self.button_prev.state(['disabled'])

    def set_index_page_button(
        self,
        index: int = None
    ) -> None:
        """
        Sets number of current page.
        """
        if index is None:
            self.button_current_page['text'] = '%s' % (self.current_page + 1)
        else:
            self.current_page = index
            self.button_current_page['text'] = '%s' % (self.current_page + 1)


def main() -> None:
    """
    """
    root = Tk()
    gui = MainGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
