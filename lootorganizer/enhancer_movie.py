from loot import Loot
import os
from typing import Optional, List, Dict

# TODO: Configureable
DESIRED_LANGUAGES = [
    "german",
    "deutsch",
    "english",
    "englisch"
]


def handle_subtitles(content, file_handler) -> bool:
    subtitles = content.get_files_for_extension("srt")
    if not subtitles:
        return False

    movies = [movie for movie in content.get_files_by_type(Loot.movie) if not movie.lower().endswith(".srt")]
    if not movies or len(movies) > 1:
        return False

    performed_changes = False
    filtered_subtitles = _filter_subtitles(subtitles, movies[0], DESIRED_LANGUAGES)
    for old in filtered_subtitles:
        new = filtered_subtitles[old]
        old_path = os.path.join(content.dirname, old)
        new_path = os.path.join(content.dirname, new)
        # update content
        content._types[Loot.movie].remove(old)
        content._types[Loot.movie].append(new)
        file_handler.move(old_path, new_path)
        # delete this processed subtitle from the list of subtitles
        subtitles.remove(old)
        performed_changes = True

    for subtitle in subtitles:
        # update content
        content._types[Loot.movie].remove(subtitle)
        subtitle_path = os.path.join(content.dirname, subtitle)
        file_handler.delete_file(subtitle_path)
        performed_changes = True

    return performed_changes


def _filter_subtitles(subtitles: List[str], movie_file: str, desired_languages: List[str]) -> Dict[str, str]:
    filtered = {}
    subtitles.sort(reverse=False)
    movie_name = _remove_extension(movie_file)

    for subtitle in subtitles:
        # test for desired languages that make up the filename, such as
        # 2_english.srt
        for lang in desired_languages:
            if lang in subtitle.lower():
                lang_code = _get_iso_lang_code(lang)
                if lang_code:
                    filtered[subtitle] = _get_subtitle_filename(movie_name, lang_code)
                    # only add the first occurrence of a language and ignore further subtitles
                    desired_languages.remove(lang)
            else:
                subtitle_filename = os.path.basename(subtitle)
                subtitle_name = _remove_extension(subtitle_filename)

                movie_filename = os.path.basename(movie_file)
                movie_name = _remove_extension(movie_filename)

                if subtitle_name.lower() == movie_name.lower():
                    filtered[subtitle] = f"{movie_name}.srt"

    return filtered


def _remove_extension(filename) -> str:
    return os.path.splitext(filename)[0]


def _get_subtitle_filename(movie_name: str, lang_code: str) -> str:
    return f"{movie_name}.{lang_code}.srt"


def _get_iso_lang_code(lang: str) -> Optional[str]:
    # TODO: Use library to detect lang codes
    lang = lang.lower()
    if lang == "german" or lang == "deutsch":
        return "de"
    if lang == "english" or lang == "englisch":
        return "en"
    if lang == "portuguese":
        return "pt"

    return None
