import csv
import io
from abc import ABCMeta, abstractmethod
from typing import Iterable

from xml_problem.xml_content import XmlParseResult


class ReportFile(metaclass=ABCMeta):
    @abstractmethod
    def generate_level_report(self, data: Iterable[XmlParseResult]) -> str:
        ...

    @abstractmethod
    def generate_objects_report(self, data: Iterable[XmlParseResult]) -> str:
        ...


class CSVReportFile(ReportFile):

    def generate_objects_report(self, data: Iterable[XmlParseResult]) -> str:
        file_obj = io.StringIO()
        fieldnames = ['id', 'object_name']
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for parse_result in data:
            for object_name in parse_result.objects:
                writer.writerow({'id': parse_result.level, 'object_name': object_name})
        file_obj.seek(0)
        return file_obj.read()

    def generate_level_report(self, data: Iterable[XmlParseResult]) -> str:
        file_obj = io.StringIO()
        fieldnames = ['id', 'level']
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for parse_result in data:
            writer.writerow({'id': parse_result.id, 'level': parse_result.level})
        file_obj.seek(0)
        return file_obj.read()
