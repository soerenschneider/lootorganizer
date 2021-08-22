import os
from typing import Optional, Tuple

from loot import Loot
from guesser import GuessImpl


class FileClassifier:
    """ Classifies files by its extensions. """

    video_extensions = [".mkv", ".avi", ".mp4", ".mpg", ".ogv", ".vob", ".srt"]
    music_extensions = [".flac", ".mp3", ".ogg", ".opus", ".wav", ".m4p"]
    ebook_extensions = [".pdf", ".epub", ".mobi"]

    def __init__(self):
        self.guesser = GuessImpl()

    def check_file(self, filename) -> Loot:
        """ Returns the detected media type for the given filename. """

        extension = self.get_extension(filename)
        if not extension or len(extension) < 1:
            return Loot.Unknown

        file_ext = extension[1].lower()
        if file_ext in FileClassifier.ebook_extensions:
            return Loot.Ebook

        if file_ext in FileClassifier.video_extensions:
            guess_result = self.guesser.guess(filename)
            video_type = guess_result["type"]
            if video_type == "episode":
                return Loot.Show
            return Loot.Movie

        if file_ext in FileClassifier.music_extensions:
            return Loot.Music

        return Loot.Unknown

    def get_extension(self, filename: str) -> Optional[Tuple]:
        """ Get the extension for the file. """
        if not filename:
            return None

        split = os.path.splitext(filename)
        if len(split) != 2:
            return None

        return split[0], split[1]
