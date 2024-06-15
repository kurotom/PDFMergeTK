# -*- coding: utf-8 -*-
"""
Thread related to antivirus, pyinstaller, and false positives.

https://github.com/pyinstaller/pyinstaller/issues/5579
"""

import pefile
import sys
import os


def re_checksum_file(file_path: str) -> None:
    """
    """
    name_, ext_ = os.path.splitext(file_path)
    if ext_.lower() != '.exe':
        ext_ = ''

    final_binary = '%s_new_checksum%s' % (name_, ext_)

    pe = pefile.PE(file_path)
    print('CheckSum: ', pe.OPTIONAL_HEADER.CheckSum)
    pe.OPTIONAL_HEADER.CheckSum = pe.generate_checksum()
    print('New Checksum: ', pe.OPTIONAL_HEADER.CheckSum)
    pe.close()
    pe.write(final_binary)
    print('Verify checksum: ', pe.verify_checksum())


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        re_checksum_file(file_path=args[1])
