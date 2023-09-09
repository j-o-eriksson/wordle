import random
from pathlib import Path


class Worldle:
    def __init__(self, word, dictionary):
        self.history = []
        self.word = word
        self.dictionary = dictionary
        self.bad = set()
        self.exact = set()
        self.partial = set()

    def guess(self, guess):
        matches = [(c1, _match(c1, c2, self.word)) for c1, c2 in zip(guess, self.word)]

        self.bad |= {c for c, m in matches if m == " "}
        self.exact |= {(i, c) for i, (c, m) in enumerate(matches) if m == "*"}
        self.partial |= {(i, c) for i, (c, m) in enumerate(matches) if m == "."}
        self.history.append(f"{guess}\n{''.join(m for _, m in matches)}")

        return matches

    def query(self):
        while True:
            word = input("enter word: ")
            if self._valid(word):
                return word, self.guess(word)

    def print(self):
        print()
        for state in self.history:
            print(state)
            print()
        print()
        print(sorted(self.bad))

    def get_candidates(self):
        return [
            word
            for word in self._get(self.exact, self.partial)
            if all(c in word for _, c in self.partial)
            and all(c not in word for c in self.bad)
        ]

    def _valid(self, guess):
        return len(guess) == 5 and guess in self.dictionary

    def _get(self, exact, partial):
        def _check(letters, word, f):
            for i, c in letters:
                if f(word[i], c):
                    return False
            return True

        return {
            w
            for w in self.dictionary
            if _check(exact, w, lambda a, b: a != b)
            and _check(partial, w, lambda a, b: a == b)
        }


def _match(c1, c2, word):
    if c1 == c2:
        return "*"
    if c1 in word:
        return "."
    return " "


def _parse(p1: Path, p2: Path):
    la = set(p1.read_text().split())
    ta = set(p2.read_text().split())
    return random.choice(list(la)), la | ta


if __name__ == "__main__":
    word, dictionary = _parse(Path("wordle-La.txt"), Path("wordle-Ta.txt"))
    game = Worldle(word, dictionary)

    for _ in range(6):
        word, matches = game.query()
        game.print()

        if all(m == "*" for _, m in matches):
            break

        candidates = game.get_candidates()
        print(f"{len(candidates)} candidate(s):", sorted(candidates[:20]))
    print(word)
