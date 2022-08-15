from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class File:
    content: Union[str, bytes]
    filename: Optional[str] = None
