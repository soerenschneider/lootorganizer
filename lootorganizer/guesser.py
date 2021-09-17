from typing import Dict

from guessit import guessit


class GuessImpl:
    def guess(self, filename: str) -> Dict:
        """
        This is a wrapper around guessit that is built because guessit
        sometimes returns inconsistent types. In this particular case,
        a string is returned 99% of time but sometimes a list, which
        does not make any sense. If a list is returned for title, take
        the first entry and throwaway the rest.
        """
        guess_result = guessit(filename)
        if isinstance(guess_result["title"], list):
            guess_result["title"] = guess_result["title"][0]

        if isinstance(guess_result["season"], list):
            guess_result["season"] = 0

        return guess_result
