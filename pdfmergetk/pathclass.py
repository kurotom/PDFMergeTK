# -*- cofing: utf-8 -*-
"""
"""

import os
import shutil
import platformdirs

from typing import Tuple


class PathClass:

    __sep = os.path.sep

    @classmethod
    @property
    def separator(cls) -> str:
        """
        """
        return cls.__sep

    def get_desktop() -> str:
        """
        """
        return platformdirs.user_desktop_dir()

    def openfile(
        path: str
    ) -> None:
        """
        """
        os.startfile(path)

    def absolute_path(
        path: str
    ) -> str:
        """
        """
        return os.path.abspath(path=path)

    def delete_file(
        path: str
    ) -> bool:
        """
        """
        return os.remove(path)

    def delete_directory(
        path: str
    ) -> bool:
        """
        """
        try:
            shutil.rmtree(path=path)
            return True
        except Exception as e:
            print(e)
            return False

    def dirname(
        path: str
    ) -> str:
        """
        """
        return os.path.dirname(path)

    def basename(
        path: str
    ) -> str:
        """
        """
        return os.path.basename(path)

    def splitext(
        path: str
    ) -> Tuple[str]:
        """
        """
        return os.path.splitext(PathClass.basename(path))

    def expanduser(
        path: str
    ) -> str:
        return os.path.expanduser(path)

    def join(
        *path: str
    ) -> str:
        """
        """
        return os.path.join(f"{os.path.sep}".join(path))

    def exists(
        path: str
    ) -> bool:
        """
        """
        return os.path.exists(path)

    def realpath(
        path: str
    ) -> str:
        """
        """
        return os.path.realpath(path)

    def makedirs(
        path: str
    ) -> bool:
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        return PathClass.exists(path)
