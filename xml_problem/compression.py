import io
import os
import zipfile
from abc import ABCMeta, abstractmethod
from typing import IO, Iterable, Union
from uuid import uuid4

from xml_problem.common import File


class ZipFile(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def create_zipfile(content: Iterable[File]) -> bytes:
        ...

    @staticmethod
    @abstractmethod
    def unpack_zipfile(file: Union[str, os.PathLike[str], IO[bytes]], ) -> Iterable[File]:
        zipped_file = zipfile.ZipFile(file=file, mode='r')
        zipped_file.testzip()
        return [File(filename=i, content=zipped_file.read(name=i)) for i in zipped_file.namelist()]


class ZipFileImpl(ZipFile):
    @staticmethod
    def create_zipfile(content: Iterable[File]) -> bytes:
        file_obj = io.BytesIO()
        zipped_file = zipfile.ZipFile(file=file_obj, mode='w', compresslevel=9)
        for file_to_arch in content:
            zipped_file.writestr(
                zinfo_or_arcname=file_to_arch.filename if
                file_to_arch.filename else f'{uuid4().hex}.xml',
                data=file_to_arch.content)
        zipped_file.testzip()
        zipped_file.close()
        file_obj.seek(0)
        return file_obj.read()

    @staticmethod
    def unpack_zipfile(file: Union[str, os.PathLike[str], IO[bytes]], ) -> Iterable[File]:
        zipped_file = zipfile.ZipFile(file=file, mode='r')
        zipped_file.testzip()
        return [File(filename=i, content=zipped_file.read(name=i)) for i in zipped_file.namelist()]
