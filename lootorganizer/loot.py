from __future__ import annotations

import os
from enum import Enum
from typing import Dict, List, Optional

class Loot(Enum):
    """ Enum describing all possible file types """

    Movie = 1
    Show = 2
    Music = 3
    Ebook = 4
    Unknown = 5


class LootFileProps:
    def __init__(self):
        self._amount = 0
        self._size = 0

    def check(self, filepath: str) -> None:
        self.amount += 1
        size_mib = os.path.getsize(filepath) >> 20
        self._size += size_mib

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, value: int) -> None:
        self._amount = value

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size

    def __gt__(self, other: LootFileProps) -> bool:
        return (self._size, self.amount) > (other._size, other.amount)

    def __eq__(self, other: LootFileProps) -> bool:
        return (self._size, self.amount) == (other._size, other.amount)

    def __repr__(self) -> str:
        return f"{self.amount}, {self._size}"

    def __hash__(self) -> str:
        return hash(f"{self._size}-{self.amount}")


class DirContent:
    def __init__(self, dirname: str, classifier):
        self._dirname = dirname
        self.classifier = classifier
        self._stats = {}
        self._extensions = {}
        self._types = {}

    @property
    def dirname(self) -> str:
        return self._dirname

    @property
    def filetypes(self) -> Dict[Loot, str]:
        return self._stats

    def contains_subtitles(self) -> bool:
        return ".srt" in self._extensions

    def get_files_by_type(self, loot: Loot) -> List[str]:
        if loot not in self._types:
            return []
        return self._types[loot]

    def get_files_for_extension(self, extension: str) -> List[str]:
        extension = extension.lower()
        if not extension.startswith("."):
            extension = f".{extension}"

        if extension not in self._extensions:
            return []

        return self._extensions[extension]

    def add_file(self, directory: str, file_name: str) -> None:
        path = os.path.join(directory, file_name)
        path = os.path.abspath(path)
        mediatype = self.classifier.check_file(file_name, path)
        # add stats
        if mediatype not in self._stats:
            self._stats[mediatype] = LootFileProps()
        self._stats[mediatype].check(path)

        # add type
        if mediatype not in self._types:
            self._types[mediatype] = []
        self._types[mediatype].append(path)

        # add extensions
        _, extension = self.classifier.get_extension(file_name)
        if extension not in self._extensions:
            self._extensions[extension] = []
        self._extensions[extension].append(path)

    def get_dominating_type(self) -> Optional[Loot]:
        if not self.filetypes:
            return None

        # by_size = sorted(self.filetypes.items(), key=lambda kv: kv[1])
        by_size = max(self.filetypes.items(), key=lambda x: x[1])
        if by_size and len(by_size) > 0:
            return by_size[0]

        return Loot.Unknown

    def __repr__(self):
        return f"{self.dirname}: {self.filetypes}"
