# -*- coding: utf-8 -*-
"""
VirusTotal API Documentation, https://docs.virustotal.com/reference/overview
"""

import hashlib
import requests
import sys
import os


class VirusTotal:
    """
    """

    def __init__(
        self,
        file: str,
        apikey: str
    ) -> None:
        """
        """
        self.file = file
        self.apikey = apikey
        self.url_api = ''
        self.max_size = 1000000 * 32
        self.id_file = None

        self.data_file = None
        self.__with_hash = False
        self.hash_file = {}
        self.algorithms = {
            'sha256': hashlib.sha256,
            'sha1': hashlib.sha1,
            'md5': hashlib.md5
        }
        self.read_file()
        self.__get_hash_sha256()

    def read_file(self) -> None:
        """
        """
        with open(self.file, 'rb') as file:
            self.data_file = file.read()

    def __get_hash_sha256(self) -> None:
        """
        """
        if self.__with_hash is False:
            self.__with_hash = True

            for name, algorithm in self.algorithms.items():
                if name not in self.hash_file:
                    instance = algorithm(self.data_file)
                    self.hash_file[name] = instance.hexdigest()

    def is_bigger(self) -> bool:
        """
        """
        size_file = os.path.getsize(self.file)
        if size_file < self.max_size:
            return False
        else:
            return True

    def get_endpoint_api(self) -> str:
        """
        """
        if not self.is_bigger():
            return "https://www.virustotal.com/api/v3/files"
        else:
            url = "https://www.virustotal.com/api/v3/files/upload_url"
            req = self.get(url=url)
            return req.json()['data']

    @property
    def get_endpoint_analysis_file(self) -> str:
        """
        """
        return "https://www.virustotal.com/api/v3/analyses/%s" % self.id_file

    @property
    def scan_file(self) -> str:
        """
        """
        res_post = self.post

        if res_post.status_code == 200:
            self.id_file = res_post.json()['data']['id']

            res_analysis_vtt = self.get(url=self.get_endpoint_analysis_file)

            if res_analysis_vtt.status_code == 200:

                print(self.make_url_gui())
                self.set_environment_variables()

                return self.make_url_gui()
            else:
                return ''
        else:
            return ''

    @property
    def post(self) -> requests.Response:
        """
        """
        res = requests.post(
                url=self.get_endpoint_api(),
                files=self.get_header_files(),
                headers=self.get_header()
            )
        return res

    def get(
        self,
        url: str
    ) -> requests.Response:
        """
        """
        return requests.get(url=url, headers=self.get_header())

    def get_header_files(self) -> dict:
        """
        """
        return {
                "file": (
                    f"{os.path.basename(self.file)}",
                    open(f"{self.file}", "rb"),
                    "application/octet-stream"
                )
            }

    def get_header(self) -> dict:
        """
        """
        return {
            "accept": "application/json",
            "x-apikey": f"{self.apikey}"
        }

    def make_url_gui(self) -> dict:
        """
        """
        return {
            name: "https://www.virustotal.com/gui/file/%s/detection" % (hash)
            for name, hash in self.hash_file.items()
        }

    def set_environment_variables(self) -> None:
        """
        """
        with open('link_vtt.txt', 'w') as fl:
            for name, link in self.make_url_gui().items():
                link_ = '%s\n' % (link)
                fl.writelines(link_)


if __name__ == '__main__':
    args = sys.argv

    file = args[1]
    api_key_vt = args[2]

    vtt = VirusTotal(file=file, apikey=api_key_vt)
    vtt.scan_file
