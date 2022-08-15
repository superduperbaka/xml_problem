import argparse
import itertools
import multiprocessing
import os
import random
import string
import tempfile
from typing import Iterable
from uuid import uuid4

from xml_problem.common import File
from xml_problem.compression import ZipFileImpl
from xml_problem.report import CSVReportFile
from xml_problem.xml_content import GenerateXmlImpl, ReadXMLImpl, XmlParseResult


class XmlData:
    @staticmethod
    def generate_xml_data(
            files_count: int,
    ) -> Iterable[str]:
        return [GenerateXmlImpl.generate_xml(
            id_value=uuid4().hex,
            level_value=str(random.randint(1, 100)),
            objects_count=random.randint(1, 10),
            random_str_func=lambda: ''.join(
                random.sample(string.ascii_letters, k=random.randint(1, len(string.ascii_letters))))
        ) for _ in range(files_count)]


def consumer_job(path: str) -> Iterable[XmlParseResult]:
    with open(path, 'rb') as file:
        arch_content = ZipFileImpl().unpack_zipfile(file)
        return [ReadXMLImpl.read_xml(i.content) for i in arch_content]


def main(processes: int, zip_files: int, directory: str, xml_files: int):
    for _ in range(zip_files):
        xml_data = XmlData.generate_xml_data(files_count=xml_files)
        zip_arch = ZipFileImpl.create_zipfile(content=[File(content=i) for i in xml_data])
        with open(os.path.join(directory, f'{uuid4().hex}.zip'), 'wb') as file:
            file.write(zip_arch)

    with multiprocessing.Pool(processes=processes) as pool:
        mp_result = pool.map(
            consumer_job,
            [os.path.join(directory, i) for i in filter(lambda x: x.endswith('.zip'), os.listdir(directory))]
        )

    report = CSVReportFile()
    with open(f'{os.path.join(directory,"level_report")}.csv', 'w') as file:
        file.write(report.generate_level_report(list(itertools.chain.from_iterable(mp_result))))
    with open(f'{os.path.join(directory,"objects_report")}.csv', 'w') as file:
        file.write(report.generate_objects_report(list(itertools.chain.from_iterable(mp_result))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--processes_count', required=False, type=int,
                        default=(multiprocessing.cpu_count() * 2) - 1)
    parser.add_argument('-z', '--zip_files_count', required=False, default=50, type=int)
    parser.add_argument('-d', '--dir', required=False, default=tempfile.mkdtemp())
    parser.add_argument('-x', '--xml_files_count', required=False, default=100)
    args = parser.parse_args()
    main(processes=args.processes_count, zip_files=args.zip_files_count, directory=args.dir,
         xml_files=args.xml_files_count)
