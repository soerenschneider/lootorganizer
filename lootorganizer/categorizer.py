import os
import logging

from typing import Dict

from enhancer_movie import handle_subtitles
from loot import Loot, DirContent
from fileclassifier import FileClassifier
from guesser import GuessImpl


class Lootorganizer:
    def __init__(self, incoming: str, dest_impl=None, guess_impl=None, file_handler=None):
        self.incoming = incoming

        self.dest = dest_impl
        self.classifier = FileClassifier()

        if not guess_impl:
            self.guess_impl = GuessImpl()
        else:
            self.guess_impl = guess_impl

        self.file_handler = file_handler

    @staticmethod
    def _attach(dictionary: Dict, key: Loot, value: str) -> None:
        if key not in dictionary:
            dictionary[key] = []
        dictionary[key].append(value)

    def travel_dir(self, root: str, dirs_to_move: Dict) -> None:
        dirstats = DirContent(root, self.classifier)
        logging.info("Checking %s", root)

        for dirname, _, filenames in os.walk(root, topdown=False):
            for filename in filenames:
                dirstats.add_file(dirname, filename)

        dominating_content = dirstats.get_dominating_type()
        if not dominating_content:
            return

        Lootorganizer._attach(dirs_to_move, dominating_content, root)
        if Loot.Movie == dominating_content:
            if dirstats.contains_subtitles():
                handle_subtitles(dirstats, self.file_handler)

    def examinate_target(self) -> None:
        files_to_move = {}
        for name in os.listdir(self.incoming):
            path = os.path.join(self.incoming, name)
            if os.path.isdir(path):
                self.travel_dir(path, files_to_move)
            else:
                media_type = self.classifier.check_file(name, path)
                Lootorganizer._attach(files_to_move, media_type, path)

        for target in files_to_move.keys():
            for obj in files_to_move[target]:
                dest_dir = self.dest.get_dir(target)
                if not os.path.isdir(dest_dir):
                    logging.info("Dir %s does not exist, trying to create it", dest_dir)
                    self.file_handler.mkdir(dest_dir)
                self.file_handler.move(obj, dest_dir)

        self.tidy_movies()
        self.tidy_shows()

    def tidy_movies(self) -> None:
        movies = self.dest.get_dir(Loot.Movie)
        for dirpath, dirnames, filenames in os.walk(movies):
            for filename in filenames:
                for ext in FileClassifier.video_extensions:
                    # do not try to move the same file over and over again
                    # therefore, check if the dir we found the file in is
                    # different to the target directory
                    if dirpath != movies and filename.endswith(ext):
                        path = os.path.join(dirpath, filename)
                        self.file_handler.move(path, movies)

        # clean debris
        for dirpath, dirnames, filenames in os.walk(movies):
            for dirname in dirnames:
                path = os.path.join(dirpath, dirname)
                logging.info("Deleting folder %s", path)
                self.file_handler.del_recursively(path)

    def tidy_shows(self) -> None:
        shows = self.dest.get_dir(Loot.Show)

        video_files = {}
        for dirpath, _, filenames in os.walk(shows):
            for filename in filenames:
                for ext in FileClassifier.video_extensions:
                    # do not try to move the same file over and over again
                    # therefore, check if the dir we found the file in is
                    # different to the target directory
                    if dirpath != shows and filename.endswith(ext):
                        path = os.path.join(dirpath, filename)
                        if dirpath not in video_files:
                            video_files[dirpath] = []
                        video_files[dirpath].append(path)

        delete_dirs = []

        for dirpath in video_files:
            subfolder = video_files[dirpath]
            non_subtitles = list(
                filter(lambda filename: not filename.endswith(".srt"), subfolder)
            )
            if len(non_subtitles) == 1:
                delete_dirs.append(dirpath)
                for path in subfolder:
                    self.file_handler(path, shows)
            else:
                showmap = {}
                title = None
                same_title = True
                for path in subfolder:
                    guess_result = self.guess_impl.guess(path)
                    season = guess_result["season"]

                    if season not in showmap:
                        showmap[season] = []
                    showmap[season].append(path)

                    if not title:
                        title = guess_result["title"]
                    elif title != guess_result["title"]:
                        same_title = False

                if same_title:
                    for season in showmap:
                        for episode in showmap[season]:
                            formatted_season = "S{0:02d}".format(season)
                            target = os.path.join(shows, title, formatted_season)
                            if not os.path.isdir(target):
                                self.file_handler.mkdir(target)

                            target_file = os.path.join(
                                target, os.path.basename(episode)
                            )
                            if not os.path.exists(target_file):
                                self.file_handler.move(episode, target)

        # clean debris
        for dirname in delete_dirs:
            path = os.path.join(dirpath, dirname)
            logging.info("Deleting folder %s", path)
            self.file_handler.del_recursively(path)

        self.file_handler.remove_empty_folders(shows)
