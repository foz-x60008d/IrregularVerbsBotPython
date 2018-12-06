import csv

from bot.classes import Word


def words_reader(csv_name):
    with open(csv_name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            translation, present, past, participle = row
            yield Word(translation, present, past, participle)
