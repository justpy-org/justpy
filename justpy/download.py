'''
Created on 2022-08-29

@author: wf
'''
import urllib.request
import os
import gzip
import shutil
from pathlib import Path

class Download:
    '''
    Utility functions for downloading data
    '''

    @staticmethod
    def getCachePath():
        home = str(Path.home())
        cachedir = f"{home}/.justpy"
        return cachedir

    @staticmethod
    def getURLContent(url:str):
        with urllib.request.urlopen(url) as urlResponse:
            content = urlResponse.read().decode()
            return content

    @staticmethod
    def getFileContent(path:str):
        with open(path, "r") as file:
            content = file.read()
            return content

    @staticmethod
    def needsDownload(filePath:str,force:bool=False)->bool:
        '''
        check if a download of the given filePath is necessary that is the file
        does not exist has a size of zero or the download should be forced
        
        Args:
            filePath(str): the path of the file to be checked
            force(bool): True if the result should be forced to True
            
        Return:
            bool: True if  a download for this file needed
        '''
        if not os.path.isfile(filePath):
            result=True
        else:
            stats=os.stat(filePath)
            size=stats.st_size
            result=force or size==0
        return result
    
    @staticmethod 
    def downloadFile(url:str,fileName:str, targetDirectory:str,force:bool=False):
        if Download.needsDownload(targetDirectory, force):
            filePath=f"{targetDirectory}/{fileName}"
            urllib.request.urlretrieve(url,filePath)

    @staticmethod
    def downloadBackupFile(url:str, fileName:str, targetDirectory:str, force:bool=False):
        '''
        Downloads from the given url the zip-file and extracts the file corresponding to the given fileName.

        Args:
            url: url linking to a downloadable gzip file
            fileName: Name of the file that should be extracted from gzip file
            targetDirectory(str): download the file this directory
            force (bool): True if the download should be forced

        Returns:
            Name of the extracted file with path to the backup directory
        '''
        extractTo = f"{targetDirectory}/{fileName}"
        # we might want to check whether a new version is available
        if Download.needsDownload(extractTo, force=force):
            if not os.path.isdir(targetDirectory):
                os.makedirs(targetDirectory)
            zipped = f"{extractTo}.gz"
            print(f"Downloading {zipped} from {url} ... this might take a few seconds")
            urllib.request.urlretrieve(url, zipped)
            print(f"Unzipping {extractTo} from {zipped}")
            with gzip.open(zipped, 'rb') as gzipped:
                with open(extractTo, 'wb') as unzipped:
                    shutil.copyfileobj(gzipped, unzipped)
                print("Extracting completed")
            if not os.path.isfile(extractTo):
                raise (f"could not extract {fileName} from {zipped}")
        return extractTo