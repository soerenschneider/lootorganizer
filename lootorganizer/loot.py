import os
from enum import Enum


class Loot(Enum):
    """ Enum describing all possible file types """

    movie = 1
    show = 2
    music = 3
    ebook = 4
    unknown = 5


class LootFileProps:
    def __init__(self):
        self._amount = 0
        self._size = 0

    def check(self, filepath: str) -> None:
        self.amount += 1
        size_mib = os.path.getsize(filepath) >> 20
        self.size = self.size + size_mib

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
        return (self.size, self.amount) > (other.size, other.amount)

    def __eq__(self, other: LootFileProps) -> bool:
        return (self.size, self.amount) == (other.size, other.amount)

    def __repr__(self) -> str:
        return f"{self.amount}, {self.size}"

    def __hash__(self) -> str:
        return hash(f"{self.size}-{self.amount}")


class DirContent:
    def __init__(self, dirname: str, classifier):
        self._dirname = dirname
        self.classifier = classifier
        self._stats = dict()
        self._extensions = dict()
        self._types = dict()

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
            return list()

        return self._extensions[extension]

    def add_file(self, dir: str, file_name: str) -> None:
        path = os.path.join(dir, file_name)
        mediatype = self.classifier.check_file(file_name)
        # add stats
        if mediatype not in self._stats:
            self._stats[mediatype] = LootFileProps()
        self._stats[mediatype].check(path)

        # add type
        if mediatype not in self._types:
            self._types[mediatype] = list()
        self._types[mediatype].append(path)

        # add extensions
        _, extension = self.classifier.get_extension(file_name)
        if extension not in self._extensions:
            self._extensions[extension] = list()
        self._extensions[extension].append(path)

    def get_dominating_type(self) -> Optional[Loot]:
        if not self.filetypes:
            return None

        # by_size = sorted(self.filetypes.items(), key=lambda kv: kv[1])
        by_size = max(self.filetypes.items(), key=lambda x: x[1])
        if by_size and len(by_size) > 0:
            return by_size[0]

        return Loot.unknown

    def __repr__(self):
        return f"{self.dirname}: {self.filetypes}"
