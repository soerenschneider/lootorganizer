from unittest import TestCase
from enhancer_movie import _filter_subtitles


class Test(TestCase):
    def test_extract_subtitles(self):
        subtitles = [
            "thats-the-name-of-the-movie.srt",
            "comments.srt"
        ]
        movie_name = "thats-the-name-of-the-movie.mp4"
        desired_languages = [
            "english"
        ]
        result = _filter_subtitles(subtitles, movie_name, desired_languages)
        expected = {
            "thats-the-name-of-the-movie.srt": "thats-the-name-of-the-movie.srt"
        }
        self.assertEqual(result, expected)

    def test_extract_subtitles_lang(self):
        subtitles = [
            "unrelated.srt",
            "2_English.srt",
            "3_English.srt"
        ]
        movie_name = "thats-the-name-of-the-movie.mp4"
        desired_languages = [
            "english",
            "german"
        ]
        result = _filter_subtitles(subtitles, movie_name, desired_languages)
        expected = {
            "2_English.srt": "thats-the-name-of-the-movie.en.srt"
        }
        self.assertEqual(result, expected)

    def test_extract_subtitles_langs(self):
        subtitles = [
            "unrelated.srt",
            "2_English.srt",
            "3_English.srt",
            "German.srt"
        ]
        movie_name = "thats-the-name-of-the-movie.mp4"
        desired_languages = [
            "english",
            "german"
        ]
        result = _filter_subtitles(subtitles, movie_name, desired_languages)
        expected = {
            "German.srt": "thats-the-name-of-the-movie.de.srt",
            "2_English.srt": "thats-the-name-of-the-movie.en.srt"
        }
        self.assertEqual(result, expected)
