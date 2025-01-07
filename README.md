# PDFMergeTK

GUI application that allows you to merge PDF files quickly, easily, intuitively and with respect for privacy. Designed to run on Windows and Linux.

---

[![Actions PDFMergeTK](https://github.com/kurotom/PDFMergeTK/actions/workflows/build.yml/badge.svg)](https://github.com/kurotom/PDFMergeTK/actions/workflows/build.yml)

---

> [!IMPORTANT]
> * If you have any problems create an issue in the [`Github Issue` section of the project](https://github.com/kurotom/PDFMergeTK/issues)
>

---


# Install


```bash
$ pip install pdfmergetk
```


# Commands

| Command | Description |
|-|-|
| `mergepdf` | start the program. |
| `mergepdfreset` | in case of an error when trying to open the program, restarts the program's multiple run mechanism (opening the program more than once). |
| `pdfmergetklinks` | creates shortcuts for the program, on desktop on Windows and in `~/.local/share/applications/` on Linux. With the name `PDFMergeTK`.|


## From Github, clone project

```bash
$ git clone https://github.com/kurotom/PDFMergeTK.git

$ cd PDFMergeTK

$ poetry shell

$ poetry install

$ python pdfmergetk
```
