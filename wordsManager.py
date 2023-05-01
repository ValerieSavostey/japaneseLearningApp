import random

from db_connect import DB
from lessons import lessonManager , Lesson, LessonCollection
from util import dotdict
class WordsManager:
    _words = []
    _rand_words= []
    _examples = []
    _level = None
    _quantity = 1
    def __init__(self):
        self.db = DB("./jp_vocab.db")

    def set_quantity(self,quantity):
        self._quantity = quantity

    def get_current_level(self):
        return self._level

    def get_words(self,level="N5"):
        if(self._level==level and self._words==[]):
            return []
        self._level = level
        lessonManager.set_current_level(level)
        self._words = self.db.get_words_by_level(level) or []
        self.get_lessons(level)
        return self._words != []

    def get_rand_words(self):
        self._rand_words = []
        for i in range(self._quantity):
            word = random.choice(self._words)
            self._words.remove(word)
            examples = self.get_examples(word[0])
            self._rand_words.append(Word(word=word,examples=examples))
        return self._rand_words
    def get_examples(self,id):
        return self.db.get_examples_by_word_id(id)

    def save_lessons(self,lesson):
        for word in self._rand_words:
            self.db.set_completed(lesson,word.get_id())

    def get_lessons(self,level="N5"):
       # print(level)
        words = self.db.get_completed_words(level)
        #print(words)
        if words==[]:
            print("NO lessons")
            return
        lessons = []
        lesson_ids = [int(word[5]) for word in words]
        lesson_ids = list(dict.fromkeys(lesson_ids))

        for lesson_id in lesson_ids:
            lesson = []
            for word in words:
                examples = self.get_examples(word[0])
                word_proc = Word(word=word, examples=examples)
                if word[5] == lesson_id:
                    lesson.append(word_proc)
                    #print(word[5])

            lessonManager.generate_lesson(dotdict({"name": "Library"}), lesson, level, lesson_id)

                


class Word:
    def __init__(self, **props):
        self.properties = props.get('word')
        self.examples = props.get('examples')

    def get_id(self):
        return self.properties[0]
    def get_word(self):
        return self.properties[1]

    def get_reading(self):
        if not self.properties[2]:
            return ""
        return self.properties[2]

    def get_meaning(self):
        return self.properties[3]
    def get_examples(self):
        return self.examples

wordsMn = WordsManager()

