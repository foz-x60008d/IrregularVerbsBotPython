import random
from collections import namedtuple

FORMS = ['present', 'past', 'past_participle']

Word = namedtuple('Word', FORMS)


class TrainSession:
    def __init__(self, words):
        self.words = words
        self.current_word = 0
        self.current_question = None

    def ask(self):
        self.current_question = random.choice(FORMS)
        question = "{} - {} - {}".format(
            *(
                getattr(self.words[self.current_word], form) if form != self.current_question else "?"
                for form in FORMS
            )
        )
        return "{}/{} {}".format(self.current_word + 1, len(self.words), question)

    def check_answer(self, answer: str):
        result = getattr(self.words[self.current_word], self.current_question) == answer.lower()
        self.current_word += 1
        return result

    @property
    def finished(self):
        return self.current_word >= len(self.words)
