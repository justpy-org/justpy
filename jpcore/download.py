"""
Created on 2022-08-29

@author: wf
"""
import urllib.request
import os
import gzip
import shutil
from pathlib import Path


class Download:
    """
    Utility functions for downloading data
    """

    @staticmethod
    def get_cache_path():
        home = str(Path.home())
        cachedir = f"{home}/.justpy"
        return cachedir

    @staticmethod
    def get_url_content(url: str):
        with urllib.request.urlopen(url) as url_response:
            content = url_response.read().decode()
            return content

    @staticmethod
    def get_file_content(path: str):
        with open(path, "r") as file:
            content = file.read()
            return content

    @staticmethod
    def needs_download(file_path: str, force: bool = False) -> bool:
        """
        Check if a download of the given file_path is necessary that is the file
        does not exist has a size of zero or the download should be forced

        Args:
            file_path(str): the path of the file to be checked
            force(bool): True if the result should be forced to True

        Return:
            bool: True if  a download for this file needed
        """
        if not os.path.isfile(file_path):
            result = True
        else:
            stats = os.stat(file_path)
            size = stats.st_size
            result = force or size == 0
        return result

    @staticmethod
    def download_file(
        url: str, file_name: str, target_directory: str, force: bool = False
    ):
        if Download.needs_download(target_directory, force):
            file_path = f"{target_directory}/{file_name}"
            urllib.request.urlretrieve(url, file_path)

    @staticmethod
    def download_backup_file(
        url: str, file_name: str, target_directory: str, force: bool = False
    ):
        """
        Downloads from the given url the zip-file and extracts the file corresponding to the given file_name.

        Args:
            url: url linking to a downloadable gzip file
            file_name: Name of the file that should be extracted from gzip file
            target_directory(str): download the file this directory
            force (bool): True if the download should be forced

        Returns:
            Name of the extracted file with path to the backup directory
        """
        extract_to = f"{target_directory}/{file_name}"
        # we might want to check whether a new version is available
        if Download.needs_download(extract_to, force=force):
            if not os.path.isdir(target_directory):
                os.makedirs(target_directory)
            zipped = f"{extract_to}.gz"
            print(f"Downloading {zipped} from {url} ... this might take a few seconds")
            urllib.request.urlretrieve(url, zipped)
            print(f"Unzipping {extract_to} from {zipped}")
            with gzip.open(zipped, "rb") as gzipped:
                with open(extract_to, "wb") as unzipped:
                    shutil.copyfileobj(gzipped, unzipped)
                print("Extracting completed")
            if not os.path.isfile(extract_to):
                raise (f"could not extract {file_name} from {zipped}")
        return extract_to
