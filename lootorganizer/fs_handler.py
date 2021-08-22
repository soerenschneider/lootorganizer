import shutil
import logging
import os


class FileMoveImpl:
    def move(self, old_path: str, new_path: str) -> None:
        logging.info("Moving %s to %s", old_path, new_path)
        shutil.move(old_path, new_path)

    def delete_file(self, path) -> None:
        os.remove(path)

    def del_recursively(self, path: str) -> None:
        shutil.rmtree(path)

    def remove_empty_folders(self, path: str) -> None:
        if not os.path.isdir(path):
            return

        files = os.listdir(path)
        if len(files):
            for file in files:
                fullpath = os.path.join(path, file)
                if os.path.isdir(fullpath):
                    self.remove_empty_folders(fullpath)

        files = os.listdir(path)
        if len(files) == 0:
            logging.info("Deleting empty folder %s", path)
            os.rmdir(path)

    def mkdir(self, path: str):
        os.makedirs(path)


class NopMoveImpl:
    def move(self, old_path: str, new_path: str) -> None:
        logging.info("Moving %s -> %s", old_path, new_path)

    def delete_file(self, path) -> None:
        logging.info("Deleting %s", path)

    def del_recursively(self, path: str) -> None:
        logging.info("Deleting %s recursively", path)

    def remove_empty_folders(self, path: str) -> None:
        logging.info("Deleting empty subfolders for %s", path)

    def mkdir(self, path: str):
        logging.info("Mkdir for %s", path)
