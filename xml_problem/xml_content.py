from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Callable, Iterable, Union

from lxml import etree


@dataclass(frozen=True)
class XmlParseResult:
    id: str
    level: int
    objects: Iterable[str]


class GenerateXml(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def generate_xml(
            id_value: str,
            level_value: str,
            objects_count: int,
            random_str_func: Callable[[], str],
    ) -> str:
        ...


class GenerateXmlImpl(GenerateXml):
    @staticmethod
    def generate_xml(
            id_value: str,
            level_value: str,
            objects_count: int,
            random_str_func: Callable[[], str],
    ) -> str:
        root = etree.Element('root')
        root.append(etree.Element('var', name='id', value=id_value))
        root.append(etree.Element('var', name='level', value=level_value))
        obj = etree.Element('objects')
        root.append(obj)
        for _ in range(objects_count):
            obj.append(etree.SubElement(obj, 'object', name=random_str_func()))
        return etree.tostring(root, pretty_print=True)


class ReadXML(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def read_xml(content: Union[str, bytes]):
        ...


class ReadXMLImpl(ReadXML):
    @staticmethod
    def read_xml(content: Union[str, bytes]) -> XmlParseResult:
        root = etree.fromstring(content)
        id_element = root.find('./var[@name="id"]').get('value')
        level_element = root.find('./var[@name="level"]').get('value')
        objects_element = root.find('./objects')
        return XmlParseResult(
            id=id_element,
            level=int(level_element),
            objects=[i.get('name') for i in objects_element],
        )
