import os

from loot import Loot


class ImplicitDestination:
    def __init__(self, target_dir: str):
        if not target_dir:
            raise ValueError("missing target_dir")

        self.target_dir = target_dir

    def get_dir(self, media_type: Loot) -> str:
        """ Get the destination for the given Media file type. """
        if not media_type:
            raise ValueError("media_type not set")
        if not isinstance(media_type, Loot):
            raise ValueError(f"Expected type Media, got: {type(media_type)}")

        dest = media_type.name.lower()
        # handle english plural correctly
        if media_type in [Loot.Movie, Loot.Show, Loot.Ebook]:
            dest += "s"

        path = os.path.join(self.target_dir, dest)
        return path
